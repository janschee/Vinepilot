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
    
    #Place points in reference to the center
    new_order: list = [[]]*4
    for p in points[0]:
        is_left: bool =   p[0] < center[0]
        is_upper: bool =  p[1] < center[1]
        if is_upper and is_left: new_order[0]= p; continue
        if not is_upper and is_left: new_order[1] = p; continue
        if not is_upper and not is_left: new_order[2] = p; continue
        if is_upper and not is_left: new_order[3] = p; continue
    
    #TODO: Check if all point are correct!
    assert [] not in new_order, "Fatal! Point not set!"
    return new_order

def check_points(idx: int, points: list) -> bool:
    valid: bool = True
    if len(points) != 4: logging.error(f"Sample {idx}: Expected 4 points but got {len(points)}!"); valid = False
    if points[0][0] == None: logging.error(f"Sample {idx}: No annotations available!"); valid = False
    if valid: logging.debug(f"Sample {idx}: Points are valid!")
    return valid


