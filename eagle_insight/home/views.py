from django.shortcuts import render,redirect
from datetime import datetime
from home.models import Contact
from home.models import Off
from home.models import PassK
from home.models import User
from home.models import Ctheft
from home.models import DApi
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import VehicleEntry
from gmail import *
from gmailo import *
from plate1 import *

# <-- otp

from twilio.rest import Client
import random
from django.http import JsonResponse
# Twilio configuration (replace with your own credentials)
account_sid = 'AC364ddae3d91114105a7bd00f97a4bf6f'  # Replace with your Twilio Account SID
auth_token = '4a715f0e5d16cb6ab398d6c4b5385e00'    # Replace with your Twilio Auth Token
twilio_phone_number = '+19034378569'  # Replace with your Twilio Phone Number


client = Client(account_sid, auth_token)

# Temporary storage for OTPs
otp_store = {}

#--> otp

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def user(request):
    if request.method == 'POST':
        if "next" in request.POST:
            phone_number = request.POST.get('phone')
            off = User.objects.filter(mobile=phone_number).exists()
            if off:
                messages.warning(request,'User already exists')
            else:
                send_otp(phone_number)
                return render(request,'verify_otp.html',{'phone_number':phone_number})
        elif "eotp" in request.POST:
            phone_number = request.POST.get('phone_number')
            otp = request.POST.get('otp')
            if verify_otp(request,otp,phone_number):
                return render(request,'create_user.html',{'phone_number':phone_number})
            else:
                return render(request,'user.html')
        elif 'cu' in request.POST:
            mobile = request.POST.get('phone')
            name = request.POST.get('name')
            email = request.POST.get('email')
            passw = request.POST.get('pass')
            cpassw = request.POST.get('cpass')
            if passw == cpassw:
                    if User.objects.filter(name=name,email=email).exists():
                        messages.warning(request,'User already exists')
                    else:
                        off = User(name = name, email = email,mobile = mobile,password = passw,date = datetime.today())
                        off.save()
                        messages.success(request, "Your Account is Created")
            else:
                messages.warning(request,'Confirm Password is not Same as Password')
        elif 'lu' in request.POST:    
            # Handle Sign In
            email = request.POST.get("email")
            inpass = request.POST.get("pass")
            try:
                off = User.objects.get(email = email)
                stpass = off.password
                Name = {'O':off.name}
                def verify_password(stpass, inpass):
                    return check_password(stpass, inpass)
                if verify_password(inpass,stpass):
                    return render(request,'user_wel.html',Name)
                else:
                    messages.warning(request,"Invalid Credentials!")
            except:
                messages.warning(request,"Invalid Credentials!")
                return render(request,'user.html')
        elif 'theft' in request.POST:
            full_name = request.POST.get('name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone')
            vehicle_type= request.POST.get('vehicle_type')
            model= request.POST.get('model')
            number_pate= request.POST.get('number_plate')
            rc_no = request.POST.get('rc_number') or None
            vehicle_color = request.POST.get('color')
            date_of_theft = request.POST.get('stolen_date')
            fir_no = request.POST.get('fir_number')
            vehicle_image = request.FILES.get('vehicle_image') # image processing
            additional_information = request.POST.get('notes') or None
            
            if not rc_no:
                rc_no = "Not Provided"  # Set a default string or None

            if not vehicle_image:
                # If no image is provided, you can handle this by leaving the field empty (if allowed by model)
                vehicle_image = None

            if not additional_information:
                additional_information = "No additional information provided."
            
            if Ctheft.objects.filter(number_plate=number_pate,email=email).exists():
                messages.warning(request,'Fir is Already Exists')
            else:
                ctheft = Ctheft(owner_name=full_name,email=email,phone_number=phone_number,vehicle_type=vehicle_type,model_number=model,number_plate=number_pate,
                            rc_no=rc_no,vehicle_color=vehicle_color,date_of_theft=date_of_theft,fir_no=fir_no,
                            image=vehicle_image,additional_information=additional_information)
                ctheft.save()
                messages.success(request,'Your stolen vehicle report has been submitted successfully!.Please Check Email.')
                # send user
                send_email(request,fir_no)
                # send officer
                send_emailo(request,fir_no)
            return render(request,'user_wel.html',{'O':full_name})
    return render(request, 'user.html')

def officer_Owner(request):
    if request.method=="POST":
        if "sign_up" in request.POST:
            passk = request.POST.get('passk')
            name = request.POST.get('name')
            email = request.POST.get('email')
            passw = request.POST.get('pass')
            cpassw = request.POST.get('cpass')
            key = PassK.objects.all()
            for k in key:
                ke = k.PassKey
            if ke == passk:
                if passw == cpassw:
                    if Off.objects.filter(name=name,email=email).exists():
                        messages.warning(request,'Officer/Owner already exists')
                    else:
                        off = Off(name = name, email = email, password = passw,date = datetime.today())
                        off.save()
                        messages.success(request, "Your Account is Created")
                else:
                    messages.warning(request,'Confirm Password is not Same as Password')
            else:
                messages.warning(request,'Wrong PassKey')
    
        elif "sign_in" in request.POST:
            # Handle Sign In
            email = request.POST.get("email")
            inpass = request.POST.get("password")
            try:
                off = Off.objects.get(email = email)
                stpass = off.password
                vehicles = VehicleEntry.objects.all().order_by('-id')  # Newest entries at the top
                Name = {'O':off,'vehicles': vehicles}
                def verify_password(stpass, inpass):
                    return check_password(stpass, inpass)
                if verify_password(inpass,stpass):
                    return render(request,'oowel.html',Name)
                else:
                    messages.warning(request,"Invalid Credentials!")
            except:
                messages.warning(request,"Invalid Credentials!")
                return render(request,'officer_Owner.html')
        elif 'dd' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            inpass = request.POST.get('pass')
            if Off.objects.filter(name=name,email=email).exists():
                off = Off.objects.get(name=name,email = email)
                stpass = off.password
                vehicles = VehicleEntry.objects.all().order_by('-id')  # Newest entries at the top
                Name = {'O':off,'vehicles': vehicles}
                cth = Ctheft.objects.all()
                Name1 = {'O':off,'cth':cth}
                def verify_password(stpass, inpass):
                    return check_password(stpass, inpass)
                if verify_password(inpass,stpass):
                    return render(request,'checkscar.html',Name1)
                else:
                    messages.warning(request,"Invalid Credentials!")
                    return render(request,'oowel.html',Name)
                
        elif 'aa' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            inpass = request.POST.get('pass')
            if Off.objects.filter(name=name,email=email).exists():
                off = Off.objects.get(name=name,email = email)
                stpass = off.password
                vehicles = VehicleEntry.objects.all().order_by('-id')  # Newest entries at the top
                Name = {'O':off,'vehicles': vehicles}
                Name1 = {'O':off}
                def verify_password(stpass, inpass):
                    return check_password(stpass, inpass)
                if verify_password(inpass,stpass):
                    return render(request,'checkentry.html',Name)
                else:
                    messages.warning(request,"Invalid Credentials!")
                    return render(request,'oowel.html',Name)
        elif 'dapi' in request.POST:
            if request.method == 'POST':
                plate_number = request.POST.get('plate_number')
                if DApi.objects.filter(license_plate=plate_number).exists():
                    dapi = DApi.objects.get(license_plate=plate_number)
                    messages.warning(request, "⚠️ This data is shown for demonstration purposes only.")
                    return render(request, 'dapi.html',{'dapi':dapi})
                else:
                    messages.warning(request,'No Data Found')
                    return render(request,'dapi.html')
    
    return render(request, 'officer_Owner.html')

    
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name = name, email = email, phone = phone, desc = desc, date = datetime.today())
        contact.save()
        messages.success(request, "Your Query is Save.Thank You!")
    return render(request, 'cont.html')

def forgot(request):
    if request.method == 'POST':
        if "reset" in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            data = {'name':name,'email':email}
            if Off.objects.filter(name=name,email=email).exists():
                return render(request,'changep.html',data)
            else:
                messages.warning(request,'Invalid Credentials!!')
        elif "change" in request.POST:
            email1 = request.POST.get('email1')
            npass = request.POST.get('pass')
            ncpass = request.POST.get('cpass')
            if npass == ncpass:
                off = Off.objects.get(email=email1)
                off.password = npass
                off.save()
                messages.success(request,'your Password has been Updated')
                return render(request,'officer_Owner.html') 
            else :
                messages.warning(request,'Password do not Match')
            
    return render(request,'password_reset.html')

def forgotton(request):
    if request.method == 'POST':
        if "reset" in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            data = {'name':name,'email':email}
            if User.objects.filter(name=name,email=email).exists():
                return render(request,'changeu.html',data)
            else:
                messages.warning(request,'Invalid Credentials!!')
        elif "change" in request.POST:
            email1 = request.POST.get('email1')
            npass = request.POST.get('pass')
            ncpass = request.POST.get('cpass')
            if npass == ncpass:
                off = User.objects.get(email=email1)
                off.password = npass
                off.save()
                messages.success(request,'your Password has been Updated')
                return render(request,'user.html') 
            else :
                messages.warning(request,'Password do not Match')
            
    return render(request,'forget_password.html')


# Generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Send OTP to the phone number
def send_otp(phone_number):
        if phone_number:
            otp = generate_otp()
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"Your OTP code is: {otp}",
                from_=twilio_phone_number,
                to=phone_number
            )
            otp_store[phone_number] = otp
            return JsonResponse({"status": "success", "message_sid": message.sid})
        return JsonResponse({"status": "error", "message": "Phone number is required"})

# Verify the OTP
def verify_otp(request,otp,phone_number):
                actual_otp = otp_store.get(phone_number)
                if actual_otp == int(otp):
                    messages.success(request,'OTP Matched')
                    # messages.success(request,'!Account is Created!')
                    return True
                else:
                    messages.warning(request,'Invalid OTP')
                    return False


def get_status(request):
    if request.method== "POST":
        number_plate = request.POST.get('numberPlate')
        try:
            Vehicles= VehicleEntry.objects.get(plate_number=number_plate)
            cehicles= Ctheft.objects.get(number_plate=number_plate)
            # 
            return render(request, 'detailuser.html',{'Vehicles':Vehicles,'cehicles':cehicles})
        except:
            try:
                ct = Ctheft.objects.get(number_plate=number_plate)
                messages.info(request,'System is Processing.!!Please Wait For Response in Your Registered Gmail!!')
            except:
                messages.warning(request,'No Stolen Vehicle Data Found')  
    return render(request, 'getstat.html')


def live(request):
    return render(request,'live.html') 