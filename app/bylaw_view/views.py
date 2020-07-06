import os
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader


def bylaw_from_id(zone_type, area, bylaw_id):
    with open(f'static/bylaws/{zone_type}/{area}/{bylaw_id}.json') as f:
        return json.load(f)

def zone_from_id(zone_type, area, zone_id):
    with open(f'static/geojson/{zone_type}/{zone_id}.json') as f:
        return json.load(f)

def bylaw(request, zone_type, area, zone_id):
    print(request)

    zone = zone_from_id(zone_type, area, zone_id)
    print(zone)
    
    standard = zone['zone_spec']
    codes = zone['codes']

    if zone_type == 'specifications':
        return specifications(request, area, standard, codes)
    elif zone_type == 'exceptions':
        return exceptions(request, area, standard, codes)
    else:
        pass
    return HttpResponse(None)

def specifications(request, area, standard, codes):
    print(request)

    bylaws = [bylaw_from_id('specifications', area, bylaw_id) for bylaw_id in codes]

    template = loader.get_template('bylaw_view/specifications.html')
    context = {
        'standard': standard,
        'bylaws': bylaws,
    }
    return HttpResponse(template.render(context, request))


def exceptions(request, area, standard, codes):
    print(request)

    bylaws = [bylaw_from_id('exceptions', area, bylaw_id) for bylaw_id in codes]

    template = loader.get_template('bylaw_view/exceptions.html')
    context = {
        'standard': standard,
        'bylaws': bylaws,
    }
    return HttpResponse(template.render(context, request))
