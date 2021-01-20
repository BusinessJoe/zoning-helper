from django.contrib import admin
from .models import BylawException, BylawSpecification, GeoJsonFeature

# Register your models here.
admin.site.register(BylawSpecification)
admin.site.register(BylawException)
admin.site.register(GeoJsonFeature)
