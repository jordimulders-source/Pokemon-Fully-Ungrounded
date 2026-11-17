# Toegestane afwijkingen van Jordi, als bovenlaag na de overname:
# 1. "die glitterspikkels kan je wegdoen en dat worden dan vuurwerkspikkels": glitter is al weg (reductie.py deglitter +
#    middeling); op de glinsterplekken in het lijf (glitter.py) komt een vuurwerkspikkel: een stukje straal van 2 px
#    (lichtroze 8 -> fel creme 5 aan het eind), van de kop af wijzend (vonken vliegen naar buiten). Geen barst op het lijf.
# 2. "om het hoofd heen dan vuurwerk spikkels": Jordi's roze barst midden onder (ref_burst.json 'b2', natief raster 1:1)
#    gecentreerd op het midden van de kop, alleen op lege pixels met 1 px afstand tot de sprite (het silhouet blijft vrij).
#    Kleuren: donker -> donkermagenta 6, midden -> magenta 9, fel -> lichtroze 8.
import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet.json')); IN,OUT=sys.argv[1],sys.argv[2]
KOP=(13,16); SRC=sys.argv[3] if len(sys.argv)>3 else 'b2'
KLEUR={1:6,2:9,3:8}
a=np.asarray(Image.open(IN)).copy(); H,W=a.shape; orig=a.copy(); log={'lijfspikkels':0,'kopspikkels':0}
# 1
for (i,j,_) in json.load(open('glitter_plekken.json')):
    dx=np.sign(i-KOP[0]); dy=np.sign(j-KOP[1])
    for (x,y,v) in ((i,j,5),(i-dx,j-dy,8)):
        if orig[y,x] in (6,7,8,9,10,11,12) and a[y,x]!=v: a[y,x]=v; log['lijfspikkels']+=1
# 2
g=np.array(json.load(open('ref_burst.json'))[SRC]); gh,gw=g.shape
ys,xs=np.where(g>0); cy,cx=int(round(ys.mean())),int(round(xs.mean()))
vrij=orig==0
for y in range(H):
    for x in range(W):
        if not vrij[y,x]: continue
        if any(0<=y+dy<H and 0<=x+dx<W and orig[y+dy,x+dx]>0 for dy in (-1,0,1) for dx in (-1,0,1)): continue
        gy,gx=y-KOP[1]+cy,x-KOP[0]+cx
        if 0<=gy<gh and 0<=gx<gw and g[gy,gx]>0: a[y,x]=KLEUR[g[gy,gx]]; log['kopspikkels']+=1
im=Image.fromarray(a,'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(OUT,transparency=0); print(log)
