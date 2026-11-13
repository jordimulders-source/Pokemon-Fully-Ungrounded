import numpy as np, sys
from PIL import Image
src=Image.open('../rond/rond_A.png')
a=np.array(src).astype(int); H,W=a.shape
pal=src.getpalette()[:48]
NEW={5:(76,104,152),15:(54,56,92)}
if "--shade" in sys.argv: NEW[3]=(134,166,190)
for i,c in NEW.items(): pal[3*i:3*i+3]=list(c)
cx,cy,R=39.5,36.5,13.6
L=np.isin(a,[1,2])
def tr(y,x): return not(0<=y<H and 0<=x<W) or a[y,x]==0
def isreg(y,x,vals): return 0<=y<H and 0<=x<W and a[y,x] in vals
b=a.copy()
eye=lambda y,x: 31<=y<=36 and 8<=x<=23
for y,x in zip(*np.nonzero(L)):
    if eye(y,x): continue
    # outward normal from transparent neighbours
    nx=ny=0
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dy or dx) and tr(y+dy,x+dx): nx+=dx; ny+=dy
    outer = (nx or ny) or any(tr(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1))
    d=((x-cx)**2+(y-cy)**2)**.5
    bol = d<=R+1.6 and y<=43 and x>=26
    vstk = any(isreg(y+dy,x+dx,(9,10)) for dy in (-1,0,1) for dx in (-1,0,1))
    if bol and outer:
        s=(-(x-cx)-(y-cy))/max(d,1)/1.414
        b[y,x]=5 if s>-0.25 else 15
    elif outer:
        if ny>0 and y>=57: b[y,x]=1          # grondcontact
        else:
            s=-nx-ny
            b[y,x]=2 if (s>0 or (s==0 and nx<0)) else 15
    else:  # binnenlijn
        if a[y,x]==1: b[y,x]=15 if vstk else 2
# ---- shading ----
SH = '--shade' in sys.argv
if SH:
    c=b.copy()
    for y in range(H):
        for x in range(W):
            v=a[y,x]
            d=((x-cx)**2+(y-cy)**2)**.5
            if v in (14,4) and x>=27 and y<=43 and d<=R+0.6 and not (y>=41 and x<45):
                s_=(-(x-cx)-(y-cy))/max(d,1)/1.414   # 1 = lit, -1 = schaduw
                w=max(0.0,(-s_+0.45))*4.6            # sikkelbreedte
                rim=R+0.6-d
                if rim< w*0.45: c[y,x]=3
                elif rim< w: c[y,x]=4
                else: c[y,x]=14 if v==14 or y<41 else v
    # voetstuk
    vs=np.isin(a,[9,10])
    for x in range(W):
        ys=np.nonzero(vs[:,x])[0]
        if len(ys)==0: continue
        top=ys.min()
        for y in ys:
            lim=2.6-max(0,x-30)*0.17
            c[y,x]=10 if (y<=46 and x<=37) or (y==47 and x<=31) or (y==48 and x<=28) or x<=27 else 9
    # onderkant voet: sikkel van 3 boven de grondlijn
    for x in range(12,W):
        col=[y for y in range(53,H) if c[y,x] in (3,4)]
        if not col: continue
        bot=max(col)
        for y in col:
            if c[y,x]==4 and bot-y<=0: c[y,x]=3
    c[31,51]=4; c[57,21]=3   # losse pixels (<3 px) opgeheven
    b=c
im=Image.fromarray(b.astype(np.uint8),'P'); im.putpalette(pal+[0]*(768-48))
out=sys.argv[1]; im.save(out,transparency=0)
chk=np.array(Image.open(out).convert('RGBA'))[:,:,3]; ref=np.array(Image.open('../rond/rond_A.png').convert('RGBA'))[:,:,3]
print('alpha-diff',int((chk!=ref).sum()),'gewijzigd',int((b!=a).sum()),'nonline changes',int(((b!=a)&~L).sum()))
s='0123456789ABCDEF'
for y in range(23,60):print('%2d '%y+''.join('.' if b[y,x]==0 else s[b[y,x]] for x in range(9,55)))
