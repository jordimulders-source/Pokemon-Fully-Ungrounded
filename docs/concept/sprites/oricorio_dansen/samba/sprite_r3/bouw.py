# r3 = r1 oppoetsen ZONDER tekenen: alleen herkleuren (belijning, kleur, schaduw) + benoemde randpixels.
# Elke stap is een scherpe paletkeuze per pixel (geen blur/gemiddelden). Gebruik: python3 bouw.py
import numpy as np; from PIL import Image
from PIL import ImageDraw
R1=np.array(Image.open('../sprite_r1/samba.png')); PAL=Image.open('../sprite_r1/samba.png').getpalette()[:48]
H=W=64; T=0
PAL[11*3:12*3]=[206,226,110]   # 11 geelgroen licht (kuif)
PAL[15*3:16*3]=[246,238,150]   # 15 lichtgeel (gele reeks: 15 licht / 13 midden / 12 donker)
def poly(pts):   # pixelmiddens binnen de veelhoek (via 8x supersample)
    im=Image.new('L',(W*8,H*8),0); ImageDraw.Draw(im).polygon([(x*8,y*8) for x,y in pts],fill=1)
    return np.array(im)[4::8,4::8].astype(bool)
# bevroren: lijf+kop+oog+snavel (veelhoek langs de lijfrand van r1) en poten (rij >= 47)
BODY=poly([(19,22.5),(32.9,22.5),(32.9,38),(36,38.6),(37,47),(23,47),(19,42)])
BODY[22,24:29]=True   # kopbovenkant (lichte koppixels op rij 22)
FROZEN=BODY.copy(); FROZEN[47:,:37]=True
KUIF=np.zeros((H,W),bool); KUIF[15:22,24:34]=True; KUIF[14,24:26]=True
YY,XX=np.mgrid[0:H,0:W]
FAN=(XX>=20)&(XX<=40)&(YY<=22)&~KUIF | (XX>=33)&(XX<=40)&(YY<=30)&~BODY
FAN&=~FROZEN
WL=(XX<20)&~FROZEN&~FAN
WR=(XX>=33)&~FROZEN&~FAN
# onderste veren (donker 6/7 in r1) = dezelfde vleugel: per kant
LOWR=WR&((YY>=35)|((XX>=44)&(YY>=21)))
LOWL=WL&(YY>=34)
def nb4(a,y,x):
    for dy,dx in((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y+dy,x+dx; yield a[yy,xx] if 0<=yy<H and 0<=xx<W else 0
FILL=(3,4,5,6,7)
o=R1.copy(); LOG={}
EDIT=FAN|WL|WR|KUIF
def touches(mask,y,x,n8=False):
    d=((-1,0),(1,0),(0,-1),(0,1))+(((-1,-1),(-1,1),(1,-1),(1,1)) if n8 else ())
    return any(0<=y+a<H and 0<=x+b<W and mask[y+a,x+b] for a,b in d)
def step(naam,f):
    global o
    n0=o.copy(); f(); LOG[naam]=int((n0!=o).sum())
# S1: zwarte binnenlijnen in waaier/vleugels -> donkergroen (2); zwart blijft op de buitenrand en tegen het lijf (schaduw)
def s1():
    for y in range(H):
        for x in range(W):
            if EDIT[y,x] and not KUIF[y,x] and R1[y,x]==1 and not touches(R1==0,y,x,True) and not touches(FROZEN,y,x,True): o[y,x]=2
step('S1_binnenlijn_zwart_naar_donkergroen',s1)
# S2: onderste veren horen bij dezelfde vleugel: zelfde tintfamilie (6->5, 7->6)
def s2():
    m=LOWL|LOWR
    o[m&(R1==6)]=5; o[m&(R1==7)]=6
step('S2_onderveren_zelfde_familie',s2)
# S3: buitenlijn aan de lichtkant (licht linksboven) -> gekleurde selout (2); schaduwkant blijft zwart
def s3():
    for y in range(H):
        for x in range(W):
            if not (EDIT[y,x] and R1[y,x]==1): continue
            nx=ny=0
            for a in (-1,0,1):
                for b in (-1,0,1):
                    if (a or b) and (not(0<=y+a<H and 0<=x+b<W) or R1[y+a,x+b]==0): nx+=b; ny+=a
            if nx or ny:
                if -nx-ny>=2: o[y,x]=2
step('S3_selout_lichtkant',s3)
# S4: losse 1-px tintvlekjes in waaier/vleugels -> de tint die alle vulburen delen
def s4():
    for it in range(2):
        for y in range(H):
            for x in range(W):
                if not (EDIT[y,x] and not KUIF[y,x] and o[y,x] in FILL): continue
                nb=[v for v in nb4(o,y,x) if v in FILL]
                if len(nb)>=3 and o[y,x] not in nb and len(set(nb))==1: o[y,x]=nb[0]
step('S4_tintvlekjes',s4)
# S5: kuif onderscheiden: vulling lichter/geler (3->11), lijnen binnen de kuif olijf (12), rand van de kuif doorlopend zwart,
#     waaierpixels direct rond de kuif een tint donkerder
def s5():
    K=KUIF&(R1>0)
    old=o.copy()
    for y,x in zip(*np.where(K)):
        v=old[y,x]
        border=any(0<=y+a<H and 0<=x+b<W and old[y+a,x+b]>0 and not KUIF[y+a,x+b] for a,b in((-1,0),(1,0),(0,-1),(0,1)))
        if v in (3,4): o[y,x]=11
        elif v in (1,2,6,7): o[y,x]=1 if border else 12
    for y in range(H):
        for x in range(W):
            if FAN[y,x] and old[y,x]>0 and not KUIF[y,x]:
                near=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if 0<=y+a<H and 0<=x+b<W and KUIF[y+a,x+b] and old[y+a,x+b] in (3,4,13)]
                if near and old[y,x] in (3,4,5,6,7,2): o[y,x]=1 if any(a==0 or b==0 for a,b in near) else {3:6,4:6,5:7,6:7,7:2,2:2}[old[y,x]]
                elif touches(KUIF,y,x,True) and old[y,x] in (3,4): o[y,x]=6
step('S5_kuif',s5)
# S6: binnenlijnen tussen veren in een donkere tint van het vlak (niet zwart/donkst): lijn = donkerste vulbuur + 2 stappen
#     (3->5, 4->6, 5->7, 6/7->2). Buitenrand, lijfrand, kuifrand en geelrand blijven zoals ze zijn.
LIJN=np.zeros((H,W),bool)
def s6():
    old=o.copy()
    for y in range(H):
        for x in range(W):
            if not (EDIT[y,x] and not KUIF[y,x] and old[y,x] in (1,2)): continue
            if touches(R1==0,y,x,True) or touches(FROZEN,y,x,True) or touches(KUIF,y,x,True) or touches(np.isin(old,(12,13,15)),y,x,True): continue
            nb=[v for v in nb4(old,y,x) if v in FILL]
            if len(nb)<2: continue
            d=max(nb); o[y,x]={3:5,4:6,5:7}.get(d,2); LIJN[y,x]=True
step('S6_binnenlijn_tint_van_vlak',s6)
# S7: tintklusters van 1-2 px in waaier/vleugels -> de meest voorkomende vulbuur (scherpe paletkeuze)
def s7():
    from collections import Counter
    for it in range(2):
        for k in FILL:
            m=(o==k)&EDIT&~KUIF&~LIJN&np.isin(R1,FILL)
            seen=np.zeros_like(m)
            for y,x in zip(*np.where(m)):
                if seen[y,x]: continue
                st=[(y,x)]; seen[y,x]=1; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for c,d in((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                        if 0<=c<H and 0<=d<W and m[c,d] and not seen[c,d]: seen[c,d]=1; st.append((c,d))
                if len(pts)>2: continue
                cnt=Counter(o[c,d] for a,b in pts for c,d in((a-1,b),(a+1,b),(a,b-1),(a,b+1)) if 0<=c<H and 0<=d<W and o[c,d] in FILL and o[c,d]!=k and not LIJN[c,d])
                if cnt: 
                    v=cnt.most_common(1)[0][0]
                    for a,b in pts: o[a,b]=v
step('S7_tintklusters_1_2px',s7)
# S8: "een aantal veren wat meer geel": hele bestaande veren (hun vulpixels, binnen hun lijnen) naar de gele reeks,
#     met dezelfde licht-donkerverdeling (lichtste tint -> 15 als de veer licht 3 had, anders 13; daarna 13/12)
def veer(sy,sx,box):
    y0,y1,x0,x1=box; st=[(sy,sx)]; seen={(sy,sx)}
    while st:
        a,b=st.pop()
        for c,d in((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
            if y0<=c<=y1 and x0<=d<=x1 and (c,d) not in seen and o[c,d] in FILL and not LIJN[c,d]: seen.add((c,d)); st.append((c,d))
    return sorted(seen)
VEREN={'A':[('rechts_onder_geelband_verlengd',(39,45),(39,39,40,60)),('links_onder_onder_geel',(41,14),(40,42,10,18)),('links_onder_klein',(37,13),(36,38,10,16))],
       'B':[('linksboven_2e_vinger',(17,9),(13,23,8,13)),('rechtsboven_waaierveer',(18,48),(14,24,46,51)),('rechts_lange_veer',(32,53),(30,34,50,58))]}
def geel(opt):
    sets=[veer(*s,b) for _,s,b in VEREN[opt]]
    for p in sets:
        t=sorted(set(int(o[a,c]) for a,c in p)); ramp=[15,13,12] if 3 in t else [13,12,12]
        m={v:ramp[min(i,2)] for i,v in enumerate(t)}
        for a,c in p: o[a,c]=m[int(o[a,c])]
BASIS=o.copy()
