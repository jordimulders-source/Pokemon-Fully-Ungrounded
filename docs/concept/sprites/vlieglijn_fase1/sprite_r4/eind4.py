# r4 eindbouw: raster -> 64x64; als laatste de twee extra verre poten (optie A) als KOPIE van poot 3 en 4,
# in schaduwtint, iets hoger en naar achter, alleen op lege pixels (grotendeels achter de nabije poot).
import numpy as np, sys; from PIL import Image
from reduce_pal import PAL
CH='.#kdgGLcChWwvpor'
L=[l.rstrip('\n') for l in open('r4_stap1.chr') if l.strip()]
o=np.array([[CH.index(c) for c in l] for l in L]); H,W=o.shape
np.savetxt('r4_stap1.txt',o,fmt='%2d')
dx3,dy3,dx4,dy4=[int(v) for v in (sys.argv[1:5] if len(sys.argv)>4 else (0,-4,-1,-3))]
X0=6; Y0=61-(H-1)
full=np.zeros((64,64),int); full[Y0:Y0+H,X0:X0+W]=o; basis=full.copy()
S={CH.index(a):CH.index(b) for a,b in zip('chCWwvor#','cCcwvvrr#')}
def kopie(r0,r1,c0,c1,dx,dy):
    n=0
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            v=o[r,c]
            if v in S:
                R,C=Y0+r+dy,X0+c+dx
                if basis[R,C]==0 and full[R,C]==0: full[R,C]=S[v]; n+=1
    return n
n=kopie(27,45,22,31,dx3,dy3)+kopie(30,43,34,46,dx4,dy4)
print('extra pootpixels',n)
np.savetxt('vlieg_r4.txt',full,fmt='%2d')
im=Image.fromarray(full.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL)))
im.save('vlieg_r4.png',transparency=0)
Image.fromarray(np.array(PAL)[full].astype('uint8')).resize((512,512),Image.NEAREST).save('vlieg_r4_8x.png')
with open('normal.pal','w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n'+''.join(f'{r} {g} {b}\r\n' for r,g,b in PAL))
ys,xs=np.where(full>0); print('breed',xs.max()-xs.min()+1,'hoog',ys.max()-ys.min()+1,'opp',(full>0).sum(),'onderste rij',ys.max())
np.savetxt('_crop.txt',full[16:62,6:56],fmt='%2d')
