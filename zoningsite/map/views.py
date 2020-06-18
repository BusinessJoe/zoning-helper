import os
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader

def map_view(request):
    template = loader.get_template('map/map_view.html')
    context = {
        'category': 'CC',
        'bylaws': [{'context': 'context', 'code': 1234, 'text': 'hello world'}],
    }
    context = {}
    return HttpResponse(template.render(context, request))

def zones(request):
    print(request)
    geojson_path = 'static/geojson/specifications/'
    zones = []
    
    for filename in os.listdir(geojson_path):
        with open(os.path.join(geojson_path, filename)) as f:
            zones.append(json.load(f))

    return JsonResponse(zones, safe=False)

