import cv2
import numpy as np
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time

barcode_database = {
    "1032220289": "Harsh Chourasia",
    "1032222392": "Om Gunjal",
    "1032222399": "Aditya Naik",
    "1032232290": "Jayesh Sangave",
    "1032221144": "Rishit Darwade",
    "1032220740": "Aishwarya Godse",
    "1032221070": "Sourabh Bhosale",
    "1032220354": "Parjanya Kilambi",
    "1032230586": "Shravani Pachpute",
    "1032220415": "Hrishikesh Ghogle",
    "1032220559": "Danish Tapia",
    "1032240120": "Avnish Deshmukh",
    "1032233454": "Amruta Panda",
    "1032210608": "Samyak Kharat",
    "1032211911": "Sujal Bafna",
    "1032240199": "Vishweshwar Patil",
    "1032240202": "Aaditya Patil",
    "1032221888": "Himadri Rajput",
    "1032212583": "Prithviraj Patil",
    "1032210315": "Rameshwar Patil",
    "1032221684": "Rutu Shirke",
}

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("lab-attendance-439409-308fc8515cfc.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Attendance Sheet").sheet1  

cap = cv2.VideoCapture(2)  
cap.set(3, 640)  
cap.set(4, 480) 

plt.ion()  
fig, ax = plt.subplots()

scan_count = 0  
detected_barcodes = set()  
last_detection_time = time.time() 
detection_interval = 2  

while True:
    success, img = cap.read()
    if not success:
        break

    barcodes = decode(img)
    current_time = time.time()

    for barcode in barcodes:
        myData = barcode.data.decode("utf-8")
        
        if myData not in detected_barcodes and (current_time - last_detection_time >= detection_interval):
            if myData in barcode_database:
                name = barcode_database[myData]
                color = (0, 0, 255)

                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, color, 5)
                pts2 = barcode.rect
                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                scan_count += 1
                current_date = datetime.now().strftime("%Y-%m-%d")
                current_time_str = datetime.now().strftime("%H:%M:%S")

                next_row = len(sheet.col_values(1)) + 1  

                sheet.update_cell(next_row, 1, next_row - 1)  
                sheet.update_cell(next_row, 2, name)  
                sheet.update_cell(next_row, 3, current_date)  
                
                if scan_count % 2 == 1:  
                    sheet.update_cell(next_row, 4, current_time_str)  
                    sheet.update_cell(next_row, 5, '')  
                else:  
                    sheet.update_cell(next_row, 5, current_time_str)  

                detected_barcodes.add(myData)
                last_detection_time = current_time

    if current_time - last_detection_time >= detection_interval:
        detected_barcodes.clear()  

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    ax.clear()
    ax.imshow(img_rgb)
    ax.axis('off')  
    plt.pause(0.001)  

cap.release()
plt.ioff()  
plt.show()
