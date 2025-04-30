import cv2
import imutils
import numpy as np
import requests
from django.http import StreamingHttpResponse

harscade = r"D:\project\django project\eagle1\eagle_insight\haarcascade_russian_plate_number.xml"
min_area = 500

def cap():
    """Capture and stream processed video with number plate detection"""
    
    plate_cascade = cv2.CascadeClassifier(harscade)  # Load classifier once

    while True:
        # success, img = cam.read()
        images = requests.get("http://192.168.2.100:8080/shot.jpg")
        vedionp = np.array(bytearray(images.content),dtype=np.uint8)
        ved = cv2.imdecode(vedionp,-1)
        img = imutils.resize(ved,width=1000)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > min_area:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, 'Number Plate Detected', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

                # Extract Region of Interest (ROI)
                img_roi = img[y:y + h, x:x + w]
                gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
                thres = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
                image = imutils.resize(thres, width=500)

                # Save detected plate image
                # cv2.imwrite(r'D:\project\django project\eagle1\eagle_insight\media\plates\1.png',image)

        # Encode processed frame
        _, buffer = cv2.imencode('.jpg', img)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        

def stream_processed_video(request):
    """Django view to stream processed video frames"""
    return StreamingHttpResponse(cap(), content_type='multipart/x-mixed-replace; boundary=frame')
            