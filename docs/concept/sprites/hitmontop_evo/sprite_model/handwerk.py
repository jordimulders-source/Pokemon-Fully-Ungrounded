# Sprite ronde 1, stap c: handwerk op kleur.npy (raster met de hand, per coördinaat).
import numpy as np
from PIL import Image
from kleur_pal import PAL, N, I
o=np.load('kleur.npy')
# 1. alle donkere 'oog'-pixels uit de render (plooischaduwen) terug naar de donkerste eigen toon
mat=lambda v: N[v][:2]
for y,x in zip(*np.nonzero(o==I['oog'])):
    nb=[mat(o[y+dy,x+dx]) for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)) if N[o[y+dy,x+dx]][:2] in ('br','bl','wi')]
    o[y,x]=I[(max(set(nb),key=nb.count) if nb else 'br')+'0']
# 2. ogen: Hitmontops eigen oog uit anim_front (F=zwart, 1=wit, E=grijs), pixel voor pixel
OOG=[".FF.","F1EF","FEFF"]
def stempel(x0,y0,pat,kaart):
    for dy,r in enumerate(pat):
        for dx,c in enumerate(r):
            if c in kaart: o[y0+dy,x0+dx]=I[kaart[c]]
for x0,y0 in ((22,35),(25,41)):
    stempel(x0,y0,OOG,{'F':'oog','1':'wi3','E':'wi1'})
# 3. binnenlijn: kop vóór de schouder/steunarm (donkerste bruin), kop als eigen ronde vorm
for x,y in ((28,30),(29,31),(30,32),(31,33),(32,34),(32,35),(33,36),(33,37),(33,38)):
    if N[o[y,x]][:2]=='br': o[y,x]=I['br0']
# 4. mond: één streepje (Jordi), diagonaal rechts van de ogen zoals in het model
for x,y in ((28,37),(29,38),(29,39)):
    o[y,x]=I['br0']
# 5. knot = rondje met witte band (Jordi): band tussen knot en kop
for y,c in ((33,'wi2'),(34,'wi3'),(35,'wi2'),(36,'wi2'),(37,'wi1')): o[y,18]=I[c]
# 6. klauwen (wit, klein): punt links aan de linkervoet, punt boven aan de rechtervoet
for x,y,c in ((9,7,'wi2'),(10,7,'wi3'),(9,8,'wi1'),(52,1,'wi2'),(52,2,'wi3'),(51,2,'wi1')): o[y,x]=I[c]
# 7. twee witte strepen op het shirt: rechte diagonalen evenwijdig aan de rechterrand (model)
def lijn(x0,y0,x1,y1):
    n=max(abs(x1-x0),abs(y1-y0)); return [(round(x0+(x1-x0)*k/n),round(y0+(y1-y0)*k/n)) for k in range(n+1)]
for (x0,y0,x1,y1),c in (((45,24,39,35),'wi2'),):
    for x,y in lijn(x0,y0,x1,y1):
        if N[o[y,x]][:2]=='bl': o[y,x]=I[c]
np.save('sprite.npy',o)
img=np.array([PAL[N[i]] for i in o.ravel()],np.uint8).reshape(64,64,3)
Image.fromarray(img).save('sprite.png'); Image.fromarray(img).resize((512,512),Image.NEAREST).save('sprite_8x.png')
