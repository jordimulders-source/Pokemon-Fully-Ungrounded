# Bouwt de sprite uit handgeschreven rijen (rij startkolom tekens). Controleert dat het silhouet exact
# gelijk is aan het verkleinde model (klassen63.npy). Ontbrekende rijen = placeholder (vlakke familiekleur).
import sys, numpy as np
from PIL import Image
PAL={'.':(0,0,0),'k':(41,24,41),'r':(140,49,57),
 'A':(255,247,189),'B':(255,222,106),'C':(238,180,65),'D':(205,128,57),'E':(156,90,41),
 'F':(255,164,82),'G':(238,112,57),'H':(197,71,49),
 'p':(255,189,197),'q':(238,130,150),'s':(180,72,100),'w':(255,255,255),'m':(99,41,66)}
ORDE='.krABCDEFGHpqswm'
R=np.load('klassen63.npy'); sil=R!='.'
G=np.full((63,63),'.',object)
filled=set()
for f in sys.argv[1:]:
    for ln in open(f):
        if not ln.strip(): continue
        y,x,s=ln.split(); y,x=int(y),int(x)
        for i,ch in enumerate(s): G[y,x+i]=ch
        filled.add(y)
fout=[]
for y in range(63):
    if y not in filled:
        for x in range(63):
            if sil[y,x]: G[y,x]={'o':'G','g':'C','p':'q','#':'k'}[R[y,x]]
    for x in range(63):
        if (G[y,x]!='.')!=sil[y,x]: fout.append((x,y,G[y,x],R[y,x]))
print('silhouetfouten:',fout[:40], len(fout))
img=np.zeros((64,64),'uint8')
for y in range(63):
    for x in range(63): img[y+1,x]=ORDE.index(G[y,x])
im=Image.fromarray(img,'P'); pal=[]
for c in ORDE: pal+=PAL[c]
im.putpalette(pal+[0]*(768-len(pal))); im.info['transparency']=0
im.save('kecleon_evo_r1.png',transparency=0)
rgb=im.convert('RGBA'); rgb.resize((512,512),Image.NEAREST).save('kecleon_evo_r1_8x.png')
