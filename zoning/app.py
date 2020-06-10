import json
import glob 
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def load_maps():

    geojson = []
    for filename in glob.iglob('geojson/*.json'):
        with open(filename) as f:
            geojson.append(json.load(f))

    #with open('templates/static.html', 'w') as f:
    #    f.write(render_template('pymap.html', zones=geojson))
    return render_template('pymap.html', zones=geojson)

if __name__ == '__main__':
    app.run(debug=True)
