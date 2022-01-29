from django.contrib import admin

from .models import CustomUser, CityModel

admin.site.register(CustomUser)
admin.site.register(CityModel)
