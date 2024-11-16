from twipfr import FLADocument
from helper import list_o_svgs_to_html
import os
# to fix:
# /PonyTemplate►Wings/PonyTemplate►Front Wing.xml
# PonyTemplate►Side Wing Front.xml
# idk the path isn't even connected for these 2, I can't fix that
# work on this later ig 
# PonyTemplate►FrontLegHoof.xml minor issues

# BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/" # /PonyTemplate►Wings
# testdocs = os.listdir("assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/")
# for name in testdocs:
#     doc = FLADocument(BASE_DIR+name)
#     frame = doc.draw_spritesheet(240,960)
#     html = list_o_svgs_to_html(frame)
#     old_html = open("src/cache/"+name[:-4]+".html", 'r').read()
#     if html!=old_html: print(name)
# BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/" # /PonyTemplate►Wings
# testdocs = os.listdir("assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts")
# testdocs.remove("PonyTemplate►Wings")
# ignore = [
#     "PonyTemplate►BackLeg0-8.xml",
#     "PonyTemplate►BackLeg2-8.xml",
#     "PonyTemplate►BackLeg4-8.xml",
#     "PonyTemplate►BackLeg5-8.xml",
#     "PonyTemplate►BackLeg6-8.xml",
#     "PonyTemplate►BackLeg7-8.xml",
#     "PonyTemplate►BackLeg8-8.xml",
#     "PonyTemplate►FrontLeg1-4.xml",
#     "PonyTemplate►FrontLeg2-4.xml",
#     "PonyTemplate►FrontLeg3-4.xml",
#     "PonyTemplate►FrontLegFront.xml",
# ]
# for name in testdocs:
#     if name not in ignore:
#         doc = FLADocument(BASE_DIR+name)
#         frame = doc.draw_spritesheet(240,960)
#         html = list_o_svgs_to_html(frame)
#         old_html = open("src/cache/"+name[:-4]+".html", 'r').read()
#         if html!=old_html: print(name)


# BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/" # /PonyTemplate►Wings
# testdocs = os.listdir("assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/PonyTemplate►Wings/")
# for name in testdocs:
#     doc = FLADocument(BASE_DIR+name)
#     frame = doc.draw_spritesheet(240,960)
#     open("src/cache/"+name[:-4]+".html", 'w').write(list_o_svgs_to_html(frame))
# BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/" 
# ignore = [
#     "PonyTemplate►BackLeg0-8.xml",
#     "PonyTemplate►BackLeg2-8.xml",
#     "PonyTemplate►BackLeg4-8.xml",
#     "PonyTemplate►BackLeg5-8.xml",
#     "PonyTemplate►BackLeg6-8.xml",
#     "PonyTemplate►BackLeg7-8.xml",
#     "PonyTemplate►BackLeg8-8.xml",
#     "PonyTemplate►FrontLeg1-4.xml",
#     "PonyTemplate►FrontLeg2-4.xml",
#     "PonyTemplate►FrontLeg3-4.xml",
#     "PonyTemplate►FrontLegFront.xml",
# ]
# testdocs = os.listdir("assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts")
# testdocs.remove("PonyTemplate►Wings")
# for name in testdocs:
#     if name not in ignore:
#         doc = FLADocument(BASE_DIR+name)
#         frame = doc.draw_spritesheet(240,960)
#         open("src/cache/"+name[:-4]+".html", 'w').write(list_o_svgs_to_html(frame))

BASE_DIR = "assets/base/LIBRARY/PonyTemplate►/PonyTemplate►BodyParts/"
doc = FLADocument(BASE_DIR+"PonyTemplate►Cover.xml")
frame = doc.draw_spritesheet(240,960)
open("test.html", 'w').write(list_o_svgs_to_html(frame))
