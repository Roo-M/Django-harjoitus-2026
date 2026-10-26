from django.contrib import admin
from .models import Robotti


@admin.register(Robotti)
class RobottiAdmin(admin.ModelAdmin):
	list_display = ('modelname', 'serialnumber', 'location_x', 'location_y')
	search_fields = ('modelname', 'serialnumber')
