# Modelhelderheid per spritepixel: het gespiegelde, geschrapte model (../sprite_r1/geschrapt.npz, 62x60) staat in de
# sprite op x+1, y+2 (silhouetdiff 14 px = alleen de oogbulten van E2). -> mlum.npy (64x64, nan = buiten het model)
import numpy as np
z=np.load('../sprite_r1/geschrapt.npz'); N=z['N'].astype(int)
L=np.full((64,64),np.nan); L[2:62,1:63]=(N*[299,587,114]).sum(2)/1000
L[2:62,1:63][z['air']]=np.nan
np.save('mlum.npy',L)
if __name__=='__main__':
    from zones import laad, YEL
    im,a=laad()
    for nm,m in (('geel',np.isin(a,YEL)),):
        v=L[m&~np.isnan(L)]; print(nm,'model-lum: n',len(v),'p10/50/90',np.percentile(v,[10,50,90]).round(1))
