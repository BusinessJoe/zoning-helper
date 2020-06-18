import ezdxf
import itertools
import numpy as np
from PIL import Image, ImageDraw


class Line:
    def __init__(self, lineobj):
        self.lineobj = lineobj
        self.remove = False
        if type(lineobj) == ezdxf.entities.lwpolyline.LWPolyline:
            self.points = np.array(list(lineobj.vertices_in_wcs()))[:,:2]
            self.closed = lineobj.closed

        elif type(lineobj) == ezdxf.entities.line.Line:
            self.points = np.array([lineobj.dxf.start, lineobj.dxf.end])[:,:2]
            self.closed = False
        else:
            raise NotImplementedError(f'Cannot convert an object of type {type(lineobj)}.')

    def transform_points(self):
        mins = (1745963.938750, 4525380.046781)

        self.points -= mins

        self.points[:, 1] = 5000 - self.points[:, 1]

    def draw(self, draw_context):
        if self.closed:
            draw.polygon(list(self.points.flatten()), fill='blue', outline='red')
        else:
            color = tuple(np.random.choice(range(256), size=3))
            draw.line(list(self.points.flatten()), fill=color, width=5)

    def threshold_join_line(self, line, threshold=0):
        
        if not self.closed and not line.closed:
            if np.linalg.norm(self.points[0] - line.points[0]) <= threshold:
                self.points = np.append(self.points[::-1], line.points)
                line.remove = True
                return True
            if np.linalg.norm(self.points[0] - line.points[-1]) <= threshold:
                self.points = np.append(self.points[::-1], line.points[::-1])
                line.remove = True
                return True
            if np.linalg.norm(self.points[-1] - line.points[0]) <= threshold:
                self.points = np.append(self.points, line.points)
                line.remove = True
                return True
            if np.linalg.norm(self.points[-1] - line.points[-1]) <= threshold:
                self.points = np.append(self.points, line.points[::-1])
                line.remove = True
                return True
        return False
                    

doc = ezdxf.readfile("references/CCREST_a.dxf")
print([layer.dxf.name for layer in doc.layers])

msp = doc.modelspace()

entities = msp.query('*[layer=="ZONING_ZONES"]')


lines = []
for e in entities:
    line = Line(e)
    line.transform_points()

    lines.append(line)

print(len(lines))

# save lines before joining them
img = Image.new('RGB', (5000, 5000), color=(128, 128, 128))
draw = ImageDraw.Draw(img)
for idx, line in enumerate(lines):
    if not line.remove:
        line.draw(draw)
img.save('convert/joined.png')

# join lines
lines_mask = [True for _ in lines]
for idx, line in enumerate(lines):
    for idx2, line2 in enumerate(lines[idx+1:], idx+1):
        lines_mask[idx2] &= not line.threshold_join_line(line2, threshold=10)

#lines = list(itertools.compress(lines, lines_mask))
lines = [line for line in lines if not line.remove]
print(f'new len: {len(lines)}')

# save lines after joining
img = Image.new('RGB', (5000, 5000), color=(128, 128, 128))
draw = ImageDraw.Draw(img)
for idx, line in enumerate(lines):
    if not line.remove:
        line.draw(draw)
img.save('convert/joined.png')

