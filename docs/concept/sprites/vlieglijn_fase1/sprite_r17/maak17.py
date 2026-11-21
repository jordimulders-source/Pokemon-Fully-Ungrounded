# r17 = r16 O2_P1 met schuine onderrand (trap 2-2-2-3-3-1) en schuin afgesneden kabelaanzetten
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
im=Image.open('sprite_r16/vlieg_r16_O2_P1.png'); b=im.load()
Y={21:37,22:37,23:38,24:38,25:39,26:39,27:40,28:40,29:40,30:39,31:39,32:39,33:38}
for x,y in Y.items():
    for yy in range(36,y):                       # boven de rand: lijf
        if b[x,yy] in (1,3,4,9) and not (x==21 and yy==36): b[x,yy]=2
    b[x,y]=4 if 23<=x<=29 else 3                 # randbelichting
    if b[x,y+1] in (2,3,4) and (x,y+1) not in ((25,40),(26,40)) and not (28<=x<=30): b[x,y+1]=1
b[30,40]=3                                       # middenpoot: rechterbovenhoek blijft kabel -> schuine bovenkant
b[34,41]=9                                       # nieuwe poot: linkerbovenhoek kabel in de taille -> schuin
b[39,40]=9                                       # achterpoot: kabel loopt schuin omhoog het achterlijf in
im.save('sprite_r17/vlieg_r17.png',transparency=0)
onbg(im).resize((512,512),Image.NEAREST).save('sprite_r17/vlieg_r17_8x.png')
