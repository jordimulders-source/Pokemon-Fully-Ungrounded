# Bewijs bevroren zones (diff 0) + wijzigingen per zone, kleuren, helderheidsstappen en hue per ramp.
import os, colorsys, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
R2A=os.path.join(H,'..','sprite','r2','lombre_gaucho_r2_A.png')
a0=Image.open(os.path.join(H,'..','sprite','r3','lombre_gaucho_r3_A.png')); b0=Image.open(os.path.join(H,'lombre_gaucho_e.png'))
a=np.array(a0); b=np.array(b0); pal=np.array(b0.getpalette()[:48]).reshape(16,3); pal0=np.array(a0.getpalette()[:48]).reshape(16,3)
print('formaat',b0.size,b0.mode,'| transparant index',b0.info.get('transparency'))
print('alpha-diff (silhouet)',int(((a>0)!=(b>0)).sum()))
zones={'mond A5 (x17-29, y26-35)':(17,30,26,36),'ver oog (x20-23, y23-27)':(20,24,23,28),'nabij oog (x28-36, y23-29)':(28,37,23,30),
       'kopcontour/kaak (x17-38, y22-35, heel kopvak)':(17,39,22,36)}
for n,(x0,x1,y0,y1) in zones.items(): print('  diff %-46s'%n, int((a[y0:y1,x0:x1]!=b[y0:y1,x0:x1]).sum()))
print('  zwart/wit in het palet ongewijzigd:', (pal[1]==pal0[1]).all() and (pal[15]==pal0[15]).all())
KOP=np.zeros((64,64),bool); KOP[22:36,17:39]=True
zz={'hoed (y<=21)':np.s_[:22,:],'romp/armen (y22-47, buiten kopvak)':np.s_[22:48,:],'benen/voeten (y>=48)':np.s_[48:,:]}
for n,sl in zz.items():
    m=np.zeros((64,64),bool); m[sl]=True; m&=~KOP; print('  gewijzigd %-36s'%n,int(((a!=b)&m).sum()),'van',int(((b>0)&m).sum()))
print('totaal gewijzigd',int((a!=b).sum()),'| kleuren incl. transparant',len(np.unique(b)),'| indexen',sorted(np.unique(b).tolist()))
L=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2]
for naam,ramp in (('rood (lijn, schaduw, midden, licht)',[2,3,4,5]),('olijf (lijn, donker, midden, licht)',[6,7,9,10]),('hoedband (schaduw, licht)',[14,8]),('mond/nagels',[12,13])):
    print(naam)
    for k in ramp:
        h,s_,v=colorsys.rgb_to_hsv(*(pal[k]/255))
        print('   %2d was %-15s nu %-15s L%3.0f -> %3.0f  hue %2.0f'%(k,tuple(pal0[k].tolist()),tuple(pal[k].tolist()),L(pal0[k]),L(pal[k]),360*h))
