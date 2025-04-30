from django.contrib import admin
from django.contrib import admin
from home.models import Contact
from home.models import Off
from home.models import DApi
from home.models import User
from home.models import PassK
from home.models import Ctheft
from home.models import VehicleEntry

# Register your models here.
admin.site.register(Contact)
admin.site.register(DApi)
admin.site.register(Off)
admin.site.register(PassK)
admin.site.register(User)
admin.site.register(Ctheft)
admin.site.register(VehicleEntry)
class VehicleEntryAdmin(admin.ModelAdmin):
     list_display = ('number_plate', 'vehicle_id', 'plate_image', 'car_image')

# Register your models here.