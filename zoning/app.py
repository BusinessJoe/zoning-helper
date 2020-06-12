import json
import glob 
import os
from flask import Flask, render_template
from whitenoise import WhiteNoise

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='assets/')
app.wsgi_app.add_files('assets/bylaws/', prefix='bylaw')

@app.route("/")
def load_maps():
    geojson = []
    for filename in glob.iglob('zoning/geojson/*.json'):
        with open(filename) as f:
            geojson.append(json.load(f))

    #with open('templates/static.html', 'w') as f:
    #    f.write(render_template('pymap.html', zones=geojson))
    return render_template('map.html', zones=geojson)

@app.route("/zone/<zoning_code>")
def show_bylaws(zoning_code):
    category = zoning_code.split('-')[0]
    codes = zoning_code.split('-')[1:]

    bylaw_dicts = []
    for code in codes:
        with open(f'assets/bylaws/{code}.json') as f:
            bylaw_json = json.load(f)
            bylaw_dicts.append(bylaw_json)

    return render_template('bylaw_display.html', category=category, bylaws=bylaw_dicts)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    app.run(host=host, port=port, debug=True)
