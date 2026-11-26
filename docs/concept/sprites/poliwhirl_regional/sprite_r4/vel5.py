# vel.png r4: r4 | r3_E6 | model 8x; kop 12x: r4 met omtrek modelogen (rood, gemeten buitenrand) | model met dezelfde omtrek
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
r4=np.load('r4.npy'); r3=np.load('r3_E6.npy'); H,W=r4.shape
mod=Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')
def rgb(a):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=PAL[k]
    return Image.fromarray(o)
def mc(c0,c1,r0,r1,s): return mod.crop((int(xs[c0]),int(ys[r0]),int(xs[c1+1]),int(ys[r1+1]))).resize(((c1-c0+1)*s,(r1-r0+1)*s),Image.LANCZOS)
def rij(ims,gap=16):
    c=Image.new('RGB',(sum(i.size[0]+gap for i in ims),max(i.size[1] for i in ims)),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.size[0]+gap
    return c
OOG=[(13.6,18.0,2.6,7.4),(26.8,31.5,1.9,7.5)]   # buitenrand modelogen in cellen
def omtrek(im,c0,r0,s):
    d=ImageDraw.Draw(im)
    for x0,x1,y0,y1 in OOG: d.ellipse([(x0-c0)*s,(y0-r0)*s,(x1-c0)*s,(y1-r0)*s],outline=(255,0,0),width=2)
    return im
s=12; c0,c1,r0,r1=10,35,0,12
A=omtrek(rgb(r4[r0:r1+1,c0:c1+1]).resize(((c1-c0+1)*s,(r1-r0+1)*s),Image.NEAREST),c0,r0,s)
B=omtrek(mc(c0,c1,r0,r1,s),c0,r0,s)
C=rgb(r3[r0:r1+1,c0:c1+1]).resize(((c1-c0+1)*s,(r1-r0+1)*s),Image.NEAREST)
MEET=('model: oogmiddens (15,8; 5,0) en (29,2; 4,7), afstand 13,4, oog->neusgat 3,6, oog->mond 5,7, links steekt 0,3 buiten de kop, rechts 2,6 tot de rechterrand | '
      'r3_E6: (17;6) (30;5), 13, 3,0, 5,0, -1 (binnen de kop), 1 | r4: (16;5) (29;5), 13, 3,5, 5,5, 0 (oog = silhouet), 2   [cellen]')
rows=[(MEET,Image.new('RGB',(4,4),'white')),('8x: r4 | r3_E6 | model',rij([rgb(a).resize((W*8,H*8),Image.NEAREST) for a in (r4,r3)]+[mc(0,W-1,0,H-1,8)])),
      ('kop 12x: r4 + omtrek modelogen (rood) | model + omtrek | r3_E6',rij([A,B,C]))]
Wt=max(max(i.size[0] for _,i in rows),1500); Ht=sum(i.size[1]+30 for _,i in rows)
v=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(v); y=0
for t,i in rows: d.text((4,y+8),t,fill=0); v.paste(i,(0,y+26)); y+=i.size[1]+30
v.save('vel.png'); print(v.size)
