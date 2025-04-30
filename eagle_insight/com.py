from plate import * 
from loc1 import *
from loc0 import *
from walert import *
import cv2
from PIL import Image
import pytesseract
from playsound import playsound
import os
import django
import shutil


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NPDS.settings')
django.setup()

# Import Django models
from home.models import VehicleEntry
from home.models import Ctheft

# Specify the Tesseract executable path if it's not in PATH (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    # Load image using OpenCV
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to clean up the image
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Optionally, apply dilation/erosion to enhance text edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

    return processed_image

def extract_text(image_path):

    # Perform OCR on the image
    text = pytesseract.image_to_string(Image.open(image_path), lang="eng", config="--oem 3 --psm 6")
    return text

# Input image path

while True:
    cap()
    image_path = r"D:\project\django project\eagle1\eagle_insight\media\plates\1.png"  # Replace with your image file
    image_path1 = r"D:\project\django project\eagle1\eagle_insight\media\cars\1.png"  # Replace with your image file
    text = extract_text(image_path)
    info = ''.join(e for e in text if e.isalnum())
    print("Number is:",info)
    if info:
        target_directory = r"D:\project\django project\eagle1\eagle_insight\media\plates"
        target_directory1 = r"D:\project\django project\eagle1\eagle_insight\media\cars"
        # Define new image name in the target directory
        new_image = os.path.join(target_directory,f'{info}.png')
        shutil.copy(image_path,new_image)
        new_image1 = os.path.join(target_directory1,f'{info}.png')
        shutil.copy(image_path1,new_image1)
    
    if VehicleEntry.objects.filter(plate_number=info).exists():
        pass
    else:
        coordinates = get_current_location()
        print(coordinates)
        dates=datetime.now()
        if coordinates:
            latitude, longitude = coordinates
            google_maps_link = create_google_maps_link(latitude, longitude)
        if info:
            vehic = VehicleEntry(plate_number = info,plate_image = f"/plates/{info}.png",date_time=dates,car_image=f"/cars/{info}.png",current_location=google_maps_link)
            vehic.save()
        
    exists = Ctheft.objects.filter(number_plate=info).exists()
    if exists:
        tar_em = Ctheft.objects.get(number_plate=info)
        cemail = tar_em.email
        phone = tar_em.phone_number
     
    ## -> testing
    if info=="":
        while time.time() < end_time:
        # Play a warning sound file
            winsound.PlaySound("warning.wav", winsound.SND_FILENAME)
        
    if exists:
        winsound.Beep(frequency, duration)
        while time.time() < end_time:
            # beepy.beep(sound=1)
            winsound.Beep(frequency, duration)
        
        # Send Stolen detail to user
        send(text = info,em = cemail)
        
        coordinates = get_current_location()
        if coordinates:
            latitude, longitude = coordinates
            google_maps_link = create_google_maps_link(latitude, longitude)
            send_whatsapp_alert(phone,info,google_maps_link) # whatsapp Alert
        
        # Send Stolen detail to officer
        send0(text = info,em = ['dheerajvarshney89@gmail.com'])
        
      
cv2.destroyAllWindows()




