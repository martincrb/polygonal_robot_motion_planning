import math

def is_right_turn(p, q, r):
    return orientation2D(p, q, r) < 0

def convex_hull(points):
    c_hull = []
    n = len(points)
    left_most = min(points, key= lambda x: x[0])
    l = points.index(left_most)
    p = l
    q = None
    while True:
        c_hull.append(points[p])
        q = (p+1)%n
        for i in range(n):
            if (orientation2D(points[p], points[i], points[q]) == -1):
                q = i
        p = q
        if (p == l): break
    return c_hull

def mink_sum(A, B):
    C = []
    ref_point = A.getRefPoint()
    for a in A.vertices:
        aa = [a[0] - ref_point[0], a[1] - ref_point[1]]
        for b in B.vertices:
            point = (b[0] + aa[0], b[1] + aa[1])
            C.append(point)
    return C

def point_in_polygon(point, poly):
    n = len(poly.vertices)
    inside = False
    p1 = poly.vertices[0]
    p1 = list(p1)
    for i in range(n+1):
        p2 = poly.vertices[i%n]
        p2 = list(p2)
        if point[1] > min([p1[1], p2[1]]):
            if point[1] <= max([p1[1], p2[1]]):
                if point[0] <= max([p1[0], p2[0]]):
                    if p1[1]!= p2[1]:
                        xinters = (point[1]-p1[1])*(p2[0]-p1[0])/(p2[1]-p1[1])+p1[0]
                    if p1[0] == p2[0] or point[0] <= xinters:
                        inside = not inside
        p1[0] = p2[0]
        p1[1] = p2[1]
    return inside

def midpoint_in_polygon(edge, poly):
    if edge in poly.edges:  return False
    midx = (edge[0][0] + edge[1][0])/2.0
    midy = (edge[0][1] + edge[1][1])/2.0
    midpoint = (midx, midy)
    return point_in_polygon(midpoint, poly)


def is_on(a, b, c):
    "Return true iff point c intersects the line segment from a to b."
    # (or the degenerate case that all 3 points are coincident)
    return (collinear(a, b, c)
            and (within(a[0], c[0], b[0]) if a[0] != b[0] else
                 within(a[1], c[1], b[1])))

def collinear(a, b, c):
    "Return true iff a, b, and c all lie on the same line."
    return (b[0] - a[0]) * (c[1] - a[1]) == (c[0] - a[0]) * (b[1] - a[1])

def within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p


def angle(center, point):
    d = (point[0] - center[0], point[1] - center[1])
    if d[0] == 0:
        if d[1] < 0:
            return math.pi * 3 / 2
        else:
            return math.pi / 2
    if d[1] == 0:
        if d[0] < 0:
            return math.pi
        else:
            return 0
    if d[0] < 0:
        return math.pi + math.atan(d[1] / d[0])
    if d[1] < 0:
        return 2 * math.pi + math.atan(d[1] / d[0])
    return math.atan(d[1] / d[0])


def overlap(p, q, r):
    return q[0] < max([p[0], r[0]]) and q[0] > min([p[0], r[0]]) and q[1] < max([p[1],r[1]]) and q[1] > min([p[1],r[1]])

def edge_intersect(p, q, edge):
    p1 = p
    p2 = q
    q1 = edge[0]
    q2 = edge[1]
    ts1 = orientation2D(q1, q2, p1)
    ts2 = orientation2D(q1, q2, p2)
    ts3 = orientation2D(p1, p2, q1)
    ts4 = orientation2D(p1, p2, q2)
    if ts1 != ts2 and ts3 != ts4: return True
    elif ts1 == 0 and overlap(q1, p1, q2) or ts2 == 0 and overlap(q1, p2, q2) or ts3 == 0 and overlap(p1, q1, p2) or ts4 == 0 and overlap(p1,q2,p2):
        return True
    else: return False

def orientation2D(p, q, r):
    area = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    if area != 0:
        if area < 0: area = -1
        if area > 0: area = 1
    return area

def ccw(p, edge, q):
    if edge[0] == q:
        angle_dif = angle(p, edge[1]) - angle(p, q)
    else:
        angle_dif = angle(p, edge[0]) - angle(p, q)
    if angle_dif < 0:
        angle_dif += 2 * math.pi
    return angle_dif < math.pi


def euclidean_distance(p, q):
    return math.sqrt(math.pow(p[0] - q[0], 2) + math.pow(p[1] - q[1], 2))


def edge_distance(p, q, edge):
    if edge[0][0] == edge[1][0]:
        if p[0] == q[0]:
            return 0
        p_slope = (p[1] - q[1]) / (p[0] - q[0])
        intersection_x = edge[0][0]
        intersection_y = p_slope * (intersection_x - p[0]) + p[1]
        intersect = (intersection_x, intersection_y)
        return euclidean_distance(intersect, p)

    if p[0] == q[0]:
        e_slope = (edge[0][1] - edge[1][1]) / (edge[0][0] - edge[1][0])
        intersection_x = p[0]
        intersection_y = e_slope * (intersection_x - edge[0][0]) + edge[0][1]
        intersect = (intersection_x, intersection_y)
        return euclidean_distance(intersect, p)

    edge_slope = (edge[0][1] - edge[1][1]) / (edge[0][0] - edge[1][0])
    points_slope = (p[1] - q[1]) / (p[0] - q[0])

    if edge_slope == points_slope:
        return 0

    intersection_x = (edge_slope * edge[0][0] - points_slope * p[0] + p[1] - edge[0][1]) / (edge_slope - points_slope)
    intersection_y = edge_slope * (intersection_x - edge[0][0]) + edge[0][1]
    intersect = (intersection_x, intersection_y)
    return euclidean_distance(intersect, p)
