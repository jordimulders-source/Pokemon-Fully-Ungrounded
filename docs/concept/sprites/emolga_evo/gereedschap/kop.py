# Kop 1,4x (optie A, Jordi 23 nov) op modelniveau: kopmasker = polygoon P['r6b'] uit model/kop_opties/plak.py (natief omgerekend)
# en alleen modelpixels (niet-achtergrond). Rechterzijde verbreed tot en met de zwarte kopomlijning van het model (kolom 38-39),
# zodat de kopomtrek daar de modellijn volgt i.p.v. de polygoon. Anker: onderkant-midden van de kop (kin) blijft op zijn plek.
import numpy as np; from PIL import Image, ImageDraw
from gemeen import klassen
from reduceer import reduceer
P=10.238; C0=9.35+0.5
POLY=[(45,60),(100,90),(140,190),(185,140),(215,60),(250,50),(255,140),(235,200),(255,260),(250,330),(205,392),(95,392),(65,330),(75,250),(55,150)]
# rechterzijde (235,200)-(255,260)-(250,330): verbreed naar de kopomlijning (model K op natief x38-39, y67-80)
POLY_A=[(45,60),(100,90),(140,190),(185,140),(215,60),(250,50),(255,140),(250,200),(262,260),(258,330),(205,392),(95,392),(65,330),(75,250),(55,150)]
# Natieve kopomtrek (u,v; cel (u,v) heeft midden u+0,5): volgt de modellijnen. Verre oor + kop + nabije oor; NIET de armband
# van de linkervleugel tussen de oren (natief x28-31, y54-66). Nabije oor: linkeromlijning K (34,54)-(31,57)-(29,61)-(28,63..67),
# kapje bovenaan (35-38, 52-53), rechteromlijning K (38, 53-61)-(37, 62-66); kop rechts: K (37,68)-(38,69)-(39, 70-77).
NATPOLY=[(17,52.5),(20.5,52.5),(27.5,65.6),(28,66),(28,63),(29,62.9),(29,60),(29.8,59.2),(30.6,58.2),(31,57.2),(32,56.3),(33.2,55.4),
         (33.7,54.3),(35.1,53),(36.6,53),(37,52),(39,52),(39,61.2),(38.4,62.8),(38.2,64.9),(37.2,65.1),(37.2,67.8),(38,69),(39,69.9),(40,70.2),(40,86),(17,86)]
def kopmasker_natief(poly=NATPOLY,shape=(99,99)):
    out=np.zeros(shape,bool); n=len(poly)
    for v in range(shape[0]):
        for u in range(shape[1]):
            x,y=u+0.5,v+0.5; ins=False
            for i in range(n):
                x1,y1=poly[i]; x2,y2=poly[(i+1)%n]
                if (y1>y)!=(y2>y) and x<x1+(y-y1)*(x2-x1)/(y2-y1): ins=not ins
            out[v,u]=ins
    return out
def kopmasker(poly=POLY_A,shape=(99,99)):
    # polygoon in 1024-coordinaten (crop-offset 150,500) -> natieve cellen (celmidden binnen de polygoon)
    m=Image.new('L',(1024,1024),0); ImageDraw.Draw(m).polygon([(x+150,y+500) for x,y in poly],fill=255)
    m=np.asarray(m)
    out=np.zeros(shape,bool)
    for v in range(shape[0]):
        for u in range(shape[1]):
            x=int(C0+(u+0.5)*P); y=int(C0+(v+0.5)*P)
            if 0<=x<1024 and 0<=y<1024: out[v,u]=m[y,x]>0
    return out
def kop_sprite(S,OX,OY,schaal=1.4):
    a,c,L=klassen()
    mk=kopmasker_natief()&(c>0)
    vv,uu=np.where(mk)
    cx=(uu.min()+uu.max()+1)/2; bot=vv.max()+1
    X=OX+cx*S; Y=OY+bot*S          # ankerpunt in de sprite (zoals in A0)
    Sh=S*schaal; OXh=X-cx*Sh; OYh=Y-bot*Sh
    ck=np.where(mk,c,0)
    o,cov=reduceer(ck,Sh,OXh,OYh,10)
    # oude kop in A0 (voor de kopzone)
    o0,_=reduceer(ck,S,OX,OY,10)
    return o,o0,(Sh,OXh,OYh),mk
def kopmodel(schaal=1.4,uit=None):
    # Referentie op modelniveau (1024, zelfde coordinaten als model.png): kop (natief masker, omgerekend) 1,4x om de kin geplakt.
    from gemeen import D as MAP
    m=Image.open(MAP+'model/model.png').convert('RGB'); A=np.asarray(m)
    a,c,L=klassen(); mk=kopmasker_natief()&(c>0)
    vv,uu=np.where(mk); cx=(uu.min()+uu.max()+1)/2; bot=vv.max()+1
    yy,xx=np.mgrid[0:1024,0:1024]
    u=np.floor((xx-C0)/P).astype(int); v=np.floor((yy-C0)/P).astype(int)
    ok=(u>=0)&(u<99)&(v>=0)&(v<99)
    m1=np.zeros((1024,1024),bool); m1[ok]=mk[v[ok],u[ok]]
    m1&=A.min(2)<235
    ax=C0+cx*P; ay=C0+bot*P
    # inverse mapping: doelpixel -> bronpixel
    sx=np.round(ax+(xx-ax)/schaal).astype(int); sy=np.round(ay+(yy-ay)/schaal).astype(int)
    ok2=(sx>=0)&(sx<1024)&(sy>=0)&(sy<1024)
    src=np.zeros((1024,1024),bool); src[ok2]=m1[sy[ok2],sx[ok2]]
    out=A.copy(); out[src]=A[sy[src],sx[src]]
    im=Image.fromarray(out)
    if uit: im.save(uit)
    return im
