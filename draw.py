"""Render AEROLITH using only repeatable, antialiased Pillow geometry."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
SCALE = 3
im = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE))
d = ImageDraw.Draw(im)


def polygon(points, fill):
    d.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=fill)


def ellipse(box, fill):
    d.ellipse(tuple(round(v * SCALE) for v in box), fill=fill)


def line(points, fill, width=1):
    d.line([(round(x * SCALE), round(y * SCALE)) for x, y in points], fill=fill,
           width=round(width * SCALE), joint="curve")


def curve(start, segments):
    points = [start]
    for a, b, end in segments:
        x, y = points[-1]
        for i in range(1, 41):
            t = i / 40
            u = 1 - t
            points.append((u**3*x + 3*u*u*t*a[0] + 3*u*t*t*b[0] + t**3*end[0],
                           u**3*y + 3*u*u*t*a[1] + 3*u*t*t*b[1] + t**3*end[1]))
    return points


def cloud(start, segments, fill):
    polygon(curve(start, segments) + [(1100, 1100), (-100, 1100)], fill)


# A quiet vertical dawn, with no random texture or noise.
stops = [(0, (34, 39, 80)), (300, (106, 77, 113)),
         (580, (221, 144, 134)), (770, (249, 204, 148)),
         (1024, (248, 220, 171))]
for (y0, c0), (y1, c1) in zip(stops, stops[1:]):
    for y in range(y0 * SCALE, y1 * SCALE):
        t = (y / SCALE - y0) / (y1 - y0)
        c = tuple(round(a + (b - a) * t) for a, b in zip(c0, c1))
        d.line((0, y, SIZE * SCALE, y), fill=c)

CREAM = "#fff0d0"
# Typography belongs to the sky: measured individual glyphs, optically calm spacing.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 112 * SCALE)
title = "AEROLITH"
tracking = 13 * SCALE
widths = [d.textlength(c, font=font) for c in title]
x = (SIZE * SCALE - sum(widths) - tracking * (len(title) - 1)) / 2
for c, width in zip(title, widths):
    d.text((round(x), 91 * SCALE), c, font=font, fill=CREAM, anchor="lt")
    x += width + tracking
line([(127, 218), (897, 218)], "#e6c6b1", 1.5)

# The sun sits low behind the single island, its broad halo defined by flat discs.
ellipse((491, 351, 865, 725), "#e9a78a")
ellipse((509, 369, 847, 707), "#f0b18c")
ellipse((531, 391, 825, 685), "#f4ba88")
ellipse((553, 413, 803, 663), "#ef8d63")

# Distant wind ribbons keep the horizon spacious.
polygon(curve((-30, 621), [((96, 603), (159, 611), (249, 618)),
                           ((322, 621), (351, 610), (386, 614))])
        + [(290, 631), (-30, 633)], "#efc2a5")
polygon(curve((805, 642), [((875, 622), (977, 627), (1050, 639))])
        + [(1050, 650), (805, 648)], "#f5d0aa")

# Clean birds: asymmetric tapered wings, never a repeated font glyph.
for x, y, s in [(251, 330, 1.0), (289, 351, .68), (793, 290, .8), (824, 307, .52)]:
    polygon([(x-17*s, y-5*s), (x-7*s, y-4*s), (x, y+2*s),
             (x+10*s, y-7*s), (x+20*s, y-9*s), (x+10*s, y-2*s),
             (x, y+6*s), (x-8*s, y)], "#373e5a")

# A detached, inverted teardrop rock. Large facets make its depth legible.
polygon([(258, 465), (305, 449), (659, 442), (765, 463), (725, 523),
         (674, 563), (632, 641), (572, 688), (529, 731), (493, 697),
         (447, 669), (398, 598), (347, 567), (311, 513)], "#173f46")
polygon([(258, 465), (370, 485), (427, 549), (447, 669), (398, 598),
         (347, 567), (311, 513)], "#255658")
polygon([(370, 485), (504, 491), (477, 574), (493, 697), (447, 669),
         (427, 549)], "#1e4a4c")
polygon([(504, 491), (597, 483), (561, 591), (572, 688), (529, 731),
         (493, 697), (477, 574)], "#12363e")
polygon([(597, 483), (765, 463), (725, 523), (674, 563), (632, 641),
         (572, 688), (603, 573)], "#326460")
polygon([(710, 482), (744, 475), (717, 515), (680, 544)], "#6f8870")
polygon([(629, 552), (655, 534), (618, 613), (587, 654)], "#52796a")
polygon([(335, 494), (359, 510), (384, 561), (365, 546)], "#42716a")

# The green top is a single welcoming shelf, edged in dawn light.
polygon(curve((258, 465), [((310, 438), (388, 433), (451, 442)),
                           ((556, 422), (686, 435), (765, 463)),
                           ((676, 489), (563, 495), (458, 486)),
                           ((381, 492), (296, 479), (258, 465))]), "#56836b")
polygon(curve((283, 460), [((390, 443), (434, 451), (473, 452)),
                           ((576, 432), (677, 447), (738, 463)),
                           ((620, 477), (469, 470), (373, 475))]), "#769579")
line(curve((259, 465), [((383, 496), (633, 502), (765, 463))]), "#e5b778", 5)

# A pale footpath connects three cottages to the lighthouse.
polygon(curve((374, 465), [((420, 441), (535, 467), (591, 441)),
                           ((608, 430), (605, 421), (601, 410))])
        + [(608, 410)] + curve((608, 421), [((637, 460), (491, 468), (374, 469))]), "#d4bd88")


def cottage(x, y, w, h):
    polygon([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], "#f5ddb0")
    polygon([(x+w*.66, y), (x+w, y), (x+w, y+h), (x+w*.66, y+h)], "#c7ae83")
    polygon([(x-6, y+2), (x+w*.47, y-21), (x+w+6, y+2)], "#273f48")
    polygon([(x+w*.47, y-21), (x+w+6, y+2), (x+w*.68, y+2)], "#976c62")
    for wx in [x+8, x+w-15]:
        polygon([(wx, y+9), (wx+7, y+9), (wx+7, y+19), (wx, y+19)], "#ffc56e")
    polygon([(x+w*.45, y+h-17), (x+w*.45+7, y+h-17),
             (x+w*.45+7, y+h), (x+w*.45, y+h)], "#5d6f60")


cottage(342, 418, 53, 35)
cottage(421, 402, 59, 41)
cottage(667, 420, 44, 31)

# Lighthouse: the one tall landmark, facing the open cloud sea.
polygon([(566, 443), (580, 331), (605, 331), (619, 443)], "#fff0d0")
polygon([(596, 332), (605, 331), (619, 443), (600, 443)], "#d3b98c")
polygon([(576, 363), (609, 363), (613, 385), (573, 385)], "#28565a")
polygon([(587, 416), (597, 416), (597, 443), (587, 443)], "#22484e")
polygon([(576, 329), (576, 307), (608, 307), (608, 329)], "#ffe0a0")
line([(582, 308), (582, 329)], "#294951", 3)
line([(600, 308), (600, 329)], "#294951", 3)
polygon([(569, 307), (592, 289), (615, 307)], "#273f48")
line([(568, 332), (616, 332)], "#233f47", 5)
line([(570, 326), (570, 336), (614, 336), (614, 326)], "#294951", 2)
line([(592, 289), (592, 281)], "#273f48", 2)

# A narrow spring snakes through the rock and leaves its pointed tip.
polygon([(541, 503), (546, 546), (531, 595), (541, 637), (525, 687),
         (525, 729), (516, 782), (520, 855), (546, 855), (539, 785),
         (536, 730), (535, 689), (550, 639), (540, 594), (552, 547),
         (549, 503)], "#84c2b9")
polygon([(529, 725), (525, 782), (528, 849), (536, 849), (532, 785),
         (534, 725)], "#e2edce")

# Distant cloud sea, then broad pink undersides and luminous foreground crowns.
cloud((-80, 774), [((-10, 718), (42, 731), (79, 746)),
                   ((107, 688), (184, 688), (227, 734)),
                   ((273, 716), (313, 728), (332, 754)),
                   ((391, 700), (451, 731), (474, 768)),
                   ((525, 753), (563, 766), (595, 777)),
                   ((620, 726), (697, 708), (738, 744)),
                   ((779, 702), (835, 714), (862, 742)),
                   ((937, 705), (1022, 715), (1100, 765))], "#e7b6ae")
# The falling water stays in front of the distant clouds, then fades into cream mist.
polygon([(525, 729), (519, 775), (520, 811), (514, 835),
         (540, 837), (537, 805), (537, 775), (536, 729)], "#a6cfc1")
polygon([(529, 730), (525, 776), (527, 812), (524, 837),
         (533, 837), (531, 807), (532, 776), (534, 730)], "#e2edce")
ellipse((505, 825, 539, 849), "#ffe6bd")
ellipse((524, 821, 552, 849), "#ffe6bd")
cloud((-80, 813), [((-18, 756), (52, 754), (98, 796)),
                   ((118, 753), (186, 746), (232, 782)),
                   ((275, 760), (326, 772), (344, 807)),
                   ((411, 789), (461, 816), (472, 844)),
                   ((523, 818), (569, 824), (595, 849)),
                   ((634, 790), (697, 777), (748, 812)),
                   ((775, 757), (847, 754), (884, 796)),
                   ((953, 761), (1033, 779), (1100, 817))], "#ffe6bd")
cloud((-70, 909), [((0, 836), (85, 837), (136, 878)),
                   ((178, 825), (276, 826), (322, 887)),
                   ((366, 862), (421, 886), (445, 920)),
                   ((493, 861), (576, 855), (621, 906)),
                   ((682, 857), (774, 867), (811, 918)),
                   ((875, 859), (991, 859), (1090, 916))], "#dca9a6")
cloud((-70, 944), [((2, 871), (82, 874), (127, 916)),
                   ((177, 871), (251, 871), (299, 922)),
                   ((350, 904), (391, 921), (414, 952)),
                   ((455, 898), (536, 892), (582, 933)),
                   ((637, 914), (676, 924), (701, 953)),
                   ((753, 895), (837, 890), (888, 938)),
                   ((951, 913), (1028, 917), (1100, 948))], "#fff0d0")

im = im.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
target = Path("entry.png")
im.save(target, format="PNG", optimize=True)
print(f"Rendered {target}: {SIZE}x{SIZE}, {target.stat().st_size} bytes")
