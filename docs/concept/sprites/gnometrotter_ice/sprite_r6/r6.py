# r6.py: Gnometrotter Ice r6 uit r5 (23 nov). Logt elke gewijzigde pixel per zone (r6_log.txt).
# 1. keuring r5 reparatie 1 (sikkel 6) en 2 (neusklont weg). 2. benen: facetgrenzen op de modellijnen
# (alleen de grenzen komen uit het model; per facet volume 11 linksboven / 10 midden / 9 sikkel rechts-onder,
# barsten als lichte naad 11). Silhouet, zolen, muts, baard, rechterhand: 0 px.
import numpy as np, os; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'../sprite_r5/gnometrotter_ice.png')); o=np.asarray(im).copy(); n=o.copy()
zone={}
def zet(x,y,v,z):
    if n[y,x]!=v: n[y,x]=v; zone[(x,y)]=z
N4=((1,0),(-1,0),(0,1),(0,-1))

# ---- 1. keuring r5 ----
for x,y in ((48,29),(47,30),(46,31),(45,32),(44,33),(43,33),(42,34),(41,34)): zet(x,y,6,'sikkel')
for x,y in ((14,20),(14,21),(15,21),(15,22)): zet(x,y,0,'neusklont')

# ---- 2. benen ----
BLUE=(9,10,11)
# delen (spritecoordinaten): linkerdij, kruis, rechterdij, linkervoetbal, rechtervoetbal
DELEN={'dij L':(19,28,42,49),'kruis':(29,37,42,48),'dij R':(38,49,40,49),'voet L':(16,27,50,53),'voet R':(40,49,50,55)}
deel=np.full((64,64),'',object)
for k,(x0,x1,y0,y1) in DELEN.items():
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if o[y,x] in BLUE: deel[y,x]=k
# lijnen uit het model (gelezen op het model, spritecoordinaten): lichte barsten en (kruis) de donkere zitnaad
BARST={'dij L':[[(18.4,45.9),(23.0,47.3),(27.5,47.3)],[(22.9,43.6),(23.0,47.3),(23.5,50.0)]],
       'dij R':[[(44.5,41.5),(45.6,47.2)],[(38.5,47.6),(45.9,47.2)],[(45.9,47.2),(49.9,44.9)],[(45.9,47.2),(47.0,50.0)]],
       'voet L':[[(19.6,51.3),(19.9,54.4)]],
       'voet R':[[(47.1,51.2),(48.0,55.7)]]}   # alleen de duidelijkste van de twee modelbarsten (twee gaven strepen)
DONKER={}
def raster(pl):   # 1 px per rij (steile lijn) of per kolom (vlakke lijn): de lijn buigt mee, geen dubbele pixels
    s=set()
    for (x0,y0),(x1,y1) in zip(pl,pl[1:]):
        if abs(y1-y0)>=abs(x1-x0):
            for y in range(int(np.floor(min(y0,y1))),int(np.floor(max(y0,y1)))+1):
                t=(y+.5-y0)/(y1-y0); s.add((int(np.floor(x0+(x1-x0)*min(1,max(0,t)))),y))
        else:
            for x in range(int(np.floor(min(x0,x1))),int(np.floor(max(x0,x1)))+1):
                t=(x+.5-x0)/(x1-x0); s.add((x,int(np.floor(y0+(y1-y0)*min(1,max(0,t))))))
    return s
def structuur(x,y):   # bestaand lijnwerk in 9 blijft: 9 dat raakt aan buitenrand, riem, baard, zool of een ander deel,
    # en de donkere zitnaad van het kruis (modellijn) die er al ligt
    if o[y,x]!=9: return False
    if deel[y,x]=='kruis': return True
    return any(o[y+b,x+a] not in BLUE or (deel[y+b,x+a]!=deel[y,x]) for a,b in N4)
for k in DELEN:
    M=(deel==k)
    for y,x in np.argwhere(M):
        if structuur(x,y): M[y,x]=False
    lijn=set(); naad=set()
    for pl in BARST.get(k,[]): lijn|=raster(pl)
    for pl in DONKER.get(k,[]): naad|=raster(pl)
    lijn={p for p in lijn if M[p[1],p[0]]}; naad={p for p in naad if M[p[1],p[0]]}
    # volume per deel (Gen 3 bol): 11 linksboven, 10 midden, 9 als sikkel rechtsonder langs de vorm;
    # daarop de modelbarsten als lichte naad (11); steile barsten met 1 px schaduwkant (een tint donkerder) rechts ernaast,
    # zodat de facetgrens als ijsribbe leest en meebuigt met de modellijn.
    P=np.argwhere(M)
    if len(P)==0: continue
    y0,x0=P.min(0); y1,x1=P.max(0); w=max(1,x1-x0); h=max(1,y1-y0)
    for y,x in P:
        u=(x-x0)/w+(y-y0)/h
        v=11 if u<0.6 else (10 if u<1.6 else 9)
        if o[y+1,x]==1 or o[y,x+1]==1: v=9 if u>=0.6 else 10
        zet(x,y,v,'benen')
    for pl in BARST.get(k,[]):
        (xa,ya),(xb,yb)=pl[0],pl[-1]; steil=abs(yb-ya)>=abs(xb-xa)
        for x,y in raster(pl):
            if not M[y,x]: continue
            zet(x,y,11,'benen')
            sx,sy=(x+1,y) if steil else (x,y+1)
            if steil and M[sy,sx] and (sx,sy) not in raster(pl):   # vlakke barsten zonder schaduwrij (anders weer een band)
                zet(sx,sy,{11:10,10:9,9:9}[n[sy,sx]],'benen')

# ---- uitvoer + log ----
out=Image.fromarray(n.astype('uint8'),'P'); out.putpalette(im.getpalette())
out.save(os.path.join(H,'gnometrotter_ice.png'),transparency=0)
out.resize((512,512),Image.NEAREST).save(os.path.join(H,'gnometrotter_ice_8x.png'),transparency=0)
tel={}
with open(os.path.join(H,'r6_log.txt'),'w') as fh:
    for Y in range(64):
        for X in range(64):
            if n[Y,X]!=o[Y,X]:
                z=zone.get((X,Y),'rest'); tel[z]=tel.get(z,0)+1; fh.write('%s (%d,%d) %X -> %X\n'%(z,X,Y,o[Y,X],n[Y,X]))
print('t.o.v. r5 per zone:',tel,'| silhouet t.o.v. r5:',int(((n>0)!=(o>0)).sum()))
