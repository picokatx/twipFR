from twipfr import FLADocument
from helper import list_o_svgs_to_html
import os
# to fix:
# /PonyTemplate►Wings/PonyTemplate►Front Wing.xml
# PonyTemplate►Side Wing Front.xml

# BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/" # /PonyTemplate►Wings
# testdocs = os.listdir("assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/")
# for name in testdocs:
#     doc = FLADocument(BASE_DIR+name)
#     frame = doc.draw_spritesheet(0,240,960)
#     html = list_o_svgs_to_html(frame)
#     old_html = open("src/cache/"+name[:-4]+".html", 'r').read()
#     if html!=old_html: print(name)

# BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/" # /PonyTemplate►Wings
# testdocs = os.listdir("assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/")
# for name in testdocs:
#     doc = FLADocument(BASE_DIR+name)
#     frame = doc.draw_spritesheet(240,960)
#     open("src/cache/"+name[:-4]+".html", 'w').write(list_o_svgs_to_html(frame))

BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/"
doc = FLADocument(BASE_DIR+"PonyTemplate►Front Wing.xml")
frame = doc.draw_spritesheet(240,960)
open("test.html", 'w').write(list_o_svgs_to_html(frame))
# open("test.html", 'w+').write(list_o_svgs_to_html([doc.draw_frame(1,7,240,960).as_svg()]))

