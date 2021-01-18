from django.http import JsonResponse
from .models import BylawSpecification, BylawException, GeoJsonFeature
from .serializers import SpecificationSerializer, ExceptionSerializer, GeoJsonSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def bylaw_specification(request, area, code):
    if request.method == 'GET':
        spec = BylawSpecification.objects.filter(area=area, code=code)[0]
        serializer = SpecificationSerializer(spec)
        return JsonResponse(serializer.data)


@csrf_exempt
def bylaw_exception(request, area, code):
    if request.method == 'GET':
        spec = BylawException.objects.filter(area=area, code=code)[0]
        serializer = ExceptionSerializer(spec)
        return JsonResponse(serializer.data)


@csrf_exempt
def geojson(request, area):
    if request.method == 'GET':
        geojsons = GeoJsonFeature.objects.filter(properties__area=area)
        serializer = GeoJsonSerializer(geojsons, many=True)
        return JsonResponse(serializer.data, safe=False)
