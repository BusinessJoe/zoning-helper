from django.urls import path
  
from . import views

urlpatterns = [
    path('<slug:zone_type>/<slug:code>', views.bylaws, name='bylaws'),
]

