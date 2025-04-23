def apply_color_to_model(file_path, color_hex):
    """Apply color to the model materials"""
    import pygltflib
    from pygltflib import GLTF2
    import numpy as np
    import os
    
    # Convert hex color to RGB (0-1 range for glTF)
    color_rgb = [int(color_hex.lstrip('#')[i:i+2], 16)/255.0 for i in (0, 2, 4)]
    color_rgba = color_rgb + [1.0]  # Add alpha channel
    
    # Create a backup of the original file
    backup_file = file_path + ".backup"
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy(file_path, backup_file)

    try:
        # Load the glTF file
        gltf = GLTF2.load(file_path)
        
        # Modify all materials to use the new color
        if hasattr(gltf, 'materials') and gltf.materials:
            for material in gltf.materials:
                if hasattr(material, 'pbrMetallicRoughness'):
                    material.pbrMetallicRoughness.baseColorFactor = color_rgba
        
        # Save the modified file
        gltf.save(file_path)
        print(f"Successfully applied color {color_hex} to model")
        return True
    except Exception as e:
        print(f"Error applying color: {e}")
        # Restore from backup if something went wrong
        if os.path.exists(backup_file):
            import shutil
            shutil.copy(backup_file, file_path)
        return False