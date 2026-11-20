# Silhouet van de geoglief (naar de luchtfoto en de hanger in ../referenties), 64x64-raster, 8x.
from PIL import Image, ImageDraw
S=8; im=Image.new('RGB',(64*S,64*S),'white'); d=ImageDraw.Draw(im)
def e(b,f='black'): d.ellipse([v*S for v in b],fill=f)
def r(b,f='black'): d.rectangle([v*S for v in b],fill=f)
def l(pts,w): d.line([(x*S,y*S) for x,y in pts],fill='black',width=int(w*S),joint='curve')
e((20,2,44,24))                 # grote ronde kop
r((26,20,38,46))                # lange smalle romp, breed aan de kop vast
l([(27,27),(16,29),(15,12)],4)  # arm omhoog, hand naast de kop
e((12,6,19,14))                 # hand
l([(37,27),(45,42)],4)          # arm omlaag, schuin naar buiten
e((43,39,49,46))                # hand
l([(29,45),(28,57)],4.5); l([(35,45),(37,57)],4.5)  # benen
e((21,54,31,61)); e((34,54,44,61))                   # ronde voeten
for cx,cy in ((27,12),(37,12)):  # ogen als cirkels
    e((cx-5,cy-5,cx+5,cy+5),'white'); e((cx-3,cy-3,cx+3,cy+3))
im.save('silhouet_r1.png')
