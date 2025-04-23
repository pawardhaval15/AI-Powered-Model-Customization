def change_texture_model(file_path, prompt):
    """Generate and apply a new texture based on a text prompt"""
    print(f"Generating texture from prompt: {prompt}")

    # This is a placeholder for the actual texture generation
    # In a real implementation, you would:
    # 1. Use Stable Diffusion or similar to generate a texture image
    # 2. Apply the texture to the model's UV coordinates

    import pygltflib
    from pygltflib import GLTF2
    import os
    import random

    # Create a backup of the original file
    backup_file = file_path + ".backup"
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy(file_path, backup_file)

    try:
        # Load the glTF file
        gltf = GLTF2.load(file_path)

        # Define preset material properties for various textures
        texture_presets = {
            # Basic materials
            "velvet": {"roughness": 0.9, "metallic": 0.0},
            "leather": {"roughness": 0.7, "metallic": 0.1},
            "metal": {"roughness": 0.2, "metallic": 0.9},
            "steel": {"roughness": 0.2, "metallic": 0.9},
            "wood": {"roughness": 0.8, "metallic": 0.0},

            # Metals
            "chrome": {"roughness": 0.1, "metallic": 1.0},
            "gold": {"roughness": 0.2, "metallic": 1.0},
            "silver": {"roughness": 0.15, "metallic": 0.95},
            "copper": {"roughness": 0.25, "metallic": 0.9},
            "brass": {"roughness": 0.3, "metallic": 0.85},
            "bronze": {"roughness": 0.35, "metallic": 0.8},
            "aluminum": {"roughness": 0.3, "metallic": 0.9},
            "brushed metal": {"roughness": 0.5, "metallic": 0.85},
            "rusted metal": {"roughness": 0.8, "metallic": 0.7},

            # Woods
            "oak": {"roughness": 0.8, "metallic": 0.0},
            "pine": {"roughness": 0.75, "metallic": 0.0},
            "mahogany": {"roughness": 0.7, "metallic": 0.05},
            "walnut": {"roughness": 0.65, "metallic": 0.0},
            "ebony": {"roughness": 0.6, "metallic": 0.0},
            "bamboo": {"roughness": 0.7, "metallic": 0.0},
            "polished wood": {"roughness": 0.4, "metallic": 0.1},
            "distressed wood": {"roughness": 0.9, "metallic": 0.0},

            # Fabrics
            "silk": {"roughness": 0.7, "metallic": 0.0},
            "cotton": {"roughness": 0.8, "metallic": 0.0},
            "linen": {"roughness": 0.85, "metallic": 0.0},
            "wool": {"roughness": 0.9, "metallic": 0.0},
            "satin": {"roughness": 0.6, "metallic": 0.1},
            "denim": {"roughness": 0.85, "metallic": 0.0},
            "canvas": {"roughness": 0.9, "metallic": 0.0},

            # Stone and minerals
            "marble": {"roughness": 0.5, "metallic": 0.1},
            "granite": {"roughness": 0.7, "metallic": 0.05},
            "sandstone": {"roughness": 0.8, "metallic": 0.0},
            "limestone": {"roughness": 0.75, "metallic": 0.0},
            "quartz": {"roughness": 0.4, "metallic": 0.2},
            "slate": {"roughness": 0.8, "metallic": 0.0},
            "obsidian": {"roughness": 0.3, "metallic": 0.2},
            "jade": {"roughness": 0.6, "metallic": 0.1},

            # Glass and ceramics
            "glass": {"roughness": 0.1, "metallic": 0.0},
            "frosted glass": {"roughness": 0.5, "metallic": 0.0},
            "ceramic": {"roughness": 0.4, "metallic": 0.0},
            "porcelain": {"roughness": 0.3, "metallic": 0.0},
            "terracotta": {"roughness": 0.8, "metallic": 0.0},

            # Synthetic materials
            "plastic": {"roughness": 0.5, "metallic": 0.0},
            "rubber": {"roughness": 0.9, "metallic": 0.0},
            "vinyl": {"roughness": 0.6, "metallic": 0.0},
            "carbon fiber": {"roughness": 0.4, "metallic": 0.3},
            "nylon": {"roughness": 0.7, "metallic": 0.0},

            # Natural elements
            "water": {"roughness": 0.1, "metallic": 0.3},
            "ice": {"roughness": 0.2, "metallic": 0.2},
            "snow": {"roughness": 0.9, "metallic": 0.0},
            "sand": {"roughness": 0.8, "metallic": 0.0},
            "mud": {"roughness": 0.95, "metallic": 0.0},
            "grass": {"roughness": 0.9, "metallic": 0.0},
            "bark": {"roughness": 0.95, "metallic": 0.0},

            # Processed materials
            "concrete": {"roughness": 0.8, "metallic": 0.0},
            "brick": {"roughness": 0.85, "metallic": 0.0},
            "asphalt": {"roughness": 0.9, "metallic": 0.0},
            "paper": {"roughness": 0.8, "metallic": 0.0},
            "cardboard": {"roughness": 0.85, "metallic": 0.0},
            "leather worn": {"roughness": 0.8, "metallic": 0.05},
            "leather polished": {"roughness": 0.5, "metallic": 0.15},

            # Specialty finishes
            "matte paint": {"roughness": 0.9, "metallic": 0.0},
            "glossy paint": {"roughness": 0.2, "metallic": 0.0},
            "metallic paint": {"roughness": 0.3, "metallic": 0.5},
            "rust": {"roughness": 0.95, "metallic": 0.3},
            "patina": {"roughness": 0.7, "metallic": 0.4},
            "weathered": {"roughness": 0.85, "metallic": 0.1},
            "polished": {"roughness": 0.2, "metallic": 0.3},
            "brushed": {"roughness": 0.6, "metallic": 0.2},
            "hammered": {"roughness": 0.7, "metallic": 0.4},

            # Composite descriptive textures
            "velvet red floral": {"roughness": 0.9, "metallic": 0.05},
            "worn brown leather": {"roughness": 0.8, "metallic": 0.05},
            "polished chrome metal": {"roughness": 0.1, "metallic": 1.0},
            "oak wood grain": {"roughness": 0.8, "metallic": 0.0},
            "distressed denim": {"roughness": 0.9, "metallic": 0.0},
            "italian marble": {"roughness": 0.5, "metallic": 0.1},
            "brushed aluminum": {"roughness": 0.5, "metallic": 0.9},
            "aged copper": {"roughness": 0.6, "metallic": 0.7},
            "wet concrete": {"roughness": 0.7, "metallic": 0.1},
            "rough granite": {"roughness": 0.8, "metallic": 0.05},
        }

        # Default values if no match is found
        roughness = 0.5
        metallic = 0.0

        # Try to find the best match for the prompt
        best_match = None
        for texture_name, properties in texture_presets.items():
            if texture_name in prompt.lower():
                best_match = texture_name
                roughness = properties["roughness"]
                metallic = properties["metallic"]
                break

        # If no exact match, see if any keywords match
        if best_match is None:
            for texture_name, properties in texture_presets.items():
                if any(word in prompt.lower() for word in texture_name.split()):
                    best_match = texture_name
                    roughness = properties["roughness"]
                    metallic = properties["metallic"]
                    break

        # If still no match, use random values within reasonable ranges
        if best_match is None:
            roughness = random.uniform(0.3, 0.9)
            metallic = random.uniform(0.0, 0.5)
            print(f"No texture preset found for '{prompt}'. Using random values.")
        else:
            print(f"Applying texture preset: {best_match}")

        # Modify all materials
        if hasattr(gltf, 'materials') and gltf.materials:
            for material in gltf.materials:
                if hasattr(material, 'pbrMetallicRoughness'):
                    material.pbrMetallicRoughness.roughnessFactor = roughness
                    material.pbrMetallicRoughness.metallicFactor = metallic

        # Save the modified file
        gltf.save(file_path)
        print(f"Successfully applied texture properties based on '{prompt}'")
        return True
    except Exception as e:
        print(f"Error changing texture: {e}")
        # Restore from backup if something went wrong
        if os.path.exists(backup_file):
            import shutil
            shutil.copy(backup_file, file_path)
        return False