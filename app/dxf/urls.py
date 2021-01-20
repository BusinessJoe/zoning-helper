from django.urls import path
from dxf import views

urlpatterns = [
    path('bylaw/spec/<area>/<code>/', views.bylaw_specification),
    path('bylaw/exc/<area>/<code>/', views.bylaw_specification),
    path('geojson/<area>/', views.geojson)
]
