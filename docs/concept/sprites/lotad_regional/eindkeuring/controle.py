# Bewijs beschermde zones: alpha-diff, oog-diff, wijzigingen per onderdeel, kleuren, helderheidsstappen en hue per ramp.
import sys, os, colorsys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from meet import fm
a0=Image.open(os.path.join(H,'..','sprite','r3','lotad_gaucho_oogG.png')); b0=Image.open(os.path.join(H,'lotad_gaucho_e.png'))
a=np.array(a0); b=np.array(b0); pal=np.array(b0.getpalette()[:48]).reshape(16,3)
print('formaat',b0.size,b0.mode,'| transparant index', b0.info.get('transparency'))
print('alpha-diff (silhouet)', int(((a>0)!=(b>0)).sum()))
print('oog-diff x18-33 y39-41', int((a[39:42,18:34]!=b[39:42,18:34]).sum()))
nm={2:'hoed',3:'kop',4:'snavel',5:'kraag',6:'poten'}
for m,n in nm.items(): print('  gewijzigd %-7s'%n, int(((a!=b)&(fm==m)).sum()), 'van', int((fm==m).sum()))
print('totaal gewijzigd', int((a!=b).sum()), '| kleuren incl. transparant', len(np.unique(b)), '| palet-indexen gebruikt', sorted(set(np.unique(b).tolist())))
L=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2]
for naam,ramp in (('terra (hoed/kop/poten)',[2,3,4,5]),('kraag',[6,7,8,9]),('snavel',[10,11])):
    print(naam, ' | '.join('%d %s L%.0f H%.0f S%.2f'%(k,tuple(pal[k].tolist()),L(pal[k]),360*colorsys.rgb_to_hsv(*(pal[k]/255))[0],colorsys.rgb_to_hsv(*(pal[k]/255))[1]) for k in ramp))
