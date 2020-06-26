from unittest import TestCase
import numpy as np

from .. import compile_dxf

np.random.seed(27042002)

class TestMapTransform(TestCase):
    unitsquare = np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]])

    def test_random_transform_accuracy(self):
        bottom_left = np.random.rand(2) * 200 - 100
        x_vector = np.random.rand(2) * 200 - 100
        y_vector = np.random.rand(2) * 200 - 100

        bottom_right = bottom_left + x_vector
        top_left = bottom_left + y_vector
        top_right = bottom_left + x_vector + y_vector

        A = compile_dxf.from_unit_square(bottom_left, top_left, bottom_right)

        expected = np.vstack((bottom_left, bottom_right, top_left, top_right))
        results = self.unitsquare.dot(A.T)[:, :2]

        self.assertTrue(np.allclose(expected, results))

    def test_multiple_transform_accuracy(self):
        for i in range(100):
            self.test_random_transform_accuracy()
