import itertools
import numpy as np
from osgeo import gdal, osr
from psd_tools import PSDImage
from PIL import Image
from scipy import ndimage


np.set_printoptions(suppress=True)


def name_to_world_coord(name):
    name = name.lstrip('@')
    name = name.split(', ')
    return tuple(map(float, name))


def solve_affine(map_space, world_space):
    num_points = len(map_space)

    x = np.array(map_space)
    y = np.array(world_space)

    x = np.hstack((x, np.ones((num_points, 1)) ))
    y = np.hstack((y, np.ones((num_points, 1)) ))

    A = np.dot(np.linalg.pinv(x), y)

    return A

def get_zoning_spec(geo_coords, trans_matrix, zone_list):
    geo_coords = np.array(geo_coords)
    if geo_coords.shape != (2,):
        raise ValueError(f"Expected shape (2,) but coordinates have shape {geo_coords.shape}")

    geo_coords = np.reshape(geo_coords, (1, 2))
    geo_coords = np.append(geo_coords, np.ones((1, 1)), axis=1)

    image_coords = (np.dot(geo_coords, trans_matrix)[0, :2]).astype(int)

    for zone in zone_list:
        print("Searching:", zone[0])
        array = np.array(zone[1])
        alpha = array[..., 3]
        #print(np.where(alpha != 0))
        if alpha[tuple(image_coords)] != 0:
            yield zone[0]
            print("---Found match")

def make_world_file(filename, matrix):
    A, B, C, D, E, F = tuple(matrix.T[:-1, :].flatten())

    with open(filename, 'w') as f:
        for value in A, D, B, E, C, F:
            f.write(str(value))
            f.write('\n')

def make_tiff_file(filename, zone, matrix):
    arr = np.array(zone[1])

    coords = np.argwhere(arr[..., -1] != 0)
    x_min, y_min = coords.min(axis=0)
    x_max, y_max = coords.max(axis=0)
    cropped = arr[x_min:x_max+1, y_min:y_max+1]

    nx, ny, _ = cropped.shape

    # find min and max latitude and longitude
    image_coords = np.array([[x_min, y_min, 1], [x_min, y_max, 1], [x_max, y_min, 1], [x_max, y_max, 1]])
    world_coords = np.dot(image_coords, matrix)[..., :2]
    lats = world_coords[:, 0]
    lons = world_coords[:, 1]

    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)

    #print(lat_min, lat_max)
    #print(lon_min, lon_max)

    x_res = (lon_max - lon_min) / nx
    y_res = (lat_max - lat_min) / ny

    #print(matrix.T[:2, :].flatten()[::-1])
    #print(lon_min, x_res, 0, lat_max, 0, -y_res)

    #geotransform = lon_min, x_res, 0, lat_max, 0, -y_res
    geotransform = lon_min, matrix[1, 1], matrix[0, 1], lat_max, matrix[1, 0], matrix[0, 0]

    dst_ds = gdal.GetDriverByName('GTiff').Create(filename, ny, nx, 4, gdal.GDT_Byte)

    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(3857)
    dst_ds.SetProjection(srs.ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(cropped[..., 0])
    dst_ds.GetRasterBand(2).WriteArray(cropped[..., 1])
    dst_ds.GetRasterBand(3).WriteArray(cropped[..., 2])
    dst_ds.GetRasterBand(4).WriteArray(cropped[..., 3])
    dst_ds.FlushCache()

def load_layers(psd):
    zone_layers = []
    coord_layers = []
    for idx, layer in enumerate(psd):
        # sort layer into appropriate list
        if layer.name.startswith('#'):
            continue
        elif layer.name.startswith('@'):
            coord_layers.append((layer.name, layer.composite()))
        else:
            zone_layers.append((layer.name, layer.composite()))
    return zone_layers, coord_layers

def calculate_affine_transformation(coord_layers):
    print("Calculating affine transformation")
    map_space = []
    world_space = []
    for layer in coord_layers:
        world_coord = name_to_world_coord(layer[0])
        world_space.append(world_coord)

        # convert to numpy array
        image = layer[1]
        arr = np.array(image)
        # find the center of the dot based on alpha values
        alpha = arr[..., 3]
        center = ndimage.measurements.center_of_mass(alpha)
        map_space.append(center)

    Aff = solve_affine(map_space, world_space)
    return Aff

if __name__ == '__main__':
    psd = PSDImage.open("cliffcrest/Cliffcrest Sch A.psd")
    size = psd.size

    zone_layers, coord_layers = load_layers(psd)

    # Calculate affine transformation
    Aff = calculate_affine_transformation(coord_layers)
    invAff = np.linalg.pinv(Aff)

    for i, layer in enumerate(zone_layers):
        # save layer as image
        image = layer[1]
        image.save(f"{i}.tif")
        make_world_file(f"{i}.tfw", Aff)

    make_tiff_file("zone.tif", zone_layers[0], Aff)

