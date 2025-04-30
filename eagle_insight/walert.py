import pywhatkit as kit

def send_whatsapp_alert(number,info,google_maps_link):
    kit.sendwhatmsg_instantly(
        message = f"🚨 Stolen Vehicle Alert! Vehicle {info} detected at {google_maps_link}",
        phone_no=number, 
        wait_time=10,  # Wait time before sending
        tab_close=True
    )

# Example Usage
# send_whatsapp_alert(number="+918791733065",info='UP81X7833',google_maps_link='https://www.google.com/maps?q=78.64,66.55')
