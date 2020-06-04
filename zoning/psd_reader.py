import itertools
import numpy as np
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

    x = np.append(x, np.ones((num_points, 1)), axis=1)
    y = np.append(y, np.ones((num_points, 1)), axis=1)

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
        print("Searching:", zone.name)
        array = np.array(zone.composite())
        alpha = array[..., 3]
        #print(np.where(alpha != 0))
        if alpha[tuple(image_coords)] != 0:
            yield zone.name
            print("---Found match")


psd = PSDImage.open("cliffcrest/Cliffcrest Sch A.psd")
size = psd.size

zone_layers = []
coord_layers = []
for idx, layer in enumerate(psd):
    # sort layer into appropriate list
    if layer.name.startswith('#'):
        continue
    elif layer.name.startswith('@'):
        coord_layers.append(layer)
    else:
        zone_layers.append(layer)

# Calculate affine transformation
print("Calculating affine transformation")
map_space = []
world_space = []
for layer in coord_layers:
    world_coord = name_to_world_coord(layer.name)
    world_space.append(world_coord)

    #print(layer)

    # convert to numpy array
    arr = np.array(layer.composite())
    # find the center of the dot based on alpha values
    alpha = arr[..., 3]
    center = ndimage.measurements.center_of_mass(alpha)
    map_space.append(center)

    #print(center)

A = solve_affine(map_space, world_space)
invA = np.linalg.pinv(A)
#print(map_space)
#print(world_space)


matches = list(get_zoning_spec((43.723637, -79.235022), invA, zone_layers))

print("All matches:", matches)
