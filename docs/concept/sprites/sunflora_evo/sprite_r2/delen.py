# Knipt de delen: r1-hoofd (exact, incl. buitenlijn) en Sunflora-lijfdelen (frame 1, pixels exact).
# Alleen mechanisch: knippen, draaien in hele pixels (rot90). Niets getekend.
import sys, numpy as np; from PIL import Image; from scipy import ndimage
sys.path.insert(0,'../sprite_r1')
R1=np.load('../sprite_r1/r1_schoon.npy'); kop=np.load('../sprite_r1/kop_kaal.npy')
k=np.zeros((kop.shape[0]+2,kop.shape[1]+2),bool); k[1:-1,1:-1]=kop>0; k=ndimage.binary_dilation(k)  # kop + 1 px lijn (4-buren)
H=np.zeros((64,64),bool); H[0:k.shape[0],3:3+k.shape[1]]=k
H&=np.isin(R1,range(1,11))   # alleen kopkleuren (lijf lag erachter)
kopr1=np.where(H,R1,0); np.save('kop_r1.npy',kopr1); print('kop pixels',H.sum())
s=np.array(Image.open('../sprite_r1/sunflora_f1.png'))
MAP={1:1,12:11,13:12,14:13,15:14}
g=np.isin(s,[12,13,14,15]); bl=(s==1)&ndimage.binary_dilation(g,structure=np.ones((3,3)))
m=g|bl
def knip(y0,y1,x0,x1):
    b=np.where(m[y0:y1,x0:x1],s[y0:y1,x0:x1],0); return np.vectorize(lambda v: MAP.get(int(v),0))(b).astype('uint8')
romp=knip(32,48,12,52)        # armen + lijfje (rij 32-47, kol 12-51)
lv=knip(48,56,17,31)          # linkervoet (rij 48-55, kol 17-30)
rv=knip(48,56,31,46)          # rechtervoet (rij 48-55, kol 31-45)
np.save('romp.npy',romp); np.save('lv.npy',lv); np.save('rv.npy',rv)
ch='.123456789abcdef'
for nm,a in (('romp',romp),('lv',lv),('rv',rv),('lv_rot',np.rot90(lv,1)),('rv_rot',np.rot90(rv,-1))):
    print(nm,a.shape); [print(''.join(ch[v] for v in r)) for r in a]
