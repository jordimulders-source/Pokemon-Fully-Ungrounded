# Eindkeuring (DC) zand-djinn fase 3: alleen paletkleuren en tinten, niets getekend.
import numpy as np; from PIL import Image
SRC='../r11/biceps.png'; OUT='zandloper_fase3.png'
im=Image.open(SRC); a=np.array(im).copy(); pal=im.getpalette()[:48]
def zet(lijst,nieuw,oud=None,doel=a):
    for x,y in lijst:
        if oud is not None: assert doel[y,x] in oud,(x,y,doel[y,x])
        doel[y,x]=nieuw
# 1. Belijning: zwart aan de lichtkant -> eigen donkerste tint (zand 2, glas 7, hout 11)
zet([(29,3),(29,4),(25,7),(24,8),(22,9),(19,10),(20,10),(21,10),(40,15),(41,15),(44,15),(43,16)],2,{1})
zet([(17,5),(15,6),(14,7),(15,8),(16,10),(16,11),(44,7),(43,8),(43,9),(46,8),(48,9),(50,10),(44,11),(44,13),(26,51),(38,52)],7,{1})
zet([(39,52)],11,{1})
# zwart aan de schaduwkant (rechterrand hoofd)
zet([(39,13),(39,14)],1,{2})
# 2. Schaduw: sikkel langs de rechterflank (model: rechterflank donker)
zet([(45,21),(45,22),(45,23),(45,24),(44,24),(44,25),(43,26)],4,{5})
zet([(42,29),(42,30),(41,31),(41,32),(41,34),(40,35),(40,36),(39,37),(38,38)],3,{4})
zet([(45,16)],3,{5})   # lichte kleur op de buitenrand
# 3. Kleurtinten (hue shift: licht geler, schaduw roder; lijnbasis als kleur, niet bijna-zwart)
P={2:(96,58,24),3:(164,112,52),4:(204,156,70),5:(232,190,98),6:(252,226,150),
   7:(64,94,122),8:(114,160,186),9:(160,204,224),10:(222,244,250),
   11:(92,50,30),12:(138,82,46)}
for i,c in P.items(): pal[3*i:3*i+3]=list(c)
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal+[0]*(768-48)); o.save(OUT,transparency=0)
