from django.urls import path
  
from . import views

urlpatterns = [
    path('<zone_type>/<area>/<int:zone_id>', views.bylaw, name='bylaw'),
    #path('specification/<slug:area>/<slug:code>', views.specifications, name='specifications'),
    #path('exception/<slug:area>/<slug:code>', views.exceptions, name='exceptions'),
]

