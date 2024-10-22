import cv2
from pyzbar.pyzbar import decode

# Load an image with a barcode
image = cv2.imread('/home/amruta/Documents/Attendance/attendance_barcode/image.png')  # Replace with the path to an image

# Decode the barcode
decoded_objects = decode(image)
for obj in decoded_objects:
    print(f"Detected barcode: {obj.data.decode('utf-8')}")
