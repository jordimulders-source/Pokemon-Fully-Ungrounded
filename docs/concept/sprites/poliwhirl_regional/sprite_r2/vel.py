# vel.png: vier varianten 8x naast het model (zelfde schaal); close-up kop en buik 12x naast het model; 1x licht/donker;
# 4x naast regionale Poliwag, Poliwhirl (gba) en Dundragoon.
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
V=['a1','a2','b1','b2']; R={v:np.load('r1_%s.npy'%v) for v in V}; H,W=R['a1'].shape
mod=Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')
def rgb(a,bg=(255,255,255)):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=bg
    for k in range(1,16): o[a==k]=PAL[k]
    return Image.fromarray(o)
def modcrop(c0,c1,r0,r1,w,h): return mod.crop((int(xs[c0]),int(ys[r0]),int(xs[c1+1]),int(ys[r1+1]))).resize((w,h),Image.LANCZOS)
def gba(n):
    a=np.array(Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%n))[:64]
    p=open('../../../../../graphics/pokemon/%s/normal_gba.pal'%n).read().split()[3:]
    cols=[tuple(map(int,p[i*3:i*3+3])) for i in range(16)]
    o=np.zeros((64,64,3),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=cols[k]
    return Image.fromarray(o)
def png(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def rij(ims,gap=16):
    c=Image.new('RGB',(sum(i.size[0]+gap for i in ims),max(i.size[1] for i in ims)),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.size[0]+gap
    return c
rows=[]
rows.append(('8x: a1 | a2 | b1 | b2 | model (zelfde schaal)   a = Poliwhirl-spiraal in modelrood, b = Poliwhirl-spiraal letterlijk; 1 = ogen Gen 3-Poliwhirl, 2 = ogen regionale Poliwag',
             rij([rgb(R[v]).resize((W*8,H*8),Image.NEAREST) for v in V]+[modcrop(0,W-1,0,H-1,W*8,H*8)])))
def close(c0,c1,r0,r1,s=12):
    ims=[rgb(R[v][r0:r1+1,c0:c1+1]).resize(((c1-c0+1)*s,(r1-r0+1)*s),Image.NEAREST) for v in V]
    return rij(ims+[modcrop(c0,c1,r0,r1,ims[0].size[0],ims[0].size[1])])
rows.append(('kop 12x: a1 | a2 | b1 | b2 | model',close(10,35,0,13)))
rows.append(('buik 12x: a1 | a2 | b1 | b2 | model',close(13,32,15,31)))
one=[]
for v in V:
    S=np.array(Image.open('poliwhirl_regional_r1_%s.png'%v))
    one.append(rij([rgb(S,bg) for bg in [(255,255,255),(232,232,216),(48,48,64),(20,20,28)]],8))
rows.append(('1x licht/donker: a1 | a2 | b1 | b2',rij(one,30)))
ref=[rgb(np.array(Image.open('poliwhirl_regional_r1_%s.png'%v))).resize((256,256),Image.NEAREST) for v in ('a2','b1')]
ref+=[png('../../poliwag_regional/af/poliwag_regional.png').resize((256,256),Image.NEAREST),gba('poliwhirl').resize((256,256),Image.NEAREST),
      png('../../dundragoon/af/dundragoon.png').resize((256,256),Image.NEAREST)]
rows.append(('4x: r1 a2 | r1 b1 | regionale Poliwag (af) | Poliwhirl (gba) | Dundragoon (af)',rij(ref)))
Wt=max(im.size[0] for _,im in rows); Ht=sum(im.size[1]+30 for _,im in rows)
vel=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(vel); y=0
for t,im in rows:
    d.text((4,y+8),t,fill=(0,0,0)); vel.paste(im,(0,y+26)); y+=im.size[1]+30
vel.save('vel.png'); print(vel.size)
