from django.urls import path
  
from . import views

urlpatterns = [
    path('specifications/<slug:code>', views.specifications, name='specifications'),
    path('exceptions/<slug:code>', views.exceptions, name='exceptions'),
]

