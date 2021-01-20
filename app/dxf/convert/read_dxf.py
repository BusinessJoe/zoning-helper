import os
import json
import glob
import re
import ezdxf
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from .georeference import transform_from_csv, add_column
from ..models import GeoJsonFeature


def remove_json_files(path):
    """
    Removes all the files with a .json extension in the target directory
    """
    files = glob.glob(os.path.join(path, '*.json'))
    for f in files:
        os.remove(f)


class Region:
    """Represents a single zone on the map

    The points representing the border of the zone are stored with a
    Polygon which allows holes to be present in the zone.
    """

    def __init__(self, points, text_segments=None, parent_area=''):
        self._polygon = Polygon(points)

        if text_segments is None:
            text_segments = []
        self.text_segments = text_segments

        self.parent_area = parent_area

    @property
    def text(self):
        """Return text ordered by height along an axis defined by the text's rotation"""
        # create rotation matrix to align text
        angle = self.text_segments[0].dxf.rotation
        c, s = np.cos(angle), np.sin(angle)
        rot = np.array([[c, s], [-s, c]])

        self.text_segments.sort(key=lambda t: rot.dot(tuple(t.dxf.insert)[:2])[1], reverse=True)
        return ' '.join(text.dxf.text for text in self.text_segments)

    def add_text(self, dxf_text):
        self.text_segments.append(dxf_text)

    @property
    def codes(self):
        p = re.compile(r'(?<!Part\s)\d+[A-Z]?')
        codes = re.findall(p, self.text)
        return codes

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

    def save_as_geojson(self, zone_id, bylaw_type):
        """Saves a geojson Polygon object to the specified file"""

        # reverse points along coordinate axis because geojson uses longitude-latitude ordering
        exterior = [(p[1], p[0]) for p in self.exterior]
        interiors = [[(p[1], p[0]) for p in i] for i in self.interiors]

        coordinates = [exterior] + interiors

        # round coordinates to 7 decimal places
        # this still has a precision of ~1 cm
        coordinates = [[(round(p[0], 7), round(p[1], 7)) for p in coordinates[0]]]

        geometry = {
            "type": "Polygon",
            "coordinates": coordinates,
        }
        properties = {
            "zone_spec": self.text,
            "codes": self.codes,
            "area": self.parent_area,
            "zone_id": zone_id,
            "bylaw_type": bylaw_type,
        }
        geojson = GeoJsonFeature(type='Feature', geometry=geometry, properties=properties)
        geojson.save()


def _perforate(base, cutout):
    return Polygon(base.exterior, list(base.interiors) + [cutout.exterior])


class DxfReader:
    def __init__(self, filename, area, spec_line_layer, spec_text_layer, exc_line_layer, exc_text_layer):
        self.doc = ezdxf.readfile(filename)
        self.area = area

        pre, ext = os.path.splitext(filename)
        csv_path = pre + '.csv'
        self.georef_transform = transform_from_csv(csv_path)

        self.spec_regions = self._get_regions(spec_line_layer, spec_text_layer)
        self.exc_regions = self._get_regions(exc_line_layer, exc_text_layer)

        self._transform_regions(self.spec_regions)
        self._transform_regions(self.exc_regions)

    def _get_regions(self, line_layer, text_layer):
        msp = self.doc.modelspace()
        polylines = msp.query(f'LWPOLYLINE[layer=="{line_layer}"]')
        dxf_text = msp.query(f'TEXT[layer=="{text_layer}"]')

        regions = [Region(points=line.vertices(), parent_area=self.area) for line in polylines if len(line) >= 3]

        for r in regions:
            poly = r.polygon
            if not poly.is_valid:
                print("Found an invalid polygon")
                # show_polygon(poly)

        # cut out nested regions
        for base in regions:
            for cutout in regions:
                # if base.polygon.is_valid and cutout.polygon.is_valid:
                if base is not cutout and base.polygon.contains(cutout.polygon):
                    polygon = _perforate(base.polygon, cutout.polygon)
                    base.polygon = polygon

        # add text to regions
        for region in regions:
            for text in dxf_text:
                # text.dxf.insert is the bottom left point of a text object
                # tuple conversion is required as the insert object doesn't allow slice indexing
                point = Point(tuple(text.dxf.insert)[:2])
                if region.polygon.contains(point):
                    region.add_text(text)

        # filter out regions without text
        for r in regions:
            if not len(r.text_segments):
                print("A region has no text")
        regions = [r for r in regions if len(r.text_segments)]

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

    def save_geojson(self, bylaw_type):
        """Save all regions as geojson using their save_as_geojson method"""
        regions = {'spec': self.spec_regions,
                   'exc': self.exc_regions}[bylaw_type]

        # for r in regions:
        #    if r.text == '':
        #        print(r)

        print(f'Saving {len(regions)} regions.')
        for idx, region in enumerate(regions):
            region.save_as_geojson(idx, bylaw_type)
