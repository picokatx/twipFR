from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from consts import SYMBOLS, Edge, Point, StrokeStyle, Path, Shape, DrawCommand, FillStyle
import re
import numpy as np
from helper import xml_find_prepend, xml_findall_prepend, decode_fla_value
import drawsvg as dw
from path import findContours, find_subpaths, disjoint_path_join, reverse_draw_commands, addEdgeToGroup
from path import draw_path, draw_paths, find_subpaths, addEdgeToGroup, reverse_draw_commands, findContours, disjoint_path_join, crop_path, get_disjoint, closed
class FLADocument:
    def __init__(self, path: str) -> None:
        self.root  = ET.parse(path).getroot() # BASE_DIR+"PonyTemplate►3Q Front Wing.xml"
        layers = xml_find_prepend(self.root, ["timeline", "DOMTimeline", "layers"])
        anim_frames = {}
        # add option to split layers into separate animations because of wings
        for layer in reversed(layers):
            frames = xml_findall_prepend(layer, ["frames/"])
            for i, frame in enumerate(frames):
                index = int(frame.attrib["index"])
                if index not in anim_frames: anim_frames[index] = []
                elements = xml_findall_prepend(frame, ["elements/"])
                for element in elements:
                    if element.tag=="{http://ns.adobe.com/xfl/2008/}DOMShape":
                        anim_frames[index].append(self.DOMshape_parse(element))
                    if element.tag=="{http://ns.adobe.com/xfl/2008/}DOMGroup":
                        for member in xml_findall_prepend(element, ["DOMShape"]):
                            anim_frames[index].append(self.DOMshape_parse(member))
        self.animations = [v for k,v in sorted(anim_frames.items())]

    def transform_point(x, y, matrix):
        point = np.array([x, y, 1])
        transformed_point = matrix @ point
        return [transformed_point[0], transformed_point[1]]

    def pathstring_parse(self, pathstr: str, S: int, transformation_matrix: np.ndarray): 
        # tried applying transformation matrix here, but leads to inaccuracies so we do it natively instead
        c = 0
        code = []
        edge = pathstr
        prev_pos = None
        while c<len(edge):
            found_symbol = False
            for i in range(len(SYMBOLS)):
                out = re.match(SYMBOLS[i], edge[c:])
                if (out!=None):
                    found_symbol = True
                    if i!=3:
                        args = [decode_fla_value(c) for c in out.groups()]
                        if prev_pos!=args[-2:] or i!=0:
                            code.append(Edge(DrawCommand(i), args, S))
                        prev_pos = args[-2:]
                    else:
                        S = int(out.group(0)[1])
                    c+=out.span()[1]-out.span()[0]
                    break
            if not found_symbol:
                print(edge[c:c+50])
                break
        return S, code

    def DOMshape_parse(self, elm: Element):
        trans_pt_node = xml_find_prepend(elm, ["transformationPoint"])
        trans_pt = xml_find_prepend(trans_pt_node, ["Point"]) if trans_pt_node!=None else None
        trans_coords = Point(trans_pt.attrib['x'], trans_pt.attrib['y']) if trans_pt!=None else (-1, -1)
        
        # matrix
        matrix = xml_find_prepend(elm, ["matrix/"])
        transformation_matrix = None
        if matrix!=None:
            matargs = matrix.attrib
            a = matargs['a'] if 'a' in matargs else 1
            b = matargs['b'] if 'b' in matargs else 0
            c = matargs['c'] if 'c' in matargs else 0
            d = matargs['d'] if 'd' in matargs else 1
            tx = matargs['tx'] if 'tx' in matargs else 0
            ty = matargs['ty'] if 'ty' in matargs else 0

            transformation_matrix = np.array([
                [a, c, tx],
                [b, d, ty],
                [0, 0, 1]
            ], dtype=np.float64)

        # color palette
        fills = xml_findall_prepend(elm, ["fills/"])
        fill_dict = {0: None}
        for fill in fills:
            col = xml_find_prepend(fill, ["SolidColor"])
            fill_dict[fill.attrib["index"]] = FillStyle(
                col.attrib["color"] if "color" in col.attrib else "#000000",
                col.attrib["alpha"] if "alpha" in col.attrib else 1
            )

        # stroke
        strokes = xml_findall_prepend(elm, ["strokes/"])
        stroke_dict = {0: None}
        if strokes!=None:
            for stroke in strokes:
                temp = xml_find_prepend(stroke, ["SolidStroke"])
                stroke_dict[stroke.attrib["index"]] = StrokeStyle(
                    color=xml_find_prepend(temp, ["fill/"]).attrib["color"] if "color" in xml_find_prepend(temp, ["fill/"]).attrib else "#000000",
                    scaleMode=temp.attrib["scaleMode"],
                    caps=temp.attrib["caps"] if "caps" in temp.attrib else None,
                    weight=temp.attrib["weight"] if "weight" in temp.attrib else 0,
                    joints=temp.attrib["joints"] if "joints" in temp.attrib else None,
                    miterLimit=temp.attrib["miterLimit"] if "miterLimit" in temp.attrib else None
                )
        # paths
        edges = xml_findall_prepend(elm, ["edges/"])
        paths = []
        hints = [] # not using hints cubics for now
        S = 0
        for edge in edges:
            if "edges" in edge.attrib:
                fill0 = fill_dict[edge.attrib["fillStyle0"] if "fillStyle0" in edge.attrib else 0]
                fill1 = fill_dict[edge.attrib["fillStyle1"] if "fillStyle1" in edge.attrib else 0]
                stroke_col = stroke_dict[edge.attrib["strokeStyle"] if "strokeStyle" in edge.attrib else 0]
                S, temp = self.pathstring_parse(edge.attrib["edges"].replace("\n", "").strip(), S, transformation_matrix)
                paths.append(Path(temp, stroke_col, fill0, fill1))
            else:
                hints.append(edge.attrib["cubics"])
        return Shape(fill_dict, trans_coords, transformation_matrix, paths)
    
    def draw_frame(self, frame: int, offset: int, size: int):
        d = dw.Drawing(size, size, id_prefix='pic', origin=(-offset, -offset))
        for shape in self.animations[frame]:
            edgeGroups = {}
            split_paths = []
            
            for path in shape.paths:
                split_paths.extend(find_subpaths(path))

            for path in split_paths:
                if path.fill0 != None: addEdgeToGroup(edgeGroups, path.fill0,  path)
                if path.fill1 != None: addEdgeToGroup(edgeGroups, path.fill1, reverse_draw_commands(path))
            filledRegs = {}
            for fillStyle, group in edgeGroups.items():
                filledRegs[fillStyle] = findContours(group, fillStyle)


            for fillStyle, group in filledRegs.items():
                # need to merge fills down to single path
                a = findContours([path for path in group], fillStyle)
                ret = a[0]
                for i in range(1, len(a)):
                    ret = disjoint_path_join(ret, a[i])
                filledRegs[fillStyle] = [ret]

            for fillStyle, contours in filledRegs.items():
                for contour in contours:
                    transform = None
                    if type(shape.trans_mat)==np.ndarray:
                        tm = shape.trans_mat
                        tm_a = tm[0][0]
                        tm_b = tm[1][0]
                        tm_c = tm[0][1]
                        tm_d = tm[1][1]
                        tm_tx = tm[0][2]
                        tm_ty = tm[1][2]
                        transform = f"matrix({tm_a} {tm_b} {tm_c} {tm_d} {tm_tx} {tm_ty})"
                    stroke = contour.stroke if contour.stroke!=None else StrokeStyle(None, None, None, 0, None, None)
                    tracer = dw.Path(fill=fillStyle.color, opacity=fillStyle.alpha, stroke=stroke.color, stroke_width=stroke.weight, stroke_linecap="butt", stroke_linejoin=stroke.joints, stroke_miterlimit=stroke.miterLimit, transform=transform)
                    for edge in contour.edges:
                        if edge.type==DrawCommand.MOVETO:
                            tracer.M(edge.data[0], edge.data[1])
                        if edge.type==DrawCommand.LINETO:
                            tracer.L(edge.data[0], edge.data[1])
                        if edge.type==DrawCommand.QUADRATICTO:
                            tracer.Q(edge.data[0], edge.data[1], edge.data[2], edge.data[3])
                    d.append(tracer)
        return d
    
    def draw_spritesheet(self, offset: int, size: int):
        anim = dw.FrameAnimation()
        for frame in range(len(self.animations)):
            anim.append_frame(self.draw_frame(frame, offset, size))
        return [anim.frames[i].as_svg() for i in range(len(anim.frames))]