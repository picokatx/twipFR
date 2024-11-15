from consts import Path, DrawCommand, Edge, StrokeStyle
from typing import List
import drawsvg as dw

def get_startpt(path: Path):
    return path.edges[0].data
def get_endpt(path: Path):
    if path.edges[-1].type == DrawCommand.QUADRATICTO:
        return path.edges[-1].data[2:]
    else:
        return path.edges[-1].data
def closed(path: Path):
    return get_startpt(path)==get_endpt(path)
def get_disjoint(path: Path):
    for i, edge in enumerate(path.edges):
        if edge.type == DrawCommand.MOVETO and i!=0:
            return i
    return False
def get_pt(edge):
    if edge.type == DrawCommand.MOVETO:
        return edge.data
    if edge.type == DrawCommand.LINETO:
        return edge.data
    if edge.type == DrawCommand.QUADRATICTO:
        return edge.data[2:]
def get_quad(edge):
    if edge.type == DrawCommand.MOVETO:
        return None
    if edge.type == DrawCommand.LINETO:
        return None
    if edge.type == DrawCommand.QUADRATICTO:
        return edge.data[:2]
def path_join(path1: Path, path2: Path):
    if get_endpt(path1)==get_startpt(path2):
        return Path(path1.edges+path2.edges[1:], path1.stroke, path1.fill0, path1.fill1)
    else:
        return None
def disjoint_path_join(path1: Path, path2: Path):
    return Path(path1.edges+path2.edges, path1.stroke, path1.fill0, path1.fill1)
def reverse_draw_commands(path: Path):
    edges = path.edges
    reversed_edges = [Edge(DrawCommand.MOVETO, get_pt(edges[-1]), edges[-1].S)]
    prev_quad = None
    prev_command = None
    endpt = get_pt(edges[-1])
    for edge in reversed(edges):
        endpt = get_pt(edge)
        if prev_command == DrawCommand.MOVETO:
            reversed_edges.append(Edge(DrawCommand.MOVETO, endpt, edge.S))
        elif prev_command == DrawCommand.LINETO:
            reversed_edges.append(Edge(DrawCommand.LINETO, endpt, edge.S))
        elif prev_command == DrawCommand.QUADRATICTO:
            reversed_edges.append(Edge(DrawCommand.QUADRATICTO, prev_quad+endpt, edge.S))
        prev_command = edge.type
        prev_quad = get_quad(edge)
    return Path(reversed_edges, path.stroke, path.fill1, path.fill0)
def addEdgeToGroup(edgeGroups,group,edge):
    if not group in edgeGroups: edgeGroups[group] = []
    edgeGroups[group].append(edge)

def findConnectedTo(prevEdge,edges):
    for i, edge in enumerate(edges):
        if get_startpt(edge) == get_endpt(prevEdge): return i, 1
        if get_endpt(edge) == get_startpt(prevEdge): return i, 2
    return -1, 0
# print(fill, contour.fill0, contour.fill1, group[at].fill0, group[at].fill1)
def find_loop_in_path(path: Path):
    for i in range(len(path.edges)):
        if get_startpt(path) == get_pt(path.edges[i]) and i!=0 and (i==len(path.edges)-1 or path.edges[i+1].type == DrawCommand.MOVETO):
            return i

def findContour(group: List[Path], fill):
    contour = group.pop(0)
    at, which = findConnectedTo(contour,group)
    while ((not closed(contour)) and len(group) > 0 and at != -1): # at != -1 is wrong, but temporary just to make error go away
        contour = path_join(contour, group[at]) if which==1 else path_join(group[at], contour)

        if (get_disjoint(contour) and closed(contour)): # reverse subpath if connected
            contour = Path(edges=contour.edges[get_disjoint(contour):]+contour.edges[1:get_disjoint(contour)], stroke=contour.stroke, fill0=contour.fill0, fill1=contour.fill1)
        else:
            # special case for /PonyTemplate►Wings/PonyTemplate►3Q Front Wing.xml
            loop_idx = find_loop_in_path(contour)
            dj = get_disjoint(crop_path(contour, 0, loop_idx))
            while loop_idx != None and dj:
                loop_idx = find_loop_in_path(contour)
                dj = get_disjoint(crop_path(contour, 0, loop_idx))
                if loop_idx != None and dj:
                    contour = Path(edges=contour.edges[dj:loop_idx+1]+contour.edges[1:dj]+contour.edges[loop_idx+1:], stroke=contour.stroke, fill0=contour.fill0, fill1=contour.fill1)
        
        group.pop(at)
        at, which = findConnectedTo(contour,group)
    
    return contour

def findContours(group: List[Path], fill):
    group = [path for path in group]
    contours = []
    while len(group) > 0:
        contours.append(findContour(group, fill))
    return contours

def find_subpaths(path: Path):
    paths = []
    start_pt = None
    old_i = 0
    for i, edge in enumerate(path.edges):
        end_pt = get_pt(edge)
        # if end_pt==[-7.0, 99.85]: print(i, edge, path)
        if start_pt==None:
            start_pt = get_pt(edge)
        elif end_pt==start_pt : #  or (edge.type==DrawCommand.MOVETO and i!=0)
            offset = i+1
            # if (edge.type==DrawCommand.MOVETO and i!=0): offset+=1
            paths.append(Path(path.edges[old_i:offset], path.stroke, path.fill0, path.fill1))
            old_i = offset
            start_pt = None
    if old_i!=i+1: paths.append(Path(path.edges[old_i:i+1], path.stroke, path.fill0, path.fill1))
    return paths

def draw_path(path: Path):
    d = dw.Drawing(960, 960, id_prefix='pic', origin=(-240, -240))
    stroke = path.stroke if path.stroke!=None else StrokeStyle(None, None, None, 0, None, None)
    tracer = dw.Path(fill='white', stroke="blue", stroke_width=3, stroke_linecap="butt", stroke_linejoin=stroke.joints, stroke_miterlimit=stroke.miterLimit, transform=None)
    for edge in path.edges:
        if edge.type==DrawCommand.MOVETO:
            tracer.M(edge.data[0], edge.data[1])
        if edge.type==DrawCommand.LINETO:
            tracer.L(edge.data[0], edge.data[1])
        if edge.type==DrawCommand.QUADRATICTO:
            tracer.Q(edge.data[0], edge.data[1], edge.data[2], edge.data[3])
    d.append(tracer)
    return d
def draw_paths(paths: List[Path]):
    d = dw.Drawing(960, 960, id_prefix='pic', origin=(-240, -240))
    for path in paths:
        stroke = path.stroke if path.stroke!=None else StrokeStyle(None, None, None, 0, None, None)
        tracer = dw.Path(fill='grey', stroke="blue", stroke_width=3, stroke_linecap="butt", stroke_linejoin=stroke.joints, stroke_miterlimit=stroke.miterLimit, transform=None)
        for edge in path.edges:
            if edge.type==DrawCommand.MOVETO:
                tracer.M(edge.data[0], edge.data[1])
            if edge.type==DrawCommand.LINETO:
                tracer.L(edge.data[0], edge.data[1])
            if edge.type==DrawCommand.QUADRATICTO:
                tracer.Q(edge.data[0], edge.data[1], edge.data[2], edge.data[3])
        d.append(tracer)
    return d
def crop_path(path: Path, start: int, end: int):
    return Path(path.edges[start:end], path.stroke, path.fill0, path.fill1)