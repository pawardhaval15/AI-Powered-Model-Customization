import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';
import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.136.0/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'https://cdn.skypack.dev/three@0.136.0/examples/jsm/controls/OrbitControls.js';

// Debug element
const debugInfo = document.getElementById('debugInfo');
if (!debugInfo) {
  console.warn('Debug info element not found');
}

// Set up scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xeeeeee);

// Get the container dimensions for proper sizing
const container = document.getElementById('viewer');
if (!container) {
  console.error('Viewer container not found');
  throw new Error('Viewer container not found');
}
const containerWidth = container.clientWidth;
const containerHeight = container.clientHeight;

// Set up camera with proper aspect ratio
const camera = new THREE.PerspectiveCamera(
  45, 
  containerWidth / containerHeight, 
  0.1, 
  1000
);
camera.position.z = 5;

// Set up renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(containerWidth, containerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);

// Add controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 10;
controls.target.set(0, 0, 0);

// Improved lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(5, 5, 5);
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 1024;
directionalLight.shadow.mapSize.height = 1024;
scene.add(directionalLight);

const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
fillLight.position.set(-5, 0, -5);
scene.add(fillLight);

// Current model reference and state
let currentModel = null;
let currentModelUrl = sessionStorage.getItem('currentModelUrl') || '/static/models/sofa.glb';

// Model loading function
function loadModel(url) {
  if (debugInfo) debugInfo.innerHTML = 'Loading model...';
  
  return new Promise((resolve, reject) => {
    const loader = new GLTFLoader();
    
    if (currentModel) {
      scene.remove(currentModel);
      currentModel = null;
    }
    
    loader.load(
      url,
      function (gltf) {
        if (debugInfo) debugInfo.innerHTML = 'Model loaded successfully!';
        
        const box = new THREE.Box3().setFromObject(gltf.scene);
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const scale = 2 / maxDim;
        
        gltf.scene.scale.set(scale, scale, scale);
        
        const center = box.getCenter(new THREE.Vector3());
        gltf.scene.position.x = -center.x * scale;
        gltf.scene.position.y = -center.y * scale;
        gltf.scene.position.z = -center.z * scale;
        
        gltf.scene.traverse((node) => {
          if (node.isMesh) {
            node.castShadow = true;
            node.receiveShadow = true;
          }
        });
        
        currentModel = gltf.scene;
        currentModelUrl = url;
        sessionStorage.setItem('currentModelUrl', url);
        
        scene.add(gltf.scene);
        resolve(gltf);
        
        controls.target.set(0, 0, 0);
        controls.update();
      },
      function (xhr) {
        if (xhr.lengthComputable && debugInfo) {
          const percentComplete = Math.round(xhr.loaded / xhr.total * 100);
          debugInfo.innerHTML = `Loading: ${percentComplete}%`;
        }
      },
      function (error) {
        if (debugInfo) debugInfo.innerHTML = 'Error loading model: ' + error.message;
        console.error('Error loading model:', error);
        reject(error);
      }
    );
  });
}

// Model management
document.addEventListener('DOMContentLoaded', function() {
  loadAvailableModels().then(() => {
    const modelSelector = document.getElementById('modelSelector');
    if (modelSelector) {
      const savedModel = sessionStorage.getItem('currentModelUrl');
      if (savedModel) {
        const modelName = savedModel.split('/').pop();
        modelSelector.value = modelName;
        loadModel(savedModel);
      }
    }
  });

  const modelSelector = document.getElementById('modelSelector');
  if (modelSelector) {
    modelSelector.addEventListener('change', function(e) {
      const selectedModel = e.target.value;
      if (selectedModel) {
        const modelUrl = `/static/models/${selectedModel}`;
        loadModel(modelUrl);
      }
    });
  }

  setupFileUpload();
});

// File upload handling
function setupFileUpload() {
  const uploadButton = document.getElementById('uploadButton');
  const fileInput = document.getElementById('modelUpload');
  
  if (uploadButton && fileInput) {
    uploadButton.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', async (event) => {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      if (debugInfo) debugInfo.innerHTML = 'Uploading model...';

      try {
        const response = await fetch('/api/upload-model', {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        if (response.ok) {
          debugInfo.innerHTML = 'Model uploaded successfully!';
          await loadAvailableModels();
          loadModel(data.model_url);
        } else {
          throw new Error(data.error);
        }
      } catch (error) {
        console.error('Error uploading model:', error);
        debugInfo.innerHTML = 'Error uploading model';
        alert('Error uploading model: ' + error.message);
      }
    });
  }
}

// Customization function
function customize() {
  const colorPicker = document.getElementById('colorPicker');
  const scaleInput = document.getElementById('scaleInput');
  const texturePrompt = document.getElementById('texturePrompt');
  const modelSelector = document.getElementById('modelSelector');
  
  if (!colorPicker || !scaleInput || !texturePrompt || !modelSelector) {
    console.error('One or more customization inputs not found');
    return;
  }
  
  const model_filename = modelSelector.value || currentModelUrl.split('/').pop();
  const color = colorPicker.value;
  const scale = parseFloat(scaleInput.value);
  const texture_prompt = texturePrompt.value;
  
  if (isNaN(scale)) {
    alert('Please enter a valid number for scale');
    return;
  }
  
  if (debugInfo) debugInfo.innerHTML = 'Customizing model...';
  
  fetch('/api/customize-model', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      color, 
      scale, 
      texture_prompt,
      model_filename 
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.model_url) {
      debugInfo.innerHTML = 'Customization successful!';
      loadModel(data.model_url);
    } else {
      throw new Error(data.error || 'Unknown error occurred');
    }
  })
  .catch(err => {
    console.error('Customization error:', err);
    debugInfo.innerHTML = `Error: ${err.message}`;
    alert(`Error customizing model: ${err.message}`);
  });
}

// Utility functions
function zoomIn() {
  const zoomSpeed = 0.5;
  camera.position.z = Math.max(controls.minDistance, camera.position.z - zoomSpeed);
  controls.update();
}

function zoomOut() {
  const zoomSpeed = 0.5;
  camera.position.z = Math.min(controls.maxDistance, camera.position.z + zoomSpeed);
  controls.update();
}

function onWindowResize() {
  const newWidth = container.clientWidth;
  const newHeight = container.clientHeight;
  camera.aspect = newWidth / newHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(newWidth, newHeight);
}

// Event listeners and animation
window.addEventListener('resize', onWindowResize);

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

// Initialize
animate();

// Global exports
window.customize = customize;
window.zoomIn = zoomIn;
window.zoomOut = zoomOut;