import os
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader

def bylaw_from_id(bylaw_id):
    with open(f'static/bylaws/{bylaw_id}.json') as f:
        return json.load(f)

def bylaws(request, code):
    # parse code
    split_code = code.split('-')
    category = split_code[0]
    bylaw_ids = split_code[1:]

    bylaws = [bylaw_from_id(bylaw_id) for bylaw_id in bylaw_ids]

    template = loader.get_template('bylaw_view/bylaw_display.html')
    context = {
        'category': category,
        'bylaws': bylaws,
    }
    return HttpResponse(template.render(context, request))

