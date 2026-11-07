"""Stap 1 r7: gemini64.png (r6-schaal 1:10,78) binnen masker + dunne delen, gekwantiseerd naar het volledige r6-palet (ook lijnkleuren). Uitvoer: onderlaag.txt."""
import sys, numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/'
sys.path.insert(0,D); from palet import PAL
g=np.array(Image.open(D+'gemini64.png').convert('RGB')).astype(float)
sil=[l.rstrip('\n') for l in open(D+'silhouet_r7.txt')][:64]
def lab(c):
    c=np.array(c,float)/255; c=np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]]); xyz=M@c/np.array([0.9505,1,1.089])
    f=np.where(xyz>0.008856,np.cbrt(xyz),7.787*xyz+16/116); return np.array([116*f[1]-16,500*(f[0]-f[1]),200*(f[1]-f[2])])
K='123456789ABCF'; KL={k:lab(PAL[int(k,16)]) for k in K}
rows=[]
for y in range(64):
    s=''
    for x in range(64):
        t=sil[y][x]
        if t=='.': s+='.'; continue
        if t=='+': s+='B'; continue            # dunne delen (snorharen/pluimrafels): lijnkleur
        L=lab(g[y,x]); s+=min(K,key=lambda k:((KL[k]-L)**2).sum())
    rows.append(s)
open(D+'onderlaag.txt','w').write('\n'.join(rows)+'\n')
