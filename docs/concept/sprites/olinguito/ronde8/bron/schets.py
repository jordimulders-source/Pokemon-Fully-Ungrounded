# Ruwe schetsen (alleen ter verkenning van pose/verhouding; niet het eindresultaat)
from PIL import Image, ImageDraw
import sys
D=(70,46,38); C=(222,200,156); K=(200,196,200); E=(20,14,14); N=(30,20,20); M=(30,22,24)
def base():
    im=Image.new('RGB',(64,64),(160,200,170)); return im, ImageDraw.Draw(im)
def claw(d,pts): d.polygon(pts,fill=K,outline=(90,90,96))
sk=[]
# A: zittend rechtop, klauwen omhoog naast de snoet (Drilbur-pose, maar klein)
im,d=base()
d.ellipse((34,38,58,50),fill=D)               # staart (ringen)
for x in (40,46,52): d.line((x,38,x+2,50),fill=C)
d.ellipse((20,32,46,60),fill=D)               # lijf
d.ellipse((24,40,40,58),fill=C)               # buik
d.ellipse((14,6,48,36),fill=D)                # kop
d.ellipse((16,4,24,12),fill=D); d.ellipse((38,3,46,11),fill=D)  # oren
d.polygon([(18,18),(4,24),(18,30)],fill=C)    # snoet
d.point((4,24),fill=N); d.point((5,24),fill=N)
d.polygon([(16,14),(44,14),(44,22),(16,22)],fill=M)  # masker
d.line((16,13,44,13),fill=C); d.line((16,23,44,23),fill=C)
d.ellipse((22,16,26,20),fill=E); d.ellipse((34,16,38,20),fill=E)
claw(d,[(14,36),(6,26),(10,24),(18,32)]); claw(d,[(44,36),(52,26),(56,30),(48,38)])
sk.append(im)
# B: op vier poten, snoet vooruit, een voorpoot opgeheven met klauw
im,d=base()
d.polygon([(48,40),(58,22),(62,26),(54,44)],fill=D)
for y in (28,34,40): d.line((50,y+4,60,y-2),fill=C)
d.ellipse((24,30,56,56),fill=D)
d.rectangle((28,48,34,60),fill=D); d.rectangle((44,48,50,60),fill=D)
d.ellipse((6,10,36,40),fill=D)
d.ellipse((8,8,15,15),fill=D); d.ellipse((26,7,33,14),fill=D)
d.polygon([(10,24),(0,30),(10,34)],fill=C); d.point((0,30),fill=N)
d.polygon([(8,20),(34,20),(34,26),(8,26)],fill=M)
d.ellipse((13,21,17,25),fill=E); d.ellipse((24,21,28,25),fill=E)
d.ellipse((12,36,26,48),fill=D)
claw(d,[(10,44),(4,52),(14,56),(18,48)])
claw(d,[(28,56),(24,62),(36,62),(34,56)])
sk.append(im)
# C: babyverhoudingen, rechtop staand, kop = helft van de hoogte, grote klauwen laag als 'wanten'
im,d=base()
d.polygon([(44,46),(60,30),(62,40),(50,54)],fill=D)
for x in (50,55): d.line((x,48-(x-44),x+3,52-(x-44)),fill=C)
d.ellipse((20,34,46,60),fill=D)
d.ellipse((26,40,40,58),fill=C)
d.ellipse((12,4,50,38),fill=D)
d.ellipse((14,2,23,11),fill=D); d.ellipse((40,2,49,11),fill=D)
d.polygon([(16,20),(2,26),(16,32)],fill=C); d.point((2,26),fill=N); d.point((3,26),fill=N)
d.polygon([(14,16),(48,16),(48,24),(14,24)],fill=M)
d.line((14,15,48,15),fill=C); d.line((14,25,48,25),fill=C)
d.ellipse((21,17,26,23),fill=E); d.ellipse((35,17,40,23),fill=E)
claw(d,[(14,42),(8,56),(16,58),(22,48)]); claw(d,[(40,44),(46,58),(54,56),(48,42)])
d.rectangle((24,58,30,62),fill=D); d.rectangle((36,58,42,62),fill=D)
sk.append(im)
S=4
out=Image.new('RGB',(64*S*3+16,64*S),(255,255,255))
for i,im in enumerate(sk): out.paste(im.resize((64*S,64*S),Image.NEAREST),(i*(64*S+8),0))
out.save(sys.argv[1])
