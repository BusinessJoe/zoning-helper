import os
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader

def bylaw_from_id(zone_type, bylaw_id):
    with open(f'static/bylaws/{zone_type}/{bylaw_id}.json') as f:
        return json.load(f)


def specifications(request, code):
    # parse code
    category, *bylaw_ids = code.split('-')

    bylaws = [bylaw_from_id('specifications', bylaw_id) for bylaw_id in bylaw_ids]

    template = loader.get_template('bylaw_view/specifications.html')
    context = {
        'standard': code,
        'category': category,
        'bylaws': bylaws,
    }
    return HttpResponse(template.render(context, request))


def exceptions(request, code):
    bylaw_ids = code.split(',')

    bylaws = [bylaw_from_id('exceptions', bylaw_id) for bylaw_id in bylaw_ids]

    template = loader.get_template('bylaw_view/exceptions.html')
    context = {
        'standard': code,
        'bylaws': bylaws,
    }
    return HttpResponse(template.render(context, request))
