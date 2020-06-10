import json
import glob 
import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def load_maps():

    geojson = []
    for filename in glob.iglob('zoning/geojson/*.json'):
        with open(filename) as f:
            geojson.append(json.load(f))

    #with open('templates/static.html', 'w') as f:
    #    f.write(render_template('pymap.html', zones=geojson))
    return render_template('pymap.html', zones=geojson)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
