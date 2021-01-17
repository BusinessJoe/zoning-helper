from django.http import JsonResponse
from .models import BylawSpecification, BylawException, GeoJson
from .serializers import SpecificationSerializer, ExceptionSerializer, GeoJsonSerializer


# Create your views here.
def bylaw_specification(request, area, code):
    if request.method == 'GET':
        spec = BylawSpecification.objects.filter(area=area, code=code)[0]
        serializer = SpecificationSerializer(spec)
        return JsonResponse(serializer.data)


def bylaw_exception(request, area, code):
    if request.method == 'GET':
        spec = BylawException.objects.filter(area=area, code=code)[0]
        serializer = ExceptionSerializer(spec)
        return JsonResponse(serializer.data)


def geojson(request, area):
    if request.method == 'GET':
        geojsons = GeoJson.objects.filter(data__area=area)
        serializer = GeoJsonSerializer(geojsons, many=True)
        return JsonResponse(serializer.data, safe=False)
