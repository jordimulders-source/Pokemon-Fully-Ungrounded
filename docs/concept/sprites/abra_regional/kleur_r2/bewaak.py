# bewaak.py NIEUW.png: silhouet van r1 is bevroren; alleen in de handenzone (x 18-37, y 46-58) mag het veranderen.
import sys; from PIL import Image; import numpy as np
a=np.array(Image.open('../kleur_r1/abra_r1.png')); b=np.array(Image.open(sys.argv[1]))
d=(a>0)!=(b>0); zone=np.zeros_like(d); zone[46:59,18:38]=True
buiten=int((d&~zone).sum()); binnen=[(int(x),int(y),'erbij' if b[y,x] else 'weg') for y,x in zip(*np.where(d&zone))]
print('silhouet-diff buiten de handenzone:',buiten); print('silhouet-diff in de handenzone:',len(binnen),binnen)
tot=(b>0).sum(); print('bijna-zwart (idx1): %.1f%%  lijnkleur (idx2): %.1f%%  kleuren: %d'%(100*(b==1).sum()/tot,100*(b==2).sum()/tot,len(set(b.ravel()))-1))
# open rand: vulkleur op de buitenrand
p=np.pad(b,1); o=[(int(x),int(y)) for y,x in zip(*np.where(b>2)) if 0 in (p[y,x+1],p[y+2,x+1],p[y+1,x],p[y+1,x+2])]
print('vulpixels op de buitenrand:',len(o),o)
# losse lijnpixels
l=[(int(x),int(y)) for y,x in zip(*np.where((b==1)|(b==2))) if (np.isin(p[y:y+3,x:x+3],[1,2]).sum()==1)]
print('losse lijnpixels:',l)
print('OK' if buiten==0 else 'FAIL'); sys.exit(0 if buiten==0 else 1)
