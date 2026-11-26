# vel.png r2: S1 | S2 | r1 | model 8x; benen/armen 12x (r2 | r1 | model); kop 12x (r2 | model | Poliwhirl gba);
# buik 12x (S1 | S2 | model | Poliwhirl gba | regionale Poliwag met weggehaalde staartpixels in magenta)
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
S1=np.load('r2_S1.npy'); S2=np.load('r2_S2.npy'); r1=np.load('../sprite_r1/r1_a1.npy'); H,W=S1.shape
mod=Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')
def rgb(a):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=PAL[k]
    return Image.fromarray(o)
def mc(c0,c1,r0,r1_,w,h): return mod.crop((int(xs[c0]),int(ys[r0]),int(xs[c1+1]),int(ys[r1_+1]))).resize((w,h),Image.LANCZOS)
def gba(n):
    a=np.array(Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%n))[:64]
    p=open('../../../../../graphics/pokemon/%s/normal_gba.pal'%n).read().split()[3:]
    cols=[tuple(map(int,p[i*3:i*3+3])) for i in range(16)]
    o=np.zeros((64,64,3),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=cols[k]
    return Image.fromarray(o)
def rij(ims,gap=16):
    c=Image.new('RGB',(sum(i.size[0]+gap for i in ims),max(i.size[1] for i in ims)),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.size[0]+gap
    return c
def sp(arrs,c0,c1,r0,r1_,s): return [rgb(a[r0:r1_+1,c0:c1+1]).resize(((c1-c0+1)*s,(r1_-r0+1)*s),Image.NEAREST) for a in arrs]
def m(c0,c1,r0,r1_,s): return mc(c0,c1,r0,r1_,(c1-c0+1)*s,(r1_-r0+1)*s)
pw=gba('poliwhirl')
pg=Image.open('../../poliwag_regional/af/poliwag_regional.png').convert('RGBA'); bg=Image.new('RGBA',pg.size,(255,255,255,255)); bg.alpha_composite(pg); pg=bg.convert('RGB')
pgm=pg.copy(); px=pgm.load()
for x,y in ((12,31),(13,30)): px[x+7,y+19]=(255,0,255)
rows=[('8x: S1 | S2 | r1 | model',rij(sp([S1,S2,r1],0,W-1,0,H-1,8)+[m(0,W-1,0,H-1,8)])),
 ('kop 12x: r2 | model | Poliwhirl gba (ogen 1-op-1, 37 px per oog, geen extra ring)',rij(sp([S1],10,35,0,12,12)+[m(10,35,0,12,12),pw.crop((14,8,50,24)).resize((36*12,16*12),Image.NEAREST)])),
 ('buik 12x: S1 | S2 | model | Poliwhirl gba | regionale Poliwag af (magenta = 2 weggehaalde staartpixels; S2 stopt nu op het pixel erboven)',
   rij(sp([S1,S2],14,31,16,31,12)+[m(14,31,16,31,12),pw.crop((17,19,45,43)).resize((28*12,24*12),Image.NEAREST),pgm.crop((7,36,27,54)).resize((20*12,18*12),Image.NEAREST)])),
 ('benen 12x: r2 | r1 | model',rij(sp([S1,r1],6,44,28,46,12)+[m(6,44,28,46,12)])),
 ('armen/schouders 12x: r2 | r1 | model',rij(sp([S1,r1],4,49,11,31,12)+[m(4,49,11,31,12)]))]
Wt=max(i.size[0] for _,i in rows); Ht=sum(i.size[1]+30 for _,i in rows)
v=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(v); y=0
for t,i in rows: d.text((4,y+8),t,fill=0); v.paste(i,(0,y+26)); y+=i.size[1]+30
v.save('vel.png'); print(v.size)
