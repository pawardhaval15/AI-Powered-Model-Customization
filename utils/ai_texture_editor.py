import cv2
import numpy as np
from PIL import Image
import os

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

def apply_color_to_texture(hex_color):
    rgb = hex_to_rgb(hex_color)
    img_path = "static/textures/base_sofa.jpg"
    output_path = "static/textures/sofa_custom.jpg"

    img = cv2.imread(img_path)
    if img is None:
        raise Exception("Base texture not found")

    color_layer = np.full_like(img, rgb)
    blended = cv2.addWeighted(img, 0.5, color_layer, 0.5, 0)

    cv2.imwrite(output_path, blended)
    return output_path
