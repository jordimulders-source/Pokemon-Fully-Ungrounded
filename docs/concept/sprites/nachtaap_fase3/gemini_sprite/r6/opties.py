from PIL import Image, ImageDraw; import numpy as np
from collections import Counter
CH='.123456789abcdef'
src=Image.open('../r5/muriqui.png'); PAL=src.getpalette()[:48]; P=np.array(PAL).reshape(16,3)
A0=np.array(src)
def save(a,fn):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save(fn,transparency=0)
def rgb(a,s,bg=(255,255,255)):
    r=np.zeros((64,64,3),int); r[:]=bg; m=a>0; r[m]=P[a[m]]
    return Image.fromarray(r.astype('uint8')).resize((64*s,64*s),Image.NEAREST)
# ---- rug: bogen weg
def zonder_bogen(a):
    a=a.copy()
    for it in range(4):
        for y in range(26,46):
            for x in range(22,45):
                if a[y,x] in (9,11):
                    c=Counter(int(v) for v in a[y-2:y+3,x-2:x+3].ravel() if v in (2,3,4,5))
                    if c: a[y,x]=c.most_common(1)[0][0]
    return a
def T(rows): return [[(k,c) for k,c in enumerate(r) if c!='.'] for r in rows]
BIG=T(["b99....",".b99...","...99..","...b99.","....b99","....b99","....b99","....99.","...b9..","..b9..."])
SMALL=T(["b99...",".b99..","..b99.","...b99","...b99","...b99","...99.","..b9..",".b9..."])
def bogen(a,pos):
    a=a.copy()
    for (x0,y0,Tb) in pos:
        for r,row in enumerate(Tb):
            for dx,c in row:
                if a[y0+r,x0+dx] in (2,3,4,5): a[y0+r,x0+dx]=CH.index(c)
    return a
RUG={'R0 huidig':None,
     'R1 horizontaal':[(23,32,BIG),(29,32,BIG),(35,32,SMALL)],
     'R2 romp-as (1 px/boog omlaag)':[(23,32,BIG),(29,33,BIG),(35,34,SMALL)],
     'R3 lager, romp-as':[(22,33,BIG),(28,34,BIG),(34,35,SMALL)]}
# ---- ogen (L x5-6, R x12-14, y37-39)
def oog(a,L,R):
    a=a.copy()
    for r in range(3):
        for k,c in enumerate(L[r]): a[37+r,5+k]=CH.index(c)
        for k,c in enumerate(R[r]): a[37+r,12+k]=CH.index(c)
    return a
OGEN={'O0 huidig':None,
 'O1 geen glans':(["ff","fa","ef"],["fff","faa","fef"]),
 'O2 donker, licht van onder':(["ef","ff","fa"],["eff","fff","faf"]),
 'O3 pupil':(["ff","f1","ef"],["fff","f1a","fef"]),
 'O4 gloeiend, zonder pupil':(["aa","ee","aa"],["aaa","eee","aaa"])}
base=zonder_bogen(A0)
vel=Image.new('RGB',(5*520,2*560+60),'white'); d=ImageDraw.Draw(vel)
d.text((10,5),'OGEN (kop 16x, rest gelijk aan r5)',fill='black')
for i,(n,v) in enumerate(OGEN.items()):
    a=A0 if v is None else oog(A0,*v); save(a,n.split()[0]+'.png')
    kop=rgb(a,16).crop((0,22*16,24*16,48*16)).resize((384,416),Image.NEAREST)
    vel.paste(kop,(i*520+10,25)); vel.paste(rgb(a,1),(i*520+410,25)); vel.paste(rgb(a,1,(40,40,56)),(i*520+410,95)); d.text((i*520+10,445),n,fill='black')
d.text((10,600),'RUGBOGEN (8x)',fill='black')
for i,(n,v) in enumerate(RUG.items()):
    a=A0 if v is None else bogen(base,v); save(a,n.split()[0]+'.png')
    vel.paste(rgb(a,8).crop((0,0,512,512)),(i*520,620)); d.text((i*520+10,1140),n,fill='black')
vel.save('vel_opties.png')
