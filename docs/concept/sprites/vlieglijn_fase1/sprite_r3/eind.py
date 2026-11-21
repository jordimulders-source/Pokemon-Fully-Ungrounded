# r3 eindbouw: 50-breed raster -> 64x64, dan als laatste de twee extra verre poten (Jordi optie A):
# KOPIE van de eigen spritepoten 3 en 4 (ring + onderkabel + klauwtjes), verschoven naar achter/hoger,
# in schaduwtint, alleen op lege pixels (dus half verstopt achter de nabije poten en het achterlijf).
import numpy as np; from PIL import Image
from reduce_pal import PAL
CH='.#kdgGLcChWwvpor'
o=np.loadtxt('r3_stap1.txt',dtype=int); H,W=o.shape
X0=6; Y0=61-(H-1)
full=np.zeros((64,64),int); full[Y0:Y0+H,X0:X0+W]=o
# vleugelruis: losse modelspikkels (1 px, geen gelijke 4-buur) in de vleugels -> meest voorkomende buurtint
from collections import Counter
vr=0
for r in range(Y0,Y0+13):
    for c in range(X0+19,X0+W):
        v=full[r,c]
        if v in (0,1): continue
        nb=[full[r-1,c],full[r+1,c],full[r,c-1],full[r,c+1]]
        if v not in nb:
            k=[x for x in nb if x not in (0,1)]
            if k: full[r,c]=Counter(k).most_common(1)[0][0]; vr+=1
print('vleugelruis weg',vr)
basis=full.copy()
SCHADUW={CH.index('c'):CH.index('c'),CH.index('h'):CH.index('C'),CH.index('C'):CH.index('c'),
         CH.index('W'):CH.index('w'),CH.index('w'):CH.index('v'),CH.index('o'):CH.index('r'),
         CH.index('r'):CH.index('r'),1:1}
def kopie(r0,r1,c0,c1,dx,dy):
    n=0
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            v=o[r,c]
            if v in SCHADUW and v!=0:
                R,C=Y0+r+dy,X0+c+dx
                if 0<=R<64 and 0<=C<64 and full[R,C]==0 and basis[R,C]==0:
                    full[R,C]=SCHADUW[v]; n+=1
    return n
n1=kopie(30,32,21,27,6,-2)+kopie(33,45,21,31,6,-2)   # verre middenpoot = kopie poot 3, 6 naar achter, 2 hoger
n2=kopie(30,32,34,39,5,-3)+kopie(33,43,35,46,5,-3)   # verre achterpoot = kopie poot 4, 5 naar achter, 3 hoger
print('extra pootpixels',n1,n2)
np.savetxt('vlieg_r3.txt',full,fmt='%2d')
im=Image.fromarray(full.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL)))
im.save('vlieg_r3.png',transparency=0)
Image.fromarray(np.array(PAL)[full].astype('uint8')).resize((512,512),Image.NEAREST).save('vlieg_r3_8x.png')
with open('normal.pal','w') as f:
    f.write('JASC-PAL\r\n0100\r\n16\r\n'+''.join(f'{r} {g} {b}\r\n' for r,g,b in PAL))
ys,xs=np.where(full>0); print('breed',xs.max()-xs.min()+1,'hoog',ys.max()-ys.min()+1,'opp',(full>0).sum(),'onderste rij',ys.max(),'kleuren',len(set(full.ravel()))-1)
