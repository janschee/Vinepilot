
def reorder_points(points: list) -> list:
    """
    @params:
    Takes a list of four points defining a polygon, where each point is described through [x,y] coordiantes.
    
    @return:
    Returns a sorted list of points, starting with the upper-left point and going in mathematicaly positiv direction.
    This gives the following order: [upper-left, lower-left, lower-right, upper-right]
    """
   
   #Calculate centroid

