import logging

def reorder_points(points: list) -> list:
    """
    @params:
    Takes a list of four points defining a polygon, where each point is described through [x,y] coordiantes.

    @return:
    Returns a sorted list of points, starting with the upper-left point and going in mathematicaly positiv direction.
    This gives the following order: [upper-left, lower-left, lower-right, upper-right]
    """

    #Calculate centroid (arithmetic mean)
    x_total: float = 0
    y_total: float = 0
    for p in points[0]: x_total += p[0]; y_total += p[1]
    center = (x_total/4, y_total/4)
    return center


def check_points(idx: int, points: list) -> bool:
    valid: bool = True
    if len(points) != 4: logging.error(f"Sample {idx}: Expected 4 points but got {len(points)}!"); valid = False
    if points[0][0] == None: logging.error(f"Sample {idx}: No annotations available!"); valid = False
    if valid: logging.debug(f"Sample {idx}: Points are valid!")
    return valid


