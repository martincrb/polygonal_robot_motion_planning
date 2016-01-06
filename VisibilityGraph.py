import math
import GeoUtils
from Graph import Graph


def getAllVertices(S):
    r = []
    for poly in S:
        for v in poly.vertices:
            r.append(v)
    return r


def visibility_graph(S, start, goal):
    V = getAllVertices(S)
    V.append(start)
    V.append(goal)
    E = []
    for v in V:
        W = visible_vertices(v, S, start, goal)
        for w in W:
            E.append((v, w))
    Gvis = Graph()
    for v in V:
        Gvis.addVertex(v)
    for e in E:
        Gvis.addEdge(e[0], e[1])
        cost = GeoUtils.euclidean_distance(e[0],e[1])
        Gvis.addCost((e[0], e[1]), cost)
    return Gvis



def visible_vertices(p, S, start, goal):
    #NAIVE:
    V = getAllVertices(S)
    V.append(start)
    V.append(goal)
    V.remove(p)
    W = []
    for point in V:
        visible = True
        for poly in S:
            for edge in poly.edges:
                if p not in edge and point not in edge: #the two vertexs of the same edge can see each other, disjoint polygons
                    if GeoUtils.edge_intersect(p, point, edge): visible = False
                if p in poly.vertices and point in poly.vertices:
                    if GeoUtils.midpoint_in_polygon([p, point], poly): visible = False
        if visible:
            W.append(point)

    '''
    points = set([])
    for poly in S:
        for v in poly.vertices:
            points.add(v)
    points.add(start)
    points.add(goal)
    points.remove(p)
    points = list(points)

    points.sort(key=lambda x: angle(p, x))

    #Let l be the half-line parallel to the positive x-axis starting at p. Find
    #the obstacle edges that are properly intersected by l, and store them in a
    #balanced search tree T in the order in which they are intersected by l.
    T = AVLTree()

    all_edges = set()
    for poly in S:
        for edge in poly.edges:
            all_edges.add((edge[0], edge[1]))

    open_edges = []
    for edge in all_edges:
        if edge_intersect(p, points[0], edge):
            open_edges.append(edge)
    open_edges.sort(key=lambda x: edge_distance(p, points[0], x))

    for edge in open_edges:
        T.insert(edge, edge)
    W = []
    for next_point in points:
        if visible(p, points, next_point, T, S):
            W.append(next_point)
        for edge in all_edges:
            if next_point in edge and not ccw(p, edge, next_point):
                T.insert(edge, edge)
            if next_point in edge and ccw(p, edge, next_point):
                if T.__contains__(edge):
                    T.remove(edge)
    '''
    return W

def visible(p, points, q, T, S):
    if points.index(q) == 0:
        ant_point = None
    else:
        ant_point = points[points.index(q) - 1]
    for poly in S:
        if q in poly.vertices:
            for edge in poly.edges:
                if GeoUtils.edge_intersect(p, q, edge): return False
        elif ant_point == None or not GeoUtils.is_on(p, ant_point, q):
            for edge in poly.edges:
                found = T.min_item() == edge
                if found and GeoUtils.edge_intersect(p, q, edge): return False
                else: return True
        elif not visible(p, points, ant_point, T, S): return False
        else:
            for edge in T:
                if GeoUtils.edge_intersect(p, q, edge):
                    return False
                else: return True

