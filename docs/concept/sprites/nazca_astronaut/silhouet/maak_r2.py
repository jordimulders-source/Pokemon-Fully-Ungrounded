# Silhouet r2: langer (Jordi: "hij is toch langer?"); verhouding hoogte:breedte ±2:1 zoals op de luchtfoto.
from PIL import Image, ImageDraw
S=8; im=Image.new('RGB',(64*S,64*S),'white'); d=ImageDraw.Draw(im)
def e(b,f='black'): d.ellipse([v*S for v in b],fill=f)
def r(b,f='black'): d.rectangle([v*S for v in b],fill=f)
def l(pts,w): d.line([(x*S,y*S) for x,y in pts],fill='black',width=int(w*S),joint='curve')
e((23.5,1,40.5,18))              # ronde kop
r((27,15,37,44))                 # lange smalle romp
l([(27.5,21),(19,24),(18,7)],3.5); e((15,2,21,9))    # arm omhoog naast de kop
l([(36.5,21),(43,38)],3.5); e((41,36,46,42))          # arm omlaag
l([(29.5,43),(29,57)],4); l([(34.5,43),(36,57)],4)    # benen
e((23,55,31,61)); e((34,55,42,61))                    # voeten
for cx,cy in ((28,9),(36,9)):
    e((cx-3.5,cy-3.5,cx+3.5,cy+3.5),'white'); e((cx-2,cy-2,cx+2,cy+2))
im.save('silhouet_r2.png')
