# r2: zelfde raster als r1 (sprite_r1/rijen.txt = silhouet, lijnen, licht/schaduw), nieuwe tinten gemeten in het
# Gemini-model (palet_gemeten.json). Zones die in het model groen waren (groenzone.npy) worden oranje; de gele
# lijnen/strepen ernaast blijven geel. Handmatige pixelreparaties daarna: patch_r2.txt (regels "y x tekens").
import json, sys, numpy as np
from PIL import Image
P=json.load(open('palet_gemeten.json'))
ORDE='.krABCDEFmGHpqw'
RGB={'.':(0,0,0),'w':(255,255,255)}
for k in ORDE[1:]:
    if k!='w': RGB[k]=tuple(P[k]['rgb'])
R=np.load('../sprite_r1/klassen63.npy'); sil=R!='.'
S=np.full((63,63),'.',object)
for ln in open('../sprite_r1/rijen.txt'):
    y,x,s=ln.split(); y,x=int(y),int(x)
    for i,ch in enumerate(s): S[y,x+i]=ch
Z=np.load('groenzone.npy')
T=S.copy()
naar_oranje={'A':'F','B':'F','C':'m','D':'G','E':'r'}
for y in range(63):
    for x in range(63):
        c=S[y,x]
        if c=='s': T[y,x]='H'            # roze schaduw = lijfschaduw in het model (163,58,61 ~ 166,63,64)
        if Z[y,x] and c in naar_oranje: T[y,x]=naar_oranje[c]
# oranje tussentint: zalm (G) die aan licht oranje (F) grenst wordt m
T2=T.copy()
for y in range(63):
    for x in range(63):
        if T[y,x]=='G' and any(0<=y+dy<63 and 0<=x+dx<63 and T[y+dy,x+dx]=='F' for dy,dx in((1,0),(-1,0),(0,1),(0,-1))):
            T2[y,x]='m'
T=T2
try:
    for ln in open('patch_r2.txt'):
        ln=ln.split('#')[0].strip()
        if not ln: continue
        y,x,s=ln.split(); y,x=int(y),int(x)
        for i,ch in enumerate(s):
            assert T[y,x+i]!='.'; T[y,x+i]=ch
except FileNotFoundError: pass
assert ((T!='.')==sil).all(), 'silhouet gewijzigd'
img=np.zeros((64,64),'uint8')
for y in range(63):
    for x in range(63): img[y+1,x]=ORDE.index(T[y,x])
im=Image.fromarray(img,'P'); pal=[]
for c in ORDE: pal+=RGB[c]
pal+=[0,0,0]
im.putpalette(pal+[0]*(768-len(pal)))
im.save('kecleon_evo_r2.png',transparency=0)
im.convert('RGBA').resize((512,512),Image.NEAREST).save('kecleon_evo_r2_8x.png')
np.save('raster_r2.npy',T)
print('kleuren gebruikt',len(np.unique(img)))
