import numpy as np
from psd_tools import PSDImage
from PIL import Image
from scipy import ndimage


def name_to_world_coord(name):
    name = name.lstrip('@')
    name = name.split(', ')
    return tuple(map(float, name))


def solve_affine(map_space, world_space):
    # TODO: work out linear algebra for this function
    num_points = len(map_space)

    x = np.array(map_space).T
    y = np.array(world_space).T

    x = np.vstack((x, np.ones(num_points)))
    y = np.vstack((y, np.ones(num_points)))

    A = np.dot(y, np.linalg.pinv(x))
    return A


psd = PSDImage.open("cliffcrest/Cliffcrest Sch A.psd")

zone_layers = []
coord_layers = []
for idx, layer in enumerate(psd):
    #print(layer)

    # sort layer into appropriate list
    if layer.name.startswith('@'):
        coord_layers.append(layer)
    else:
        zone_layers.append(layer)

    # convert to PIL Image
    #image = layer.composite()
    #image.save(f"cliffcrest/{idx}.png")

map_space = []
world_space = []
for layer in coord_layers:
    world_coord = name_to_world_coord(layer.name)
    world_space.append(world_coord)

    print(layer)

    # convert to numpy array
    arr = np.array(layer.composite())
    # find the center of the dot based on alpha values
    alpha = arr[..., 3]
    center = ndimage.measurements.center_of_mass(alpha)
    map_space.append(center)

print(map_space)
print(world_space)

A = solve_affine(map_space, world_space)

m = np.array([[2682], [2060], [1]])

print(np.dot(A, m))


#print(zone_layers)
#print(coord_layers)
