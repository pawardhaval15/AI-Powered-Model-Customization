def resize_model_3d(file_path, scale):
    """Resize the 3D model"""
    import pygltflib
    from pygltflib import GLTF2
    import numpy as np
    import os
    
    # Create a backup of the original file
    backup_file = file_path + ".backup"
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy(file_path, backup_file)
    
    try:
        # Load the glTF file
        gltf = GLTF2.load(file_path)
        
        # Scale nodes that have meshes
        for node in gltf.nodes:
            if hasattr(node, 'scale') and node.scale is not None:
                node.scale = [s * float(scale) for s in node.scale]
            else:
                node.scale = [float(scale), float(scale), float(scale)]
        
        # Save the modified file
        gltf.save(file_path)
        print(f"Successfully resized model with scale factor {scale}")
        return True
    except Exception as e:
        print(f"Error resizing model: {e}")
        # Restore from backup if something went wrong
        if os.path.exists(backup_file):
            import shutil
            shutil.copy(backup_file, file_path)
        return False