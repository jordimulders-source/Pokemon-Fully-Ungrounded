# Bewijs bevroren zones (diff 0) + wijzigingen per zone, kleuren, helderheidsstappen en hue per ramp.
import os, sys, colorsys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from meet import BASIS
a0=Image.open(BASIS); b0=Image.open(os.path.join(H,'ludicolo_gaucho_e.png'))
a=np.array(a0); b=np.array(b0); pal=np.array(b0.getpalette()[:48]).reshape(16,3); pal0=np.array(a0.getpalette()[:48]).reshape(16,3)
print('formaat',b0.size,b0.mode,'| transparant index',b0.info.get('transparency'))
print('alpha-diff (silhouet)',int(((a>0)!=(b>0)).sum()))
zones={'linkeroog (x19-23, y24-28)':(19,24,24,29),'rechteroog (x26-30, y24-29)':(26,31,24,30),'snavel/mond (x15-35, y27-34)':(15,36,27,35),
       'heel gezichtsvak (x15-35, y22-34)':(15,36,22,35)}
for n,(x0,x1,y0,y1) in zones.items(): print('  diff %-40s'%n, int((a[y0:y1,x0:x1]!=b[y0:y1,x0:x1]).sum()))
print('  zwart/olijf/rode lijn/oog-licht in het palet ongewijzigd:', all((pal[k]==pal0[k]).all() for k in (1,2,7,8,9,10,11)))
P=np.load(os.path.join(H,'..','sprite','r1','poncho_masker.npy'))
GEZ=np.zeros((64,64),bool); GEZ[22:35,15:36]=True
zz={'hoed (y<=25)':np.s_[:26,:],'poncho (masker)':None,'romp/armen/benen buiten poncho (y>=26)':np.s_[26:,:]}
for n,sl in zz.items():
    m=np.zeros((64,64),bool)
    if sl is None: m=P.copy()
    else: m[sl]=True; m&=~P
    m&=~GEZ; print('  gewijzigd %-42s'%n,int(((a!=b)&m).sum()),'van',int(((b>0)&m).sum()))
print('totaal gewijzigd',int((a!=b).sum()),'| kleuren incl. transparant',len(np.unique(b)),'| indexen',sorted(np.unique(b).tolist()))
print('zwart-aandeel %.1f%% -> %.1f%%'%(100*(a==1).sum()/(a>0).sum(),100*(b==1).sum()/(b>0).sum()))
L=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2]
for naam,ramp in (('rood (lijn, diep, donker, mdonker, midden, licht)',[2,3,4,5,6,7]),('olijf (lijn, diep, donker, midden)',[8,9,10,11]),('geel (donker, licht)',[12,13])):
    print(naam)
    for k in ramp:
        h,s_,v=colorsys.rgb_to_hsv(*(pal[k]/255))
        print('   %2d was %-15s nu %-15s L%3.0f -> %3.0f  hue %2.0f  n=%d'%(k,tuple(pal0[k].tolist()),tuple(pal[k].tolist()),L(pal0[k]),L(pal[k]),360*h,(b==k).sum()))
