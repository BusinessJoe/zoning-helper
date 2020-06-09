import json
from osgeo import gdal
import utm
import rasterio
from rasterio.features import shapes
from pprint import pprint

def tiff_to_geojson(filename, json_filename):
    with rasterio.open(filename) as src:
        mask = src.dataset_mask()
        image = src.read(4)
        results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for s, v
            in shapes(image, mask=mask, transform=src.transform))

    geometry = list(results)
    if len(geometry) != 1:
        raise RuntimeError

    with open(json_filename, 'w') as f:
        json.dump(geometry[0]['geometry'], f)

if __name__ == '__main__':
    tiff_to_geojson("zone.tif", "geoJSON.txt")
