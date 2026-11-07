"""Onderlaag r3: Gemini-plaatje verkleind op silhouet_r2 (schaal 1:9,97, offset 1,10), gekwantiseerd naar het palet (alleen vlaktinten + 1)."""
import sys, numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
sys.path.insert(0,D+'kleur_r3'); from palet import PAL
src=Image.open(D+'referenties/gemini_gekozen_ronde6.png').convert('RGB')
x0,y0,S,ox,oy=np.load(D+'silhouet/meta.npy')
c=src.crop((int(x0),int(y0),int(x0+62*S),int(y0+53*S))).resize((62,53),Image.BOX)
f=Image.new('RGB',(64,64),'white'); f.paste(c,(int(ox),int(oy))); f.save(D+'kleur_r3/gemini64.png')
a=np.array(f).astype(float)
sil=[l.rstrip('\n') for l in open(D+'silhouet/silhouet_r2.txt')][:64]
KAND='1345679ABC'
out=[]
for y in range(64):
    s=''
    for x in range(64):
        if sil[y][x]!='#': s+='.'; continue
        best=min(KAND,key=lambda k:sum((a[y,x,i]-PAL[int(k,16)][i])**2 for i in range(3)))
        s+=best
    out.append(s)
open(D+'kleur_r3/onderlaag.txt','w').write('\n'.join(out)+'\n')
