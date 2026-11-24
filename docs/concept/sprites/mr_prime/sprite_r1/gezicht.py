# Ogen + monocle. Ogen = Mr. Rime's eigen oogpixels (graphics/pokemon/mr_rime/front.png), omgekleurd naar grijs en
# verschoven naar de gemeten oogmiddens van r9: rechteroog dx=+7, linkeroog dx=+7/dy=-1 (r9-ogen staan op één hoogte).
# Leden/ogen uit Hitmonchan (Gen 3, graphics/pokemon/hitmonchan/anim_front_gba.png, rechteroog x32-38 rij 19-23).
import numpy as np; from PIL import Image; import monocle
RING=2   # toon van de monocle-ring
R=np.asarray(Image.open('../../../../../graphics/pokemon/mr_rime/front.png')).astype(int)
H=np.asarray(Image.open('../../../../../graphics/pokemon/hitmonchan/anim_front_gba.png')).astype(int)
OOGMAP={0xa:7, 6:6, 7:5, 0xb:0, 8:5}   # wit->248, oogschaduw (lichtblauw)->208, iris (oranje)->144, pupil (geel)->zwart, onderrand->144
def rime_oog(x0,x1,y0,y1,dx,dy):
    # pupilkolom van Rime is geel-wit-geel; het witte midden wordt ook zwart (anders leest de pupil als ':')
    return {(y+dy,x+dx):(0 if R[y,x]==0xa and R[y-1,x]==0xb and R[y+1,x]==0xb else OOGMAP[R[y,x]]) for y in range(y0,y1+1) for x in range(x0,x1+1) if R[y,x] in OOGMAP and 17<=y+dy<=21}
def _oud(x0,x1,y0,y1,dx,dy):
    return {(y+dy,x+dx):OOGMAP[R[y,x]] for y in range(y0,y1+1) for x in range(x0,x1+1) if R[y,x] in OOGMAP and 17<=y+dy<=21}
ROOG=rime_oog(29,35,15,21,7,1)      # -> x37-42, rij 17-21 (1 rij lager: witte rij onder de hoedrand)
LOOG=rime_oog(20,26,16,23,7,0)      # -> x28-32, rij 17-21
HMAP={15:0,1:7,14:1}
HOOG={(y,x):HMAP[H[y,x]] for y in range(19,24) for x in range(32,39) if H[y,x] in HMAP}
HLID=[(19,35),(19,36),(19,37),(20,33),(21,32)]
TOPK={}
for (y,x) in list(LOOG)+list(ROOG): TOPK[x]=min(TOPK.get(x,99),y)
def maak(C,var,log):
    C=C.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    # 1. oude ogen/ringen van de reductie weg -> gezichtswit (modelkleur)
    for y in range(16,21):
        for x in range(27,45):
            if C[y,x] not in (-1,6,7) or (C[y,x]==6 and x<=35): zet(y,x,7,'oogvlak schoon (r9-ogen + linkerring weg -> gezichtswit)')
    R_=lambda hx,hy: (hy-2, 41-(37-hx))          # Hitmonchan-rechteroog -> ons rechteroog (rechterrand x37->41)
    L_=lambda hx,hy: (hy-2, 28+(37-hx))          # gespiegeld -> ons linkeroog (buitenrand x37->28)
    if var in ('O1','O2'):
        for (y,x),v in list(LOOG.items())+list(ROOG.items()):
            if var=='O2' and y==TOPK[x]: v=0   # bovenste oogpixel per kolom zwart = recht lid (Rime-pixels, alleen kleur)
            if y==21 and C[y,x] not in (6,7): continue      # onderste oogrij: de snor ligt ervoor
            zet(y,x,v,'Rime-oog')
        if var=='O1':
            for f in (R_,L_):
                for (hy,hx) in HLID: zet(*f(hx,hy),0,'Hitmonchan-lid (links gespiegeld)')
                for hx in (33,34): zet(*f(hx,19),7,'boven het lid -> gezichtswit')
    elif var=='O3':
        for (hy,hx),v in HOOG.items():
            zet(*R_(hx,hy),v,'Hitmonchan-oog rechts'); zet(*L_(hx,hy),v,'Hitmonchan-oog links (gespiegeld)')
    # 2. monocle alleen rechts: modelring van r9 op factor 2.0, rijen >=16 (erboven ligt de hoedrand)
    for (y,x) in monocle.ring(2.0,sx=38.4,sy=19):
        if 16<=y<=21: zet(y,x,RING,'monocle (modelring, factor 2.0)')
    pass
    return C
