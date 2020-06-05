import json
from osgeo import gdal
import utm
import rasterio
from rasterio.features import shapes
from pprint import pprint

mask = None
with rasterio.open("zone.tif") as src:
    mask = src.dataset_mask()
    image = src.read(1) # first band
    results = (
        {'properties': {'raster_val': v}, 'geometry': s}
        for s, v
        in shapes(image, mask=mask, transform=src.transform))

geoms = list(results)

coords = geoms[0]['geometry']['coordinates'][0]

for idx, coord in enumerate(coords):
    pass
    #coords[idx] = utm.from_latlon(*coord)[:2]

pprint(geoms[0]['geometry']['coordinates'][0])

with open("geoJSON.txt", 'w') as f:
    json.dump(geoms[0]['geometry'], f)
print(len(geoms))
