# EM: kale reductie van alleen het modeloog, met een eigen rasterfase (hoogste zuiverheid in het oogvak).
# Klassen per modelpixel: Z zwart (L<70), W wit/lichtgrijs (L>=170, sat<40), Y geel; meerderheid per cel.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')).astype(int)
L=a.mean(2); sat=a.max(2)-a.min(2)
K=np.full(L.shape,'G'); K[L<70]='Z'; K[(L>=170)&(sat<40)]='W'; K[(sat>=60)&(a[...,0]>140)&(a[...,2]<120)]='Y'
P=15.36
def reduc(x0,y0,n=7):
    best=None
    for ox in range(16):
        for oy in range(16):
            s=0; g=[]
            for j in range(n):
                row=''
                for i in range(n):
                    blk=K[int(y0+oy+j*P):int(y0+oy+(j+1)*P),int(x0+ox+i*P):int(x0+ox+(i+1)*P)].ravel()
                    u,c=np.unique(blk,return_counts=True); s+=c.max()/c.sum(); row+=u[np.argmax(c)]
                g.append(row)
            if best is None or s>best[0]: best=(s/n/n,ox,oy,g)
    return best
if __name__=='__main__':
    # oogvakken (modelpixels): links x 325-435, rechts x 520-635, y 175-290
    for x0 in (322,520):
        b=reduc(x0,172); print('zuiverheid %.2f fase %d %d'%b[:3]); print('\n'.join(b[3])); print()
