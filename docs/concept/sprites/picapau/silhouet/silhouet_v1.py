# Silhouet v1: massa uit foto 4 (gespiegeld, maskers in fotocoordinaten).
# Met de hand (dunne delen): snavel schuiner omhoog, kuif met twee punten (Pikachu-oren),
# steunstaart met knik (bliksem-hint), pootjes. Daarna: kop vloeiend 1,25x (meer Pikachu), kop 1,55x, romp 0,78x korter, alles 1,45x breder.
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
P='docs/concept/sprites/picapau/silhouet/'
m=Image.open(P+'masker_foto4.png').convert('L')
W,H=700,1400
c=Image.new('L',(W,H),0); c.paste(m,(0,0))
d=ImageDraw.Draw(c)
d.polygon([(122,255),(10,196),(4,214),(116,322)],fill=255)                    # snavel
d.polygon([(165,250),(200,105),(228,112),(245,245)],fill=255)                  # kuifpunt voor
d.polygon([(225,255),(320,150),(340,168),(290,300)],fill=255)                  # kuifpunt achter
d.polygon([(300,1000),(420,985),(440,1120),(470,1135),(450,1330),(428,1332),(402,1175),(362,1155)],fill=255)  # staart
d.polygon([(215,990),(170,1040),(150,1062),(185,1060),(195,1080),(232,1030),(260,1010)],fill=255)  # voet dichtbij
d.polygon([(285,1020),(262,1062),(295,1060),(315,1030)],fill=255)             # voet ver
a=np.asarray(c).astype(float)/255
# vloeiende kopvergroting rond (185,290)
cy,cx=290,185; k=1.55; R1,R2=170,300
yy,xx=np.mgrid[0:H,0:W].astype(float)
r=np.hypot(yy-cy,xx-cx)
t=np.clip((r-R1)/(R2-R1),0,1); s=1/k*(1-t)+1*t
sy=cy+(yy-cy)*s; sx=cx+(xx-cx)*s
a=ndimage.map_coordinates(a,[sy,sx],order=1)>0.5
# romp korter: alles onder y=480 verticaal 0,78x
import numpy as _n
rows=_n.arange(a.shape[0]); src=_n.where(rows<480,rows,480+(rows-480)/0.78).astype(int)
src=_n.clip(src,0,a.shape[0]-1); a=a[src]
ys,xs=np.nonzero(a); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
hi=Image.fromarray((a*255).astype('uint8'))
hi=hi.resize((int(hi.width*1.45),hi.height))
th=52; sc=th/hi.height; tw=round(hi.width*sc)
small=np.asarray(hi.resize((tw,th),Image.BOX))>110
spr=np.zeros((64,64),bool); ox=(64-tw)//2; oy=64-th-3
spr[oy:oy+th,ox:ox+tw]=small
img=Image.fromarray((~spr*255).astype('uint8'))
img.save(P+'silhouet_v1_1x.png'); img.resize((512,512),Image.NEAREST).save(P+'silhouet_v1_8x.png')
hi.resize((hi.width//3,hi.height//3)).save(P+'silhouet_v1_hires.png')
print(tw,th)
