from convert import read_dxf as rdxf
from convert import read_docx as rdocx


if __name__ == '__main__':
    docx = rdocx.DocxBylawReader('convert/CCREST.docx', 'cliffcrest')
    docx.save_bylaws('spec', 'app/static/bylaws/specifications')
    docx.save_bylaws('exc', 'app/static/bylaws/exceptions')

    dxf = rdxf.DxfReader("convert/ccrest_marked.dxf", 'cliffcrest', 'z_regions', 'z_standards', 'exc_regions', 'exc_standards')
    dxf.save_geojson('spec', 'app/static/geojson/specifications')
    dxf.save_geojson('exc', 'app/static/geojson/exceptions')
