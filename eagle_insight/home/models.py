from django.db import models
from django.contrib.auth.hashers import make_password
import random
 
# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122) 
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()
def __str__(self):
    return self.name



class Off(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122) 
    password = models.CharField(max_length=12)
    date = models.DateField()
    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if not self.password.startswith('pbkdf2_'):  # Avoid re-hashing an already hashed password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class User(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122) 
    mobile =models.CharField(max_length=13)
    password = models.CharField(max_length=12)
    date = models.DateField()
    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if not self.password.startswith('pbkdf2_'):  # Avoid re-hashing an already hashed password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class PassK(models.Model):
    PassKey = models.CharField(max_length=10)

class Ctheft(models.Model):
    owner_name = models.CharField(max_length=122)
    phone_number= models.CharField(max_length=12)
    email = models.CharField(max_length=122,null=True)
    vehicle_type= models.CharField(max_length=122) 
    model_number= models.CharField(max_length=122) 
    number_plate= models.CharField(max_length=122)
    rc_no= models.CharField(max_length=122,null=True, blank=True)
    vehicle_color= models.CharField(max_length=122)
    date_of_theft= models.DateField()
    fir_no= models.CharField(max_length=122)
    image = models.ImageField(upload_to='images/',null=True, blank=True,default='Not Found')
    additional_information = models.TextField(null=True, blank=True)


def generate_vehicle_id():
    """Generate a random 4-digit vehicle ID."""
    return str()

class VehicleEntry(models.Model):
    vehicle_id = models.CharField(max_length=4, default=str(random.randint(1000, 9999)), unique=False)
    plate_image = models.ImageField(upload_to='plates/')
    plate_number = models.CharField(max_length=20)
    date_time = models.DateTimeField()  # Automatically set the date and time
    car_image = models.ImageField(upload_to='cars/')
    current_location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle_id} - {self.plate_number}"

class DApi(models.Model):
    license_plate = models.CharField(max_length=15, unique=True)
    owner_name = models.CharField(max_length=255)
    permanent_address = models.TextField()
    insurance_company = models.CharField(max_length=255)
    insurance_expiry = models.DateField()
    vehicle_class = models.CharField(max_length=50)
    registration_date = models.DateField()
    chassis_number = models.CharField(max_length=50)
    engine_number = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    cubic_capacity = models.PositiveIntegerField()
    cylinders = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    norms = models.CharField(max_length=50)
    rc_status = models.CharField(max_length=10, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')])

    def __str__(self):
        return self.license_plate
    