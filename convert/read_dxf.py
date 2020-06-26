import ezdxf
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


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
    def __init__(self, filename, line_layer='ZONING_ZONES', text_layer='ZONING_STANDARDS'):
        self.doc = ezdxf.readfile(filename)
        msp = self.doc.modelspace()

        polylines = msp.query(f'LWPOLYLINE[layer=="{line_layer}"]')
        dxf_text = msp.query(f'TEXT[layer=="{text_layer}"]')
        
        self.regions = [Region(points=line.vertices()) for line in polylines]

        for region in self.regions:
            for text in dxf_text:
                point = Point(text.dxf.insert[:2])
                if region.contains(point):
                    region.add_text(text)


if __name__ == '__main__':
    reader = DxfReader("convert/CCREST_a_origin.dxf", line_layer='z_lukas')

    for idx, region in enumerate(reader.regions):
        path = f"app/static/geojson/specifications/{idx}.json"
        region.save_as_geojson(path)
