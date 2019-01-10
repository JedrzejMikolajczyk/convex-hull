from math import sqrt
#it is assumed that 
#x axis goes from left to right
#y axis goes from top to bottom
def _quick_sort(tab, A):
    if len(tab) <= 1:
        return tab
    value = tab[0][A]
    less = []
    equal = []
    more = []
    for i in tab:
        if i[A] < value:
            less.append(i)
        elif i[A] == value:
            equal.append(i)
        elif i[A] > value:
            more.append(i)
   
    return _quick_sort(less, A) + equal + _quick_sort(more, A)

def _create_linear_function(p1, p2):#p1,p2 - 2dimensional points [x, y]
    def linear_function(x):
        a = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b = p2[1] - a * p2[0]
        return a * x + b
    return linear_function

def _a_and_b_of_linear_function(p1, p2):#p1,p2 - 2dimensional points [x, y]
    a = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p2[1] - a * p2[0]
    return a, b

def _filter(setOfPoints, p1, p2, function, direction):# finds points that are above (and on) or below (and on) a linear function
    newSet = []
    if direction == "down":
        for point in setOfPoints:
            if point[1] >= function(point[0]) and p1[0] < point[0] < p2[0]:
                newSet.append(point)
    elif direction == "up":
        for point in setOfPoints:
            if point[1] <= function(point[0]) and p1[0] < point[0] < p2[0]:
                newSet.append(point)
    return newSet

def _convex_hull(setOfPoints, p1, p2, direction):#returns "upper" or "lower" part of the convex hull
    setOfPoints = _filter(setOfPoints, p1, p2, _create_linear_function(p1, p2), direction)
    if len(setOfPoints) <= 1:#if there is only one point beyond the line then it must a part of the convex hull
        return setOfPoints

    a, b = _a_and_b_of_linear_function(p1, p2)#if there are more points then the one that is furthest away from the line must be a part of the convx hull
    furthestPoint = []
    distance = 0

    for point in setOfPoints:
        d = abs(a * point[0] - point[1] + b) / sqrt(a * a + 1)
        if d >= distance:
            distance = d
            furthestPoint = point
    return  _convex_hull(setOfPoints, p1, furthestPoint, direction) + [furthestPoint] + _convex_hull(setOfPoints, furthestPoint, p2, direction)  

def convex_hull_clockwise(points):#takes a list of points in a two-dimensional space and returns their convex hull in clockwise order; sample input = [[0,23], [14, 56]]
    points = _quick_sort(points, 0)
    start = points[0]
    end = points[len(points) - 1]
    START =[]#a set of all points whose X is minimal
    END =[]#a set of all points whose X is maximal
    for point in points:
        if point[0] == start[0]:
            START.append(point)
        else:
            break

    for i in range(len(points) - 1, 0, -1):
        if points[i][0] == end[0]:
            END.append(points[i])
        else:
            break

    START = _quick_sort(START, 1)#points are sorted by y
    END = _quick_sort(END, 1)

    hull = START[::-1] + _convex_hull(points, START[0], END[0], "up") + END + (_convex_hull(points, START[-1], END[-1], "down")[::-1])
    return(hull)