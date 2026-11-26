# Sneeuwmonster r6 = r5 + Jordi "linkerstukje van de kuif ook niet [rond] en linkerkant van het hoofd is ook hoekig" (ruimer:
# dekking >= .30 mag erbij, <= .60 mag eraf, alleen naar de modelvorm). Ogen en knopen bevroren (assert).
# Varianten: hoofd A (licht) / B (sterker), kuif 1 (licht) / 2 (sterker) -> r6_hoofd<A|B>_kuif<1|2>.png
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
U='sprite_r6/'
r5=np.asarray(Image.open('sprite_r5/sneeuwmonster_r5.png')).astype(int)
# modelrand links (0,5-dekking) r16..28: 25,7 24,6 23,5 22,6 22,3 21,7 21,2 20,6 20,6 20,6 20,6 21,1 21,2
# dekking die erbij komt: (24,17) .40, (23,18) .50, (22,19) .40, (21,21) .30, (20,23..26) .41-.45; er gaat niets > .60 af.
HOOFD={  # linkerrandpixel per rij 16..28
 'A':[26,25,24,23,22,22,21,21,20,20,20,21,21],   # trap: 1-1-1-1 schuin, dan verticaal 2-2-3, terug 2 (kin)
 'B':[26,24,23,22,22,21,21,20,20,20,20,21,21],   # trap: horizontaal 2-1-1, dan verticaal 2-2-4, terug 2: cirkelboog (zoals Igglybuff/Marill _gba)
}
def hoofd(o,v):
    for i,e in enumerate(HOOFD[v]):
        Y=16+i; fg=np.where(o[Y]>0)[0]; oud=fg.min(); rk=o[Y,oud]   # randkleur van r5 (sneeuwlijn boven, zwart rij 27-28)
        binnen=o[Y,oud+1]
        if e<oud:
            for X in range(e+1,oud+1): o[Y,X]=binnen
        else:
            o[Y,:e]=0
        o[Y,e]=rk if rk in (1,2) else 2
        if i and e<prev-1:              # horizontale stap > 1: de stap zelf is ook buitenrand (geen open/lichte rand)
            for X in range(e+1,prev): o[Y,X]=o[Y,e]
        prev=e
    return o
def kuif(o,v):
    if v=='1':   # r4-toestand + model-inkeping: (29,12) achtergrond (dekking .38), (29,13) zwart (model natief (45,19) = L 6-8)
        o[12,29]=0; o[13,29]=1
    else:        # bolletje 2 px breed bovenop ((28,12) (29,12) sneeuwlijn), binnenkant (29,13) licht, inkeping naar het middenbolletje = (30,12) zwart
        o[12,29]=2; o[13,29]=5; o[12,30]=1
    return o
OGEN_KNOPEN=[(x,y) for x in range(21,35) for y in range(21,28) if r5[y,x] in (1,6,7,8) and x>=22]+[(x,y) for x in range(23,29) for y in range(33,47) if r5[y,x] in (1,6,7,8)]
uit={}
for h in 'AB':
    for k in '12':
        o=kuif(hoofd(r5.copy(),h),k); assert all(o[y,x]==r5[y,x] for x,y in OGEN_KNOPEN)
        n=U+'r6_hoofd%s_kuif%s.png'%(h,k); opslaan(o,n); uit[(h,k)]=o
        d=np.argwhere(o!=r5); zh=[(int(X),int(Y)) for Y,X in d if X<=26 and Y>=16]; zk=[(int(X),int(Y)) for Y,X in d if not(X<=26 and Y>=16)]
        print(n,'| hoofd %d px'%len(zh),'| kuif %d px'%len(zk),zk,'| silhouet t.o.v. r5: +%d -%d'%(((o>0)&(r5==0)).sum(),((o==0)&(r5>0)).sum()))
BEST=('B','2'); opslaan(uit[BEST],U+'sneeuwmonster_r6.png')
toon(uit[BEST],10,31,17,35)
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
K=(17,9,36,31); z=12; w=(K[2]-K[0])*z; h=(K[3]-K[1])*z
tegels=[('r5',r5)]+[('hoofd %s, kuif %s'%hk,uit[hk]) for hk in uit]+[('model',None)]
B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8
cols=3; rows=2
V=Image.new('RGB',(max(cols*(w+10),3*(W8+10)),rows*(h+20)+H8+30+80),'white'); dr=ImageDraw.Draw(V)
for i,(t,o) in enumerate(tegels):
    x=(i%cols)*(w+10); y=(i//cols)*(h+20)
    a=mcrop(*K,z) if o is None else grid(rgbo(o).crop(K).resize((w,h),Image.NEAREST),z)
    dr.text((x+2,y+2),t+(' (gekozen)' if o is not None and o is uit[BEST] else ''),fill=(200,0,0)); V.paste(a,(x,y+14))
y=rows*(h+20)+6
for i,(t,a) in enumerate((('r6 8x (hoofd %s, kuif %s)'%BEST,rgbo(uit[BEST]).crop(B).resize((W8,H8),Image.NEAREST)),('r5 8x',rgbo(r5).crop(B).resize((W8,H8),Image.NEAREST)),('model',mcrop(*B,8)))):
    dr.text((i*(W8+10)+2,y),t,fill=(200,0,0)); V.paste(a,(i*(W8+10),y+14))
x=0
for bg in [(255,255,255),(248,248,232),(40,48,56),(24,24,24)]: V.paste(rgbo(uit[BEST],bg),(x,y+H8+20)); x+=72
V.save(U+'vel.png'); print(U+'vel.png',V.size)
