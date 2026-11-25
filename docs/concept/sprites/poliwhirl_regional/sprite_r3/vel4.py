import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
R=[np.load('r3_%s.npy'%v) for v in ('E6','E5','EM')]; H,W=R[0].shape
mod=Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')
def rgb(a):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=PAL[k]
    return Image.fromarray(o)
def mc(c0,c1,r0,r1,s): return mod.crop((int(xs[c0]),int(ys[r0]),int(xs[c1+1]),int(ys[r1+1]))).resize(((c1-c0+1)*s,(r1-r0+1)*s),Image.LANCZOS)
def gba(n):
    a=np.array(Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%n))[:64]
    p=open('../../../../../graphics/pokemon/%s/normal_gba.pal'%n).read().split()[3:]
    cols=[tuple(map(int,p[i*3:i*3+3])) for i in range(16)]
    o=np.zeros((64,64,3),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=cols[k]
    return Image.fromarray(o)
def png(p):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB')
def rij(ims,gap=16):
    c=Image.new('RGB',(sum(i.size[0]+gap for i in ims),max(i.size[1] for i in ims)),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.size[0]+gap
    return c
pw=gba('poliwhirl')
rows=[('8x: E6 | E5 | EM | model',rij([rgb(a).resize((W*8,H*8),Image.NEAREST) for a in R]+[mc(0,W-1,0,H-1,8)])),
 ('kop 12x: E6 | E5 | EM | model | Poliwhirl gba (zelfde schaal)',rij([rgb(a[0:12,10:36]).resize((26*12,12*12),Image.NEAREST) for a in R]+[mc(10,35,0,11,12),pw.crop((15,9,51,22)).resize((36*12,13*12),Image.NEAREST)])),
 ('4x: E6 | E5 | EM | regionale Poliwag | Poliwhirl gba',rij([png('poliwhirl_regional_r3_%s.png'%v).resize((256,256),Image.NEAREST) for v in ('E6','E5','EM')]+[png('../../poliwag_regional/af/poliwag_regional.png').resize((256,256),Image.NEAREST),pw.resize((256,256),Image.NEAREST)]))]
Wt=max(i.size[0] for _,i in rows); Ht=sum(i.size[1]+30 for _,i in rows)
v=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(v); y=0
for t,i in rows: d.text((4,y+8),t,fill=0); v.paste(i,(0,y+26)); y+=i.size[1]+30
v.save('vel.png'); print(v.size)
