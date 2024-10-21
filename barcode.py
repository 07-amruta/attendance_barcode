import cv2
from pyzbar.pyzbar import decode
import pandas as pd
from datetime import datetime

barcode_data = []

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    decoded_objects = decode(frame)
    
    for obj in decoded_objects:
        
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
        barcode_text = obj.data.decode('utf-8')
        barcode_type = obj.type

        print(f"Detected {barcode_type}: {barcode_text}")
        barcode_data.append({'Barcode': barcode_text, 'Type': barcode_type, 'Timestamp': datetime.now()})

    cv2.imshow('Barcode Scanner', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if barcode_data:
    df = pd.DataFrame(barcode_data)
    df.to_excel('scanned_barcodes.xlsx', index=False)
    print("Data saved to scanned_barcodes.xlsx")
else:
    print("No barcodes scanned.")
