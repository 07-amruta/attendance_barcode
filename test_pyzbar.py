import cv2
from pyzbar.pyzbar import decode

# Load an image with a barcode
image = cv2.imread('path_to_your_barcode_image.jpg')  # Replace with the path to an image

# Decode the barcode
decoded_objects = decode(image)
for obj in decoded_objects:
    print(f"Detected barcode: {obj.data.decode('utf-8')}")
