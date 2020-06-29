import os
import json
import ezdxf
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from georeference import transform_from_csv, add_column


class Region:
    def __init__(self, points=None, text_segments=None):
        if points is None:
            points = []
        self._points = list(points)
        self.polygon = Polygon(self._points)

        if text_segments is None:
            text_segments = []
        self.text_segments = text_segments

    @property
    def text(self):
        return ''.join(text.dxf.text for text in self.text_segments)

    def add_text(self, dxf_text):
        self.text_segments.append(dxf_text)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = list(points)
        self.polygon = Polygon(self._points)

    def contains(self, point):
        return self.polygon.contains(point)

    def save_as_geojson(self, filename):
        points = self.points.copy()
        points.append(self.points[0])
        points = [(p[1], p[0]) for p in points]

        with open(filename, 'w') as json_file:
            data = {"zone_spec": self.text,
                    "type": "Polygon",
                    "coordinates": [points]}
            json.dump(data, json_file)


class DxfReader:
    def __init__(self, filename, spec_line_layer, spec_text_layer, exc_line_layer, exc_text_layer):
        self.doc = ezdxf.readfile(filename)

        self.spec_regions = self._get_regions(spec_line_layer, spec_text_layer)
        self.exc_regions = self._get_regions(exc_line_layer, exc_text_layer)

        pre, ext = os.path.splitext(filename)
        csv_path = pre + '.csv'
        self.georef_transform = transform_from_csv(csv_path)

        self._transform_regions(self.spec_regions)
        self._transform_regions(self.exc_regions)

    def _get_regions(self, line_layer, text_layer):
        msp = self.doc.modelspace()
        polylines = msp.query(f'LWPOLYLINE[layer=="{line_layer}"]')
        dxf_text = msp.query(f'TEXT[layer=="{text_layer}"]')

        regions = [Region(points=line.vertices()) for line in polylines]

        for region in regions:
            for text in dxf_text:
                point = Point(text.dxf.insert[:2])
                if region.contains(point):
                    region.add_text(text)

        return regions

    def _transform_regions(self, regions):
        for region in regions:
            points = np.array(region.points)
            transformed_points = add_column(points).dot(self.georef_transform)
            region.points = transformed_points.tolist()

    def save_specifications(self, path):
        for idx, region in enumerate(self.spec_regions):
            filename = os.path.join(path, f'{idx}.json')
            region.save_as_geojson(filename)

    def save_exceptions(self, path):
        for idx, region in enumerate(self.exc_regions):
            filename = os.path.join(path, f'{idx}.json')
            region.save_as_geojson(filename)

if __name__ == '__main__':
    reader = DxfReader("convert/ccrest_marked.dxf", 'z_regions', 'z_standards', 'exc_regions', 'exc_standards')
    reader.save_specifications('app/static/geojson/specifications')
    reader.save_exceptions('app/static/geojson/exceptions')
