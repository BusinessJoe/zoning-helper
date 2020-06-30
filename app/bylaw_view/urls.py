from django.urls import path
  
from . import views

urlpatterns = [
    path('specification/<slug:area>/<slug:code>', views.specifications, name='specifications'),
    path('exception/<slug:area>/<slug:code>', views.exceptions, name='exceptions'),
]

