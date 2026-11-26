# Sneeuwmonster r3_ogen: alleen de ogen rond (Jordi: "probeer de ogen rond te maken"), op r2; buiten de oogvakken diff 0.
# Vorm = pixelpatroon van echte Gen 3 ronde stipogen (_gba):
#   4x4 rond (Lickitung (38,21), Politoed (32,19), Delcatty dichtbij-oog (31,24), Dewgong (19,16)):  .XX. / XGXX / XXXX / .XX.
#   3x4 ovaal, ver oog (Delcatty ver-oog (23,24)):                                                   XX. / XGX / XXX / .XX
#   glans G in alle vier de bronnen linksboven binnen het oog (kolom 1, rij 1) = ook de modelplek.
#   Glansvariant "onder" (SPRITE_KERN, vuurduivel): zelfde kolom, één rij lager (kolom 1, rij 2), pupilpixel die niet aan de rand grenst.
# Tinten per pixel uit het 1024-model (gemiddelde helderheid van de donkere modelpixels: <48 zwart, <76 steen donker, anders steen midden);
# een oogpixel zonder donkere modeldekking (verschoven variant) neemt de tint van dezelfde patroonplek in de onverschoven vorm.
# Gebruik: cd sneeuwmonster && python3 sprite_r3_ogen/bouw.py   (maakt alle combinaties + vel)
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
U='sprite_r3_ogen/'
r2=np.asarray(Image.open('sprite_r2/sneeuwmonster_r2.png')).astype(int)
VAK=[(21,26,21,27),(29,34,22,28)]          # oogvakken (x0,x1,y0,y1), gelijk aan de zone 'ogen'
def invak(X,Y): return any(a<=X<=b and c<=Y<=d for a,b,c,d in VAK)
R44=['.XX.','XXXX','XXXX','.XX.']; R34=['XX.','XXX','XXX','.XX']
def vorm(pat,x0,y0): return {(x0+i,y0+j) for j,r in enumerate(pat) for i,ch in enumerate(r) if ch=='X'}
MG=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); LG=MG@[.299,.587,.114]; SG=MG.max(2)-MG.min(2); DK=(LG<160)&(SG<45)
fr=lambda X,ph,o0,u0: int(round(ph+0.5+10.24*((X-o0)/S+u0)))
def oogtint(X,Y):
    r=np.s_[fr(Y,9.25,Y0,V0):fr(Y+1,9.25,Y0,V0),fr(X,9.05,X0,U0):fr(X+1,9.05,X0,U0)]
    d=DK[r]
    if d.mean()<0.15: return None
    l=LG[r][d].mean(); return 1 if l<48 else 6 if l<76 else 7
# varianten: naam -> (patroon, x0, y0, tint-bron x0 (onverschoven))
RECHTS={'R':(R44,30,23,30)}
LINKS={'a':(R34,22,22,22),'b':(R44,22,22,22),'c':(R44,23,22,22),'a1':(R34,23,22,22)}   # a1 = extra: a 1 px naar rechts
def snee(o,X,Y):   # vrijgekomen oogpixel -> sneeuwtint van r2 (als die daar sneeuw is), anders meest voorkomende niet-oog sneeuwbuur in r2
    if r2[Y,X] in (3,4,5) and (X,Y) not in GL2: return r2[Y,X]
    nb=[r2[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and r2[Y+dy,X+dx] in (3,4,5) and (X+dx,Y+dy) not in GL2]
    return max(set(nb),key=nb.count) if nb else 5
GL2={(23,23),(31,24)}   # r2-glanspixels (5 in een oog, geen sneeuw)
def bouw(lv,gl):
    o=r2.copy(); rand=[]
    for Y in range(64):
        for X in range(64):
            if invak(X,Y) and (o[Y,X] in (1,6,7,8) or (X,Y) in GL2): o[Y,X]=snee(o,X,Y)
    for pat,x0,y0,xs in (RECHTS['R'],LINKS[lv]):
        V=vorm(pat,x0,y0)
        for X,Y in V:
            t=oogtint(X,Y) if x0==xs else None
            if t is None: t=oogtint(X-(x0-xs),Y) or 6
            o[Y,X]=t
        gx,gy=(x0+1,y0+1) if gl=='lb' else (x0+1,y0+2)
        o[gy,gx]=5
        if pat is not R44 or x0!=30:   # linkeroog: raakt het de gezichtsrand (buitenlijn 1/2 direct ernaast)?
            rand.append(any(r2[Y,X+dx] in (1,2) and (X+dx,Y) not in V and not invak(X+dx,Y) or (X+dx==21) for X,Y in V for dx in (-1,)))
    assert all(((o!=r2)&~np.array([[invak(X,Y) for X in range(64)] for Y in range(64)])).ravel()==False)
    return o,rand
uit={}
for lv in ('a','a1','b','c'):
    for gl in ('lb','onder'):
        o,rand=bouw(lv,gl); n=U+'oog_R_%s_%s.png'%(lv,gl); opslaan(o,n); uit[(lv,gl)]=o
        print(n,'| linkeroog raakt gezichtsrand:', 'ja' if rand[0] else 'nee','| diff t.o.v. r2: %d px (alleen oogvakken)'%(o!=r2).sum())
BEST=('a1','lb')
opslaan(uit[BEST],U+'sneeuwmonster_r3.png')

# ---------- vel ----------
def rgbo(o,bg=(255,255,255)):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
M=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return M.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def grid(a,z):
    d=ImageDraw.Draw(a)
    for x in range(0,a.width,z): d.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    return a
ok=(19,19,37,29); z=12; w=(ok[2]-ok[0])*z; h=(ok[3]-ok[1])*z
tegels=[('r2',r2)]+[('%s, glans %s'%(lv,'linksboven' if gl=='lb' else 'onder'),uit[(lv,gl)]) for lv in ('a','a1','b','c') for gl in ('lb','onder')]+[('model',None)]
cols=3; rows=(len(tegels)+cols-1)//cols
B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8
V=Image.new('RGB',(max(cols*(w+10),2*W8+20),rows*(h+22)+H8+40+80),'white'); d=ImageDraw.Draw(V)
for i,(t,o) in enumerate(tegels):
    x=(i%cols)*(w+10); y=(i//cols)*(h+22)
    a=mcrop(*ok,z) if o is None else grid(rgbo(o).crop(ok).resize((w,h),Image.NEAREST),z)
    d.text((x+2,y+2),t+(' (gekozen)' if o is not None and (o is uit[BEST]) else ''),fill=(200,0,0)); V.paste(a,(x,y+16))
y=rows*(h+22)+10; best=uit[BEST]
d.text((2,y),'beste combinatie %s, glans %s, 8x | model 8x | 1x'%BEST,fill=(200,0,0))
V.paste(rgbo(best).crop(B).resize((W8,H8),Image.NEAREST),(0,y+14)); V.paste(mcrop(*B,8),(W8+10,y+14))
x=0
for bg in [(255,255,255),(248,248,232),(40,48,56),(24,24,24)]: V.paste(rgbo(best,bg),(x,y+H8+24)); x+=72
V.save(U+'vel.png'); print(U+'vel.png',V.size)
