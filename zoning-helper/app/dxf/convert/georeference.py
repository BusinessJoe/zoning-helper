import numpy as np


def add_column(array, val=1):
    """
    Appends a column of a single value to a 2d array and returns the
    result. Default fill value is 1.
    """
    result = np.full((array.shape[0], array.shape[1] + 1), fill_value=val, dtype=float)
    result[:, :-1] = array
    return result


def from_unit_square(bottom_left, top_left, bottom_right):
    """
    Returns an affine transformation from a square containing the points
    (0, 0), (0, 1), (1, 0) and (1, 1)
    to the rectangle defined by the three input points.
    """
    top_left = np.array(top_left)
    bottom_right = np.array(bottom_right)
    bottom_left = np.array(bottom_left)

    x_vector = bottom_right - bottom_left
    y_vector = top_left - bottom_left

    A = np.eye(3)
    A[:2, 0] = x_vector
    A[:2, 1] = y_vector

    # Offset is bottom_left
    A[:2, 2] = bottom_left

    return A


def solve_affine(source_coords, dest_coords):
    """Creates an affine transformation from source_coords to dest_coords"""
    D = from_unit_square(*source_coords)
    M = from_unit_square(*dest_coords)

    A = M.dot(np.linalg.pinv(D))

    return A.T


def transform_from_csv(csv_path):
    """
    Return an affine transform from a set of source coordinates to 
    destination coordinates. The names of the columns don't matter, but
    their content should be <source_x, source_y, dest_x, dest_y>.
    """
    with open(csv_path) as csv_file:
        csv = np.loadtxt(csv_file, delimiter=',')

    source_coords = csv[:, :2]
    dest_coords = csv[:, 2:4]

    Aff = solve_affine(source_coords[:3], dest_coords[:3])
    return Aff

