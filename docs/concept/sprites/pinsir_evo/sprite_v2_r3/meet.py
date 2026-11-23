# Helderheid per vlak (zonder lijn- en buitenlijnpixels): sprite (paletkleur) tegen model (modelcellen van dezelfde pixels, zonder lijncellen).
import sys, numpy as np
sys.path.insert(0,'sprite_v2'); sys.path.insert(0,'sprite_v2_r3')
from reductie import *
from onderdelen import kaart as delenkaart
from scipy import ndimage as nd
from PIL import Image
cx,cy=kaart(0.3,0.3); OY=63-cy[88]
inv={}
for y in range(H):
    for x in range(W): inv.setdefault((cy[y]+OY,cx[x]),[]).append((y,x))
LIJNCEL=(K==1)|(K==2)|BG
Lnat=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
def meet(pad):
    im=Image.open(pad); I=np.array(im); pal=np.array(im.getpalette()[:3*16]).reshape(-1,3)
    Lp=pal@np.array([0.299,0.587,0.114])
    SIL=I>0; RAND=SIL&~nd.binary_erosion(SIL,np.array([[0,1,0],[1,1,1],[0,1,0]]),border_value=0)
    D=delenkaart(); D[~SIL]=''
    vlak=SIL&~RAND&~np.isin(I,(1,2,9))
    rows=[]
    VL={'kopschild':D=='kopschild','schouder':D=='schouder','schouderkoepel':D=='schouderkoepel','nabije_arm':D=='nabije_arm',
        'verre_arm':D=='verre_arm','nabije_dij':D=='nabije_dij','knie':D=='knie','nabije_voet':D=='nabije_voet','verre_been':D=='verre_been',
        'staart':D=='staart','rug':D=='rug','buik (room)':np.isin(I,(6,7,8))&(D=='')&(np.arange(64)[:,None]>32),'kaken (rood)':np.isin(I,(10,11,12))}
    for n,m in VL.items():
        m=m&vlak
        if n not in ('buik (room)','kaken (rood)'): m&=np.isin(I,(3,4,5,14))
        if not m.any(): continue
        sp=Lp[I[m]].mean()
        cl=[c for y,x in zip(*np.where(m)) for c in inv.get((y,x),[]) if not LIJNCEL[c]]
        mo=np.mean([Lnat[c] for c in cl]) if cl else float('nan')
        rows.append((n,int(m.sum()),sp,mo))
    return rows
if __name__=='__main__':
    for p in sys.argv[1:]:
        print(p)
        for n,c,sp,mo in meet(p): print('  %-15s %4d px  sprite %5.1f  model %5.1f  verschil %+5.1f'%(n,c,sp,mo,sp-mo))
