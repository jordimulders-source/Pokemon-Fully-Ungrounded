# Sneeuwmonster r9 = r7 + Jordi over r8: "geen enkele goed, nergens doe je echt de vorm na, de een na laatste misschien maar daar
# zijn ze te groot". Knopen = de natieve modelknopen (gereedschap/natief.png) zelf verkleind met oppervlakteweging per klasse.
# Alleen de knoopvakken veranderen (assert). Gebruik: cd sneeuwmonster && python3 sprite_r9/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
U='sprite_r9/'
base=np.asarray(Image.open('sprite_r7/sneeuwmonster_r7.png')).astype(int)
N=np.asarray(Image.open(NATIEF).convert('RGB')).astype(float); LN=N@[.299,.587,.114]; SN=N.max(2)-N.min(2)
def kl(v,u):
    l=LN[v,u]
    if SN[v,u]>=40 or l>=170: return '.'
    return '#' if l<20 else 'd' if l<75 else 'm' if l<115 else 'L' if l<150 else '.'
def natief(x0,x1,y0,y1): return [''.join(kl(v,u) for u in range(x0,x1+1)) for v in range(y0,y1+1)]
NB=natief(37,42,53,59); NO=natief(36,42,63,69)   # boven 6x7 schuin, onder 7x7 rond
DREMPEL=0.45
CODE={'#':1,'d':6,'m':7,'L':8}
def verklein(pat,W,H):
    """oppervlakteweging per klasse: elke spritepixel krijgt de klasse met het grootste oppervlak ('.' = sneeuw telt mee)"""
    h,w=len(pat),len(pat[0]); out=[]
    for J in range(H):
        r=''
        for I in range(W):
            a0,a1=I*w/W,(I+1)*w/W; b0,b1=J*h/H,(J+1)*h/H; acc={}
            for v in range(int(b0),int(np.ceil(b1))):
                for u in range(int(a0),int(np.ceil(a1))):
                    wt=max(0,min(a1,u+1)-max(a0,u))*max(0,min(b1,v+1)-max(b0,v))
                    acc[pat[v][u]]=acc.get(pat[v][u],0)+wt
            st=sum(v for k,v in acc.items() if k!='.')
            if st<DREMPEL*(w/W)*(h/H)-1e-9: r+='.'; continue   # pixel is steen als de steenklassen samen >= de helft dekken
            r+=max((k for k in acc if k!='.'),key=lambda k:(acc[k],'#dmL'.index(k)))
        out.append(r)
    return out
VAR={ # naam: (boven W,H, plek), (onder W,H, plek)
 'v1':((5,6,(24,34)),(5,5,(24,41))),
 'v2':((4,5,(25,35)),(5,5,(24,41))),
 'v3':((5,6,(24,34)),(6,5,(23,41))),
}
VAK=[(22,33,30,40),(21,40,30,47)]
oud=[{(X,Y) for Y in range(v[1],v[3]+1) for X in range(v[0],v[2]+1) if base[Y,X] in (6,7,8) or (base[Y,X]==1 and 23<=X<=29 and 33<=Y<=46 and all(base[Y+dy,X+dx]!=0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))))} for v in VAK]
def vorm(pat,x0,y0): return {(x0+i,y0+j):CODE[ch] for j,r in enumerate(pat) for i,ch in enumerate(r) if ch!='.'}
uit={}; pats={}
for n,((wb,hb,lb),(wo,ho,lo)) in VAR.items():
    pb,po=verklein(NB,wb,hb),verklein(NO,wo,ho); pats[n]=(pb,po)
    o=base.copy(); b,u=vorm(pb,*lb),vorm(po,*lo); nieuw={**b,**u}
    rest={p for s in oud for p in s if p not in nieuw}
    while rest:
        for X,Y in sorted(rest):
            nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) if (X+dx,Y+dy) not in rest and (X+dx,Y+dy) not in nieuw and o[Y+dy,X+dx] in (3,4,5)]
            if nb: o[Y,X]=max(set(nb),key=nb.count); rest.discard((X,Y)); break
        else: raise SystemExit('vastgelopen')
    for (X,Y),k in nieuw.items(): o[Y,X]=k
    D=np.argwhere(o!=base); assert all(any(v[0]<=X<=v[2] and v[1]<=Y<=v[3] for v in VAK) for Y,X in D)
    assert not any((X+dx,Y+dy) in u for X,Y in b for dx in (-1,0,1) for dy in (-1,0,1))
    opslaan(o,U+'sneeuwmonster_r9_%s.png'%n); uit[n]=o
    print(n,'boven %dx%d %s | onder %dx%d %s | diff t.o.v. r7: %d px (knoop %d, sneeuw %d)'%(wb,hb,'/'.join(pb),wo,ho,'/'.join(po),len(D),sum(1 for Y,X in D if (X,Y) in nieuw),sum(1 for Y,X in D if (X,Y) not in nieuw)))
# vel
PC={'.':(244,250,255),'#':PAL[1],'d':PAL[6],'m':PAL[7],'L':PAL[8]}
def patimg(p,z):
    a=np.array([[PC[c] for c in r] for r in p],'uint8'); return grid(Image.fromarray(a).resize((len(p[0])*z,len(p)*z),Image.NEAREST),z)
def rgbo(o,bg=(255,255,255)):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def grid(a,z):
    dr=ImageDraw.Draw(a)
    for x in range(0,a.width,z): dr.line([(x,0),(x,a.height)],fill=(200,200,200))
    for y in range(0,a.height,z): dr.line([(0,y),(a.width,y)],fill=(200,200,200))
    return a
z=16; V=Image.new('RGB',(1300,1200),'white'); dr=ImageDraw.Draw(V)
x=0
for t,(pb,po) in [('natief model',(NB,NO))]+list(pats.items()):
    dr.text((x,2),t+' 16x',fill=(200,0,0)); V.paste(patimg(pb,z),(x,16)); V.paste(patimg(po,z),(x,16+7*z+12)); x+=7*z+20
K=(20,32,33,49); w=(K[2]-K[0])*z; h=(K[3]-K[1])*z; y=16+14*z+30; x=0
for t,o in [('r7',base)]+list(uit.items()):
    dr.text((x,y),t+' 16x',fill=(200,0,0)); V.paste(grid(rgbo(o).crop(K).resize((w,h),Image.NEAREST),z),(x,y+14)); x+=w+10
B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8; y+=h+24; x=0
for t,o in uit.items():
    dr.text((x,y),t+' 8x',fill=(200,0,0)); V.paste(rgbo(o).crop(B).resize((W8,H8),Image.NEAREST),(x,y+14)); x+=W8+10
for bg in [(255,255,255),(40,48,56)]:
    V.paste(rgbo(uit[list(uit)[0]],bg),(x,y+14+(0 if bg[0]==255 else 70)))
y+=H8+20; x=0
for t,o in uit.items():
    for bg in [(255,255,255),(40,48,56)]: V.paste(rgbo(o,bg),(x,y)); x+=70
    x+=16
V=V.crop((0,0,V.width,y+70)); V.save(U+'vel.png'); print(U+'vel.png',V.size)
