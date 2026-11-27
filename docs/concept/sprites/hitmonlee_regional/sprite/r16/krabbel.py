# Jordi's krabbel (jordi/krabbel_benen.png) -> spritecoordinaten. Schaal 10,02 px/spritepixel, offset (8,3) (gefit op ek3).
import numpy as np; from PIL import Image
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/'
S,OX,OY=10.02,8.0,3.0
k=np.array(Image.open(D+'jordi/krabbel_benen.png').convert('RGB')).astype(int)
R,G,B=k[...,0],k[...,1],k[...,2]
yel=(R>170)&(G>150)&(B<70)
grn=(G>190)&(R<180)&(B<180)&(G-R>60)
def lijnen(M,minpx=30):
    lab,n=ndimage.label(M,np.ones((3,3)))
    out=[]
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(ys)<minpx: continue
        out.append(((xs-OX)/S,(ys-OY)/S))
    return out
if __name__=='__main__':
    for nm,M in (('GEEL',yel),('GROEN',grn)):
        for j,(sx,sy) in enumerate(lijnen(M)):
            print(nm,j,'x %.1f-%.1f y %.1f-%.1f'%(sx.min(),sx.max(),sy.min(),sy.max()))
            if nm=='GEEL':
                for y in range(int(sy.min()),int(sy.max())+1):
                    m=(sy>=y)&(sy<y+1)
                    if m.any(): print('   rij %d  x=%.2f'%(y,sx[m].mean()))
