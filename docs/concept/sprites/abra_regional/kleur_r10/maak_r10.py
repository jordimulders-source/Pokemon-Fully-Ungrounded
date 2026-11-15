# maak_r10.py: ogen zachter (Jordi: "de ogen zijn nog wel wat hard met dat pure zwart, kan die iets zachter qua kleur?")
# Oogpixels: kern zwart (K=1), uiteinden lijnkleur L=2 (60,54,80). Varianten:
#  A: kern -> L (alle 8 oogpixels in de lijnkleur)
#  B: kern -> nieuwe tint tussen zwart en L (36,32,52) op een vrije index; uiteinden L
import numpy as np; from PIL import Image
OOG=[(22,28),(23,29),(24,30),(24,31),(30,27),(29,28),(28,29),(28,30)]
for bron in ['abra_r9','abra_r9_curve']:
    src=Image.open(f'../kleur_r9/{bron}.png'); a0=np.array(src).astype(int); pal=src.getpalette()
    gebruikt=set(np.unique(a0)); vrij=next(i for i in range(1,16) if i not in gebruikt)
    for v,(kleur) in [('A',None),('B',(36,32,52))]:
        a=a0.copy(); p=list(pal)+[0]*(768-len(pal))
        for x,y in OOG:
            if a[y,x]==1:
                if kleur is None: a[y,x]=2
                else: a[y,x]=vrij
        if kleur: p[3*vrij:3*vrij+3]=kleur
        im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(p)
        naam=bron.replace('r9','r10')+'_'+v; im.save(naam+'.png',transparency=0)
