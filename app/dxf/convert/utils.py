import matplotlib.pyplot as plt
from shapely.validation import explain_validity


def show_polygon(polygon):
    print("Polygon")
    print(explain_validity(polygon))
    x, y = polygon.exterior.xy
    plt.plot(x, y)
    plt.axis('equal')
    plt.show()
