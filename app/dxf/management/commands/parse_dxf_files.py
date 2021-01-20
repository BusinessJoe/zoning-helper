from django.core.management.base import BaseCommand

from dxf.convert import read_dxf as rdxf
from dxf.convert import read_docx as rdocx


class Command(BaseCommand):
    def handle(self, *args, **options):
        docx = rdocx.DocxBylawReader('app/dxf/convert/CCREST.docx', 'cliffcrest')
        docx.save_bylaws('spec')
        docx.save_bylaws('exc')

        dxf = rdxf.DxfReader("app/dxf/convert/ccrest_marked.dxf",
                             'cliffcrest', 'z_regions', 'z_standards', 'exc_regions', 'exc_standards')
        dxf.save_geojson('spec')
        dxf.save_geojson('exc')
