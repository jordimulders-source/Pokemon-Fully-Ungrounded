# Sneeuwmonster r5 = r4_oog_c_onder + Jordi (26 nov): "Bovenste knoop is ook niet rond, linkerstukje van de kuif ook niet en
# linkerkant van het hoofd is ook hoekig". Ogen bevroren; buiten de drie zones diff 0 (assert).
# Gebruik: cd sneeuwmonster && python3 sprite_r5/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
U='sprite_r5/'
r4=np.asarray(Image.open('sprite_r4/r4_oog_c_onder.png')).astype(int); o=r4.copy()
ZONES={'knoop':(23,33,28,39),'kuif links':(25,11,30,17),'hoofd links':(19,17,25,31)}   # (x0,y0,x1,y1) inclusief
# 1. Bovenste knoop: patroon + tinten van de onderste knoop (x24-27, y41-45; leest rond: .XX./XXXX/XXXX/XXXX/.XX.),
#    op de modelplek van de bovenste knoop (model natief u37-42, v53-59 -> sprite x24,7-27,9, y34,5-39,0 -> vak x24-27, y34-38).
for Y in range(34,39):
    for X in range(24,28):
        b=r4[Y+7,X]
        if b in (1,6,7,8): o[Y,X]=b
        elif r4[Y,X] in (1,6,7,8): o[Y,X]=4   # oude knooppixel buiten het nieuwe patroon -> sneeuw (midden, zoals de buurt)
# 2. Linkerbolletje kuif: model-dekking rij 12 = x28 .61, x29 .38, x30 .74 (bolletje 2 px breed bovenop, geen punt).
#    (29,12) bg -> sneeuwlijn (bovenrand, lichtkant), (29,13) sneeuwlijn -> licht (binnenkant bolletje); scheidingslijn begint nu op (30,13).
o[12,29]=2; o[13,29]=5
# 3. Linkerkant hoofd: modelrand (0,5-dekking) per rij: 16:25,7 17:24,6 18:23,5 19:22,6 20:22,3 21:21,7 22:21,2 23-26:20,6 27:21,1 28:21,2.
#    r4 had op rij 18 twee randpixels naast elkaar ((23,18) en (24,18)): sprong 25 -> 23, een knik. (23,18) eruit (dekking .50):
#    trap wordt 1-1-1-1-2-7 (x26 r16, x25 r17, x24 r18, x23 r19, x22 r20-21, x21 r22-28), regelmatig oplopend.
o[18,23]=0
def inzone(X,Y): return any(a<=X<=c and b<=Y<=d for a,b,c,d in ZONES.values())
D=np.argwhere(o!=r4); assert all(inzone(X,Y) for Y,X in D)
opslaan(o,U+'sneeuwmonster_r5.png')
for n,(a,b,c,d) in ZONES.items():
    l=[(int(X),int(Y),CH[r4[Y,X]]+'>'+CH[o[Y,X]]) for Y,X in D if a<=X<=c and b<=Y<=d]; print(n,len(l),l)
toon(o,10,40,17,40)
# vel: r5 8x | r4 8x | model / per zone 12x voor | na | model / 1x
def rgbo(o,bg=(255,255,255)):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
MI=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return MI.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def grid(a,z):
    dr=ImageDraw.Draw(a)
    for x in range(0,a.width,z): dr.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): dr.line([(0,y),(a.width,y)],fill=(225,225,225))
    return a
B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8; z=12
CZ=[('knoop',(21,31,31,47)),('kuif links',(23,9,35,19)),('hoofd links',(17,14,29,33))]
rows=[]
for n,K in CZ:
    w=(K[2]-K[0])*z; h=(K[3]-K[1])*z
    rows.append((n,[grid(rgbo(r4).crop(K).resize((w,h),Image.NEAREST),z),grid(rgbo(o).crop(K).resize((w,h),Image.NEAREST),z),mcrop(*K,z)]))
W=max(3*(W8+10),max(3*(p[0].width+10) for _,p in rows)); H=H8+30+sum(p[0].height+24 for _,p in rows)+80
V=Image.new('RGB',(W,H),'white'); dr=ImageDraw.Draw(V)
for i,(t,a) in enumerate((('r5 8x',rgbo(o).crop(B).resize((W8,H8),Image.NEAREST)),('r4 8x',rgbo(r4).crop(B).resize((W8,H8),Image.NEAREST)),('model',mcrop(*B,8)))):
    dr.text((i*(W8+10)+2,2),t,fill=(200,0,0)); V.paste(a,(i*(W8+10),16))
y=H8+24
for n,p in rows:
    for i,(t,a) in enumerate(zip(('voor (r4)','na (r5)','model'),p)): dr.text((i*(a.width+10)+2,y),n+': '+t,fill=(200,0,0)); V.paste(a,(i*(a.width+10),y+14))
    y+=p[0].height+24
x=0
for bg in [(255,255,255),(248,248,232),(40,48,56),(24,24,24)]: V.paste(rgbo(o,bg),(x,y)); x+=72
V.save(U+'vel.png'); print(U+'vel.png',V.size)
