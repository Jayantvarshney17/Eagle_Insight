import geocoder
from geopy.geocoders import Nominatim
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import beepy
import time
import winsound
from datetime import datetime

#-> beep
# Frequency and duration of the beep
frequency = 1000  # Frequency in Hertz
duration = 2000    # Duration in milliseconds
# Make a beep sound

end_time = time.time() + 5
# <- beep

# Function to get current location
def get_current_location():
    g = [27.877771, 78.083264]  # Uses your IP address to get an approximate location
    return g

# Function to create a Google Maps URL
def create_google_maps_link(latitude, longitude):
    return f"https://www.google.com/maps?q={latitude},{longitude}"

# Function to send an email with the location link
def send_email(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # TLS port

    # Sender email credentials (Replace with your credentials)
    sender_email = "dheerajvarshney74@gmail.com"
    sender_password = "bibf nsig edqh tgmy"  # Use an App Password for security
    
    try:
        # Set up the email structure
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))  # Email body

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)  # Login
        server.send_message(msg)  # Send email
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send(text,em):
    coordinates = get_current_location()
    
    if coordinates:
        latitude, longitude = coordinates
        google_maps_link = create_google_maps_link(latitude, longitude)
        # print(f"Google Maps Link: {google_maps_link}")
        
        # Email details
        current_time = datetime.now()
        subject = f"Your Vehicle {text} Found At This Location on {current_time.strftime('%H:%M:%S')}"
        body = f"Here is your vehicle current location: {google_maps_link}"
        to_email = em
        
        # Send the email
        send_email(to_email,subject, body)
        # print("Email with Google Maps link sent successfully!")
    else:
        print("Unable to retrieve location.")

# ## <- testing 
# nump = "UP81BX6915"
# num = "UP81BX6915"
# ## -> testing 

# # Main program
# if nump==num:
#     while time.time() < end_time:
#         beepy.beep(sound=1)
#     send()
        
# coordinates = get_current_location()
    
# if coordinates:
#     latitude, longitude = coordinates
#     google_maps_link = create_google_maps_link(latitude, longitude)
#     print(f"Google Maps Link: {google_maps_link}")