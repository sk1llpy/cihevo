from django.contrib import admin
from django.contrib.auth.models import User, Group
from cities_light.models import City, Region, Country, SubRegion

try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
    
    admin.site.unregister(City)
    admin.site.unregister(Region)
    admin.site.unregister(Country)
    admin.site.unregister(SubRegion)
except admin.sites.NotRegistered:
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ("name_ascii", "country__name")

    def has_module_permission(self, request):
        return False
