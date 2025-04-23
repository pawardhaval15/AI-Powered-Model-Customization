from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from model.apply_color import apply_color_to_model
from model.resize_model import resize_model_3d
from model.change_texture import change_texture_model
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Configure upload settings
UPLOAD_FOLDER = 'static/models'
ALLOWED_EXTENSIONS = {'glb', 'gltf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve the frontend index.html
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

# Serve JS files
@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('frontend/js', path)

# Serve CSS files
@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('frontend/css', path)

# New route to list available models
@app.route('/api/list-models', methods=['GET'])
def list_models():
    models = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(('.glb', '.gltf')):
            models.append({
                'name': filename,
                'url': f'/static/models/{filename}'
            })
    return jsonify({'models': models})

# New route to upload model
@app.route('/api/upload-model', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            'message': 'File uploaded successfully',
            'model_url': f'/static/models/{filename}'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

# Modified customize-model route
@app.route('/api/customize-model', methods=['POST'])
def customize_model():
    data = request.get_json()
    color = data.get("color")
    scale = data.get("scale")
    texture_prompt = data.get("texture_prompt")
    model_filename = data.get("model_filename", "sofa.glb")  # Default to sofa.glb if not specified

    model_path = os.path.join("static/models", model_filename)
    
    if not os.path.exists(model_path):
        return jsonify({"error": "Model not found"}), 404

    # Apply AI-powered color
    if color:
        apply_color_to_model(model_path, color)

    # Resize 3D model
    if scale:
        resize_model_3d(model_path, scale)

    # Change Texture
    if texture_prompt:
        change_texture_model(model_path, texture_prompt)

    return jsonify({
        "message": "3D model customized!",
        "model_url": f"/static/models/{model_filename}"
    })

if __name__ == '__main__':
    app.run(debug=True)
