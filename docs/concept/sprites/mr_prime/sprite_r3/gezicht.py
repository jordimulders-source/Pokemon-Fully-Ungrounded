# r2 ogen + monocle + neus. Alles uit bestaande pixels:
#  E1 = oog van de kale reductie (modus-reductie van r9, linker grijze ring er al uit op het natieve raster),
#       rechts met de eigen modelring (= monocle, schaal 2.5 zoals de rest)
#  E2 = E1 + lid uit Hitmonchan (Gen 3 anim_front_gba.png, rechteroog: (19,35-37), (20,33), (21,32));
#       rechteroog het hele lid, linkeroog (verre oog, smal) alleen het rechte stuk van 3 px boven de pupil
#  E3 = Mr. Rime-ogen (front.png) omgekleurd + Hitmonchan-lid, 1 rij hoger dan in r1 (voorhoofd erboven),
#       met de modelring op factor 2.0 (anders past het Rime-oog er niet in)
#  neus: modelomlijning van het neusbolletje als selout 112 (cellen met >=2 grijze omlijningspixels in het model)
import numpy as np; from PIL import Image; import monocle
R=np.asarray(Image.open('../../../../../graphics/pokemon/mr_rime/front.png')).astype(int)
H=np.asarray(Image.open('../../../../../graphics/pokemon/hitmonchan/anim_front_gba.png')).astype(int)
M=np.load('kaal_mode_idx.npy'); OY=3
OOGMAP={0xa:7, 6:6, 7:5, 0xb:0, 8:5}
def rime_oog(x0,x1,y0,y1,dx,dy):
    return {(y+dy,x+dx):(0 if R[y,x]==0xa and R[y-1,x]==0xb and R[y+1,x]==0xb else OOGMAP[R[y,x]])
            for y in range(y0,y1+1) for x in range(x0,x1+1) if R[y,x] in OOGMAP and 16<=y+dy<=20}
ROOG=rime_oog(29,35,15,21,7,0); LOOG=rime_oog(20,26,16,23,7,-1)
HLID=[(19,35),(19,36),(19,37),(20,33),(21,32)]
def neus():
    a=np.asarray(Image.open('natief_kop.png').convert('L')).astype(int); cnt={}
    for y in range(63,70):
        for x in range(88,97):   # x<88 is de rechterrand van het linkeroog
            if 100<=a[y,x]<240:
                k=((2*y-50)//5+OY,(2*x-14)//5); cnt[k]=cnt.get(k,0)+1
    return [k for k,v in cnt.items() if v>=2]
def ring_vlak(F=2.5,sx=39,sy=18,thr=0.3,cx=104,cy=63):
    """r3: monocle = de zwarte modelring (natief_stok, straal 5-8.6 rond (104,63)) per spritecel bemonsterd
    (aandeel ringpixels in het vlak van de cel >= thr). Factor 2.5 = schaal van de rest. Geeft een ronde ring
    met lege hoekpixels."""
    a=np.asarray(Image.open('natief_stok.png').convert('L')).astype(int)
    yy,xx=np.mgrid[0:a.shape[0],0:a.shape[1]]; d=np.hypot(xx-cx,yy-cy)
    up=np.repeat(np.repeat((a<140)&(d>=5)&(d<=8.6),10,0),10,1).astype(float); out=[]
    for y in range(sy-5,sy+6):
        for x in range(sx-5,sx+6):
            x0=cx+(x-sx-0.5)*F; y0=cy+(y-sy-0.5)*F
            if up[int(y0*10):int((y0+F)*10), int(x0*10):int((x0+F)*10)].mean()>=thr: out.append((y,x))
    return out
def maak(C,var,log):
    C=C.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    if var in ('E1','E2'):
        for y in range(16,21):
            for x in range(27,46):
                if M[y-OY,x]!=-1: zet(y,x,M[y-OY,x],'oogvlak uit modus-reductie (modeloog)')
        if var=='E2':
            for (hy,hx) in HLID: zet(hy-2,hx+4,0,'Hitmonchan-lid rechts')
            for x in (29,30,31): zet(16,x,0,'Hitmonchan-lid links (recht stuk)')
    elif var=='E2r3':
        # r3 (keurder r2 punt 2-4): oogvlak leeg -> gezichtswit (alleen omkleuren), dan per oog
        # Hitmonchan-lid recht stuk (3 px, zwart) + pupil 1x2 uit het modeloog (zwart), monocle = modelring.
        for y in range(16,21):
            for x in range(28,45):
                if C[y,x]!=-1 and C[y,x]!=7: zet(y,x,7,'oogvlak leeg -> gezichtswit')
        for x in (29,30,31): zet(17,x,0,'Hitmonchan-lid recht stuk (verre oog)')
        for y in (18,19): zet(y,30,0,'pupil 1x2 uit modeloog (verre oog)')
        for (y,x) in ring_vlak():
            if 16<=y<=20: zet(y,x,1,'monocle: modelring factor 2.5, tint 48')
        for x in (38,39,40): zet(17,x,0,'Hitmonchan-lid recht stuk (monocle-oog)')
        for y in (18,19): zet(y,39,0,'pupil 1x2 uit modeloog (monocle-oog)')
        # neus: wit bolletje van de modusreductie (20,33-34) met de modelselout 112 boven/opzij
        for (y,x) in ((20,33),(20,34)): zet(y,x,7,'neusbolletje wit (modusreductie)')
        for (y,x) in ((19,33),(19,34),(20,32),(20,35)): zet(y,x,4,'neus: modelselout 112')
        return C
    elif var=='E3':
        for y in range(16,21):
            for x in range(27,45):
                if C[y,x] not in (-1,6,7) or (C[y,x]==6 and x<=35): zet(y,x,7,'oogvlak schoon -> gezichtswit')
        for (y,x),v in list(LOOG.items())+list(ROOG.items()): zet(y,x,v,'Rime-oog')
        R_=lambda hx,hy: (hy-3, 41-(37-hx)); L_=lambda hx,hy: (hy-3, 28+(37-hx))
        for f in (R_,L_):
            for (hy,hx) in HLID: zet(*f(hx,hy),0,'Hitmonchan-lid (links gespiegeld)')
            for hx in (33,34): zet(*f(hx,19),7,'boven het lid -> gezichtswit')
        for (y,x) in monocle.ring(2.0,sx=38.4,sy=18):
            if 16<=y<=21: zet(y,x,2,'monocle (modelring, factor 2.0)')
    for (y,x) in neus():
        if C[y,x] in (6,7): zet(y,x,4,'neusbolletje: modelomlijning als selout 112')
    return C
