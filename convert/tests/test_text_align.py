from unittest import TestCase
from dataclasses import dataclass
from typing import List
import math

import numpy as np

from ..read_dxf import Region


@dataclass
class _dxf:
    """Dataclass to mimic a few elements of a text object's dxf class"""
    text: str
    insert: List[float]
    rotation: float

class SimpleText:
    """Mimics an ezdxf text object"""
    def __init__(self, text, origin, angle):
        self.dxf = _dxf(text, origin, angle)
        self.dxf.text = text
        self.dxf.rotation = angle
        self.dxf.insert = origin

class TestTextAlign(TestCase):
    def test_horizontal_text(self):
        """Assert non-rotated text is ordered correctly"""
        tri = [[0, 0], [0, 1], [1, 0]]
        r = Region(tri)

        r.add_text(SimpleText('top', [0, 1], 0))
        r.add_text(SimpleText('bot', [0, 0], 0))

        self.assertEqual(r.text, 'top bot')

    def test_upside_down_text(self):
        """Assert text rotated by 180 degrees is ordered correctly"""
        tri = [[0, 0], [0, 1], [1, 0]]
        r = Region(tri)

        r.add_text(SimpleText('top', [0, 0], math.pi))
        r.add_text(SimpleText('bot', [0, 1], math.pi))

        self.assertEqual(r.text, 'top bot')

    def test_tilted_text(self):
        """Assert text rotated by 45 degrees is ordered correctly"""
        tri = [[0, 0], [0, 1], [1, 0]]
        r = Region(tri)

        r.add_text(SimpleText('top', [-1 - 0.1, -1], math.pi/2))
        r.add_text(SimpleText('bot', [0, 0], math.pi/2))

        self.assertEqual(r.text, 'top bot')


