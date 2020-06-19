from django.urls import path
  
from . import views

urlpatterns = [
    path('<slug:code>', views.bylaws, name='bylaws'),
]

