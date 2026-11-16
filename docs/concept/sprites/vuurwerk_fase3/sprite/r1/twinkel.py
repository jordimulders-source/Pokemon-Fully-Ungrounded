# Overname-reparatie: de vijf twinkelsterretjes van het model werden bij de reductie vlekjes van 2-4 px.
# Model: vierpuntige kruisjes van ~3x3 spritepx (gemeten: hoogte 2,6-3,6, breedte 2,5-3,5), goud/tan met licht midden.
# Hier: plusje op het gemeten middelpunt, armen tan (3), midden lichtcreme (5) -- modelkleuren.
import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet.json')); IN,OUT=sys.argv[1],sys.argv[2]
a=np.asarray(Image.open(IN)).copy(); n=0
OUD=[(8,5),(9,6),(8,7),(8,6),(5,9),(5,10),(29,18),(29,19),(30,18),(20,26),(21,27),(20,27),(16,29),(17,29)]
for x,y in OUD:
    if a[y,x]: a[y,x]=0; n+=1
for cx,cy in [(8,6),(5,9),(29,18),(20,26),(16,29)]:
    for dx,dy,v in ((0,0,5),(1,0,3),(-1,0,3),(0,1,3),(0,-1,3)):
        if a[cy+dy,cx+dx]!=v: a[cy+dy,cx+dx]=v; n+=1
im=Image.fromarray(a,'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(OUT,transparency=0); print('twinkels: pixelwijzigingen',n)
