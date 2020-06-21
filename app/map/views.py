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
    spec_path = 'static/geojson/specifications/'
    except_path= 'static/geojson/exceptions/'
    
    spec_zones = []
    except_zones = []
    
    for filename in os.listdir(spec_path):
        with open(os.path.join(spec_path, filename)) as f:
            spec_zones.append(json.load(f))

    for filename in os.listdir(except_path):
        with open(os.path.join(except_path, filename)) as f:
            except_zones.append(json.load(f))

    return JsonResponse({'specifications': spec_zones, 'exceptions': except_zones}, safe=False)

