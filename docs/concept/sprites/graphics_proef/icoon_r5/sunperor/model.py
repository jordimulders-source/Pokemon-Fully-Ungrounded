"""r5: model = Gemini-driekwart nat_sunperor_icoon_p2.png (63x63 RGB, witte achtergrond), gekwantiseerd naar het frontpalet
(koningstiran/af/sapa_inca.png) -> model_idx.npy (63x63, 0 = transparant). Niets hertekend."""
import os,numpy as np
from PIL import Image
from scipy import ndimage as nd
H=os.path.dirname(os.path.abspath(__file__))+'/'
SRC=H+'../../nat_sunperor_icoon_p2.png'; FRONT=H+'../../../koningstiran/af/sapa_inca.png'
a=np.array(Image.open(SRC).convert('RGB')).astype(int)
P=np.array(Image.open(FRONT).getpalette()[:48]).reshape(16,3)
wit=(a.min(2)>=240)
lab,n=nd.label(wit); groot=[i for i in range(1,n+1) if (lab==i).sum()>6]
bg=np.isin(lab,groot)   # rand-wit en de ingesloten witte gaten (tussen staf/lijf, onder de vleugel); kleine witte plekken = oogwit
d=((a[:,:,None,:]-P[None,None,1:,:])**2).sum(3); idx=d.argmin(2)+1
idx[bg]=0
np.save(H+'model_idx.npy',idx.astype(np.uint8))
if __name__=='__main__':
    print('palet front:'); [print(k,P[k]) for k in range(16)]
    ys,xs=np.nonzero(idx); print('bbox',xs.min(),xs.max(),ys.min(),ys.max(),'maat',xs.max()-xs.min()+1,ys.max()-ys.min()+1)
    print('   '+''.join(str(i%10) for i in range(63)))
    for y in range(63): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in idx[y]))
