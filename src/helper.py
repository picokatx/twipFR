from xml.etree.ElementTree import Element
from typing import List

def xml_find_prepend(root: Element, path: List[str]):
    return root.find("/".join(".//{http://ns.adobe.com/xfl/2008/}"+p for p in path))
def xml_findall_prepend(root: Element, path: List[str]):
    return root.findall("/".join(".//{http://ns.adobe.com/xfl/2008/}"+p for p in path))
def decode_fla_value(val: str):
    if val[0]=="#":
        if len(val[1:].split(".")[1])==1: val = val[0]+"."+val[1:]+"0"
        hex_out = "".join(val[1:].split("."))
        out = int(hex_out, 16)
        if out >= 0x80000000:
            out = -(0xffffffff - out + 1)
        out = out / 256
    else:
        out = float(val) if "." in val else int(val)
    if (out>100000): print(val, out) # did we parse something wrong?
    return out / 20 # fla spec stores subpixels to 1/20 depth
def list_o_svgs_to_html(list_o_svgs: List[str]):
    out = ""
    out += '<!DOCTYPE html>\n'
    out += '<head>\n'
    out += '<meta charset="utf-8">\n'
    out += '</head>\n<body style="background-color:black">\n'
    for svg in list_o_svgs:
        out += svg
    out += '\n</body>\n</html>\n'
    return out