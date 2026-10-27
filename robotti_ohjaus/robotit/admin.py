from django.contrib import admin
from .models import Location, Robotti


class LocationInline(admin.TabularInline):
	model = Location
	extra = 0


@admin.register(Robotti)
class RobottiAdmin(admin.ModelAdmin):
	list_display = ('modelname', 'serialnumber')
	search_fields = ('modelname', 'serialnumber')
	inlines = (LocationInline,)
