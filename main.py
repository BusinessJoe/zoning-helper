from convert import read_dxf as rdxf


if __name__ == '__main__':
    reader = rdxf.DxfReader("convert/ccrest_marked.dxf", 'cliffcrest', 'z_regions', 'z_standards', 'exc_regions', 'exc_standards')
    reader.save_geojson('spec', 'app/static/geojson/specifications')
    reader.save_geojson('exc', 'app/static/geojson/exceptions')
