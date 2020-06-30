import os
import json
import glob
import ezdxf
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from georeference import transform_from_csv, add_column


def remove_json_files(path):
    """
    Removes all the files with a .json extension in the target directory
    """
    files = glob.glob(os.path.join(path, '*.json'))
    for f in files:
        os.remove(f)


class Region:
    def __init__(self, points, text_segments=None, area='no-area'):
        self._polygon = Polygon(points)

        if text_segments is None:
            text_segments = []
        self.text_segments = text_segments

        self.area = area

    @property
    def text(self):
        return ''.join(text.dxf.text for text in self.text_segments)

    def add_text(self, dxf_text):
        self.text_segments.append(dxf_text)

    @property
    def exterior(self):
        return list(self._polygon.exterior.coords)

    @property
    def interiors(self):
        return [list(i.coords) for i in self._polygon.interiors]

    @property
    def polygon(self):
        return self._polygon

    @polygon.setter
    def polygon(self, polygon):
        self._polygon = polygon

    def save_as_geojson(self, filename):
        # reverse along coordinate axis because geojson uses longitude-latitude ordering
        exterior = [(p[1], p[0]) for p in self.exterior]
        interiors = [[(p[1], p[0]) for p in i] for i in self.interiors]

        coordinates = [exterior] + interiors

        with open(filename, 'w') as json_file:
            data = {"zone_spec": self.text,
                    "area": self.area,
                    "type": "Polygon",
                    "coordinates": coordinates}
            json.dump(data, json_file)


class DxfReader:
    def __init__(self, filename, area, spec_line_layer, spec_text_layer, exc_line_layer, exc_text_layer):
        self.doc = ezdxf.readfile(filename)
        self.area = area

        self.spec_regions = self._get_regions(spec_line_layer, spec_text_layer)
        self.exc_regions = self._get_regions(exc_line_layer, exc_text_layer)

        pre, ext = os.path.splitext(filename)
        csv_path = pre + '.csv'
        self.georef_transform = transform_from_csv(csv_path)

        self._transform_regions(self.spec_regions)
        self._transform_regions(self.exc_regions)

    def _perforate(self, base, cutout):
        return Polygon(base.exterior, list(base.interiors) + [cutout.exterior])

    def _get_regions(self, line_layer, text_layer):
        msp = self.doc.modelspace()
        polylines = msp.query(f'LWPOLYLINE[layer=="{line_layer}"]')
        dxf_text = msp.query(f'TEXT[layer=="{text_layer}"]')

        regions = [Region(points=line.vertices(), area=self.area) for line in polylines]

        for base in regions:
            for cutout in regions:
                if base is not cutout and base.polygon.contains(cutout.polygon):
                    polygon = self._perforate(base.polygon, cutout.polygon)
                    base.polygon = polygon

        for region in regions:
            for text in dxf_text:
                # text.dxf.insert is the bottom left point of a text object
                point = Point(text.dxf.insert[:2])
                if region.polygon.contains(point):
                    region.add_text(text)

        return regions

    def _transform_points(self, points):
        points = np.array(points)
        transformed_points = add_column(points).dot(self.georef_transform)[:, :2]
        return transformed_points.tolist()

    def _transform_regions(self, regions):
        for r in regions:
            exterior = self._transform_points(r.exterior)
            interiors = [self._transform_points(i) for i in r.interiors]
            r.polygon = Polygon(exterior, interiors)

    def save_geojson(self, bylaw_type, path):
        regions = {'spec': self.spec_regions,
                  'exc' : self.exc_regions}[bylaw_type]

        remove_json_files(path)
        print(f'Saving {len(regions)} regions.')
        for idx, region in enumerate(regions):
            filename = os.path.join(path, f'{idx}.json')
            region.save_as_geojson(filename)

if __name__ == '__main__':
    reader = DxfReader("convert/ccrest_marked.dxf", 'cliffcrest', 'z_regions', 'z_standards', 'exc_regions', 'exc_standards')
    reader.save_geojson('spec', 'app/static/geojson/specifications')
    reader.save_geojson('exc', 'app/static/geojson/exceptions')
