# Ronde 5: reparaties keuring r4 (punten 1-11). Basis r4, niets getekend: nieuwe randpixels alleen op modelplekken
# (natief gemeten), tinten uit het model of uit de omringende vlaktint. Telt elke pixel per punt. Gezicht bevroren.
import numpy as np; from PIL import Image
src=Image.open('../sprite_r4/sprite.png'); pal=src.getpalette(); o=np.asarray(src).astype(int).copy(); r4=o.copy()
m=np.asarray(Image.open('model_geschaald.png').convert('RGB')).astype(int); ML=m@[0.3,0.59,0.11]
GH=(2,3,4,5,6); WOOD=(7,8,9,10,13); GREY=(11,12)
FACE=np.zeros((64,64),bool); FACE[9:27,25:43]=True          # x25-42, y9-26
log={}
def mark(pt,y,x,v):
    if o[y,x]!=v:
        o[y,x]=v; log[pt]=log.get(pt,0)+1
def edge_info(y,x):
    nx=ny=0; e=False
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dx==dy==0: continue
            yy,xx=y+dy,x+dx
            if not(0<=yy<64 and 0<=xx<64) or o[yy,xx]==0:
                if abs(dx)+abs(dy)==1: e=True
                nx+=dx; ny+=dy
    return e,nx,ny
# --- punt 1 en 6: wagenrand op de modelplek (natief: donkere lijn x46-48 -> sprite x3, rij 75-96 -> sprite 23-33;
#     bovenlijn natief rij 73, x46-56 -> sprite rij 22, x3-7). Nieuwe pixels in selout van het hout (9, lichtkant).
for y in range(29,39): mark('1 linkerrand wagen (x3) ',y,3,9)
for x in range(3,8): mark('6 bovenrand wagen (rij 22)',22,x,9)
# --- punt 9: tint 6 (gloed) in de geest -> omringende geesttint
for y in range(0,23):
    for x in range(64):
        if o[y,x]==6 and not FACE[y,x]:
            nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<64 and 0<=x+dx<64 and o[y+dy,x+dx] in (2,3,4)]
            if nb: u,c=np.unique(nb,return_counts=True); mark('9 tint 6 uit de geest',y,x,int(u[c.argmax()]))
# --- punt 3: vuist; knokkellijn (53,8-9) donkerste groen 5; ruis (51,7) naar modeltint
for (x,y) in ((53,8),(53,9)): mark('3 vuist: knokkellijn',y,x,5)
def gtone(l): return 2 if l>=200 else 3 if l>=160 else 4 if l>=125 else 5
mark('3 vuist: ruis naar model',7,51,gtone(ML[7,51]))
# --- punt 11: linkerlob wolk x4-12 y45-52: vlak egaal uit het model (lum 100-140 -> 4), rand 5
for y in range(45,53):
    for x in range(4,13):
        if o[y,x] in (4,5):
            e,_,_=edge_info(y,x)
            mark('11 linkerlob wolk',y,x,5 if e else 4)
# --- punt 7/8/10: wagen binnen
WZ=np.zeros((64,64),bool); WZ[22:45,3:56]=True
# 7: losse zwarte pixels (component <=3, niet aan transparant, niet vast aan grote zwarte vlakken) -> donkere houttint 9
def comps(mask):
    lab=-np.ones((64,64),int); out=[]
    for y in range(64):
        for x in range(64):
            if mask[y,x] and lab[y,x]<0:
                st=[(y,x)]; lab[y,x]=len(out); cur=[]
                while st:
                    cy,cx=st.pop(); cur.append((cy,cx))
                    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                        yy,xx=cy+dy,cx+dx
                        if 0<=yy<64 and 0<=xx<64 and mask[yy,xx] and lab[yy,xx]<0: lab[yy,xx]=len(out); st.append((yy,xx))
                out.append(cur)
    return out
blk=comps((o==1)&WZ)
for c in blk:
    if len(c)<=3 and not any(edge_info(y,x)[0] for y,x in c) and all(not (39<=y<=44 and (x<6 or 13<=x<=20)) for y,x in c):
        for y,x in c: mark('7 losse zwarte pixel -> donkere houttint',y,x,9)
# 10: banden als stroken: per samenhangend donker stuk (9 en d samen) één tint (meerderheid)
dark=np.isin(o,[9,13])&WZ
for c in comps(dark):
    vals=[o[y,x] for y,x in c]
    if len(c)>=3:
        maj=9 if vals.count(9)>vals.count(13) else 13
        for y,x in c: mark('10 band/naad één tint',y,x,maj)
# 8: spikkels (donker stuk < 3 px) -> vlaktint, tenzij het model daar donker is in een vorm >= 3 px
for c in comps(np.isin(o,[9,13])&WZ):
    if len(c)<3:
        if sum(ML[y,x]<90 for y,x in c)>=1 and len(c)>=2: continue
        for y,x in c:
            if edge_info(y,x)[0]: continue
            nb=[o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[y+dy,x+dx] in (7,8,10)]
            if nb: u,cn=np.unique(nb,return_counts=True); mark('8 spikkel -> vlaktint',y,x,int(u[cn.argmax()]))
# --- punten 1,2,4,5,6 (+3 rechterrand): gesloten 1-px buitenlijn; lichtkant selout, schaduwkant #292018
newedge={}
for y in range(64):
    for x in range(64):
        v=o[y,x]
        if v==0 or v in GREY: continue
        e,nx,ny=edge_info(y,x)
        if not e: continue
        if 39<=y<=44 and (x<=5 or 14<=x<=19): continue                     # grijze wielen (bevroren r2)
        lit=(nx+ny<0) or (nx+ny==0 and ny<0)
        if v in GH and (y>=27 and not (x>=44 and y<=33 and v in (2,3))):   # wolk/staart: altijd selout 5
            nv=5
        elif v in GH: nv=5 if lit else 1
        else: nv=9 if lit else 1                                              # wagen
        newedge[(y,x)]=nv
# geen om-en-om: een randpixel die van al zijn randburen (>=2) verschilt, krijgt hun kleur
for (y,x),nv in list(newedge.items()):
    grp=lambda q: 'G' if q in GH else 'W'
    nb=[newedge[(y+dy,x+dx)] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (y+dy,x+dx) in newedge and grp(o[y+dy,x+dx])==grp(o[y,x])]
    if len(nb)>=1 and all(q!=nv for q in nb) and len(set(nb))==1: newedge[(y,x)]=nb[0]
for (y,x),nv in newedge.items():
    pt='2/4/5 geestrand' if o[y,x] in GH and y<27 else ('wolkrand' if o[y,x] in GH else '1/6 wagenrand')
    mark(pt,y,x,nv)
# --- bevriezing gezicht: terugzetten en tellen (randpixels van de kop mogen)
nfr=0
for y,x in zip(*np.where(FACE&(o!=r4))):
    if not edge_info(y,x)[0]: o[y,x]=r4[y,x]; nfr+=1
np.save('r5.npy',o)
im=Image.fromarray(o.astype(np.uint8),'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
im=Image.open('sprite.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),'white')
Image.alpha_composite(bg,im).convert('RGB').resize((512,512),Image.NEAREST).save('sprite_8x.png')
print('per punt:',log); print('totaal t.o.v. r4:',(o!=r4).sum(),'| gezicht teruggezet',nfr)
fi=FACE.copy()
print('gezichtzone diff (niet-rand):',sum(1 for y,x in zip(*np.where(FACE&(o!=r4))) if not edge_info(y,x)[0]))
print('kleuren',len(Image.open('sprite.png').getcolors()))
