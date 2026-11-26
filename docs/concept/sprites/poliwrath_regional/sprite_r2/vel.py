# vel.png r2: 6 varianten 8x in raster (rij E1, rij E2) + gespiegeld model; kop 12x per variant naast de modelkop en het Gen 3-Poliwrath-oog 12x; 1x.
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
import uitvoer as U
R=U.R; H,W=U.H,U.W
z=np.load('../sprite_r1/geschrapt.npz'); MOD=z['N'].astype('uint8').copy(); MOD[z['air']]=255
pw=np.array(Image.open('../../../../../graphics/pokemon/poliwrath/anim_front_gba.png'))[:64]
p=open('../../../../../graphics/pokemon/poliwrath/normal_gba.pal').read().split()[3:]; PC=[tuple(map(int,p[i*3:i*3+3])) for i in range(16)]
def rgb(a,bg=(255,255,255),pal=PAL):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=bg
    for k in range(1,16): o[a==k]=pal[k]
    return Image.fromarray(o)
def big(a,s): return a.resize((a.size[0]*s,a.size[1]*s),Image.NEAREST)
def rij(ims,gap=16):
    c=Image.new('RGB',(sum(i.size[0]+gap for i in ims),max(i.size[1] for i in ims)),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.size[0]+gap
    return c
rows=[]
rows.append(('8x: E1M1 | E1M2 | E1M3 | model (gespiegeld, geschrapt)',rij([big(rgb(R['E1'+m]),8) for m in ('M1','M2','M3')]+[big(Image.fromarray(MOD),8)])))
rows.append(('8x: E2M1 | E2M2 | E2M3 | model',rij([big(rgb(R['E2'+m]),8) for m in ('M1','M2','M3')]+[big(Image.fromarray(MOD),8)])))
c0,c1,r0,r1=10,48,0,19
kop=[big(rgb(R[k][r0:r1+1,c0:c1+1]),12) for k in ('E1M1','E1M2','E1M3')]
rows.append(('kop 12x: E1M1 | E1M2 | E1M3 | model',rij(kop+[big(Image.fromarray(MOD[r0:r1+1,c0:c1+1]),12)])))
kop=[big(rgb(R[k][r0:r1+1,c0:c1+1]),12) for k in ('E2M1','E2M2','E2M3')]
rows.append(('kop 12x: E2M1 | E2M2 | E2M3 | Gen 3-Poliwrath ogen (bron, x 16-52, y 6-22)',rij(kop+[big(rgb(pw[6:23,16:53],pal=PC),12)])))
one=[rij([rgb(np.array(Image.open('poliwrath_regional_r2_%s.png'%k)),bg) for bg in [(255,255,255),(232,232,216),(48,48,64),(20,20,28)]],8) for k in R]
rows.append(('1x licht/donker: '+' | '.join(R),rij(one,30)))
Wt=max(im.size[0] for _,im in rows); Ht=sum(im.size[1]+30 for _,im in rows)
vel=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(vel); y=0
for t,im in rows:
    d.text((4,y+8),t,fill=(0,0,0)); vel.paste(im,(0,y+26)); y+=im.size[1]+30
vel.save('vel.png'); print(vel.size)
