# r4 + poten uit r12 (lama naar de gespiegelde foto), geschaald en omgekleurd naar karamel
from PIL import Image; import numpy as np
a=np.array(Image.open('r4/r4_prompt_v4.png').convert('RGB')).astype(int)
B=Image.open('r12/r12_lama_foto.png').convert('RGB')
s=0.93; dx,dy=12,250; Y0=600   # r12-rijen vanaf Y0 = poten
Bs=np.array(B.resize((round(B.width*s),round(B.height*s)),Image.LANCZOS)).astype(int)
O=a.copy(); H,W=1024,1024
def white(p): return p.sum()>=700
# r4-poten wissen
O[865:,195:525]=255
O[812:,540:870]=255
for y in range(840,866):
    for x in range(195,525):
        r,g,b=a[y,x]
        if (r>110 and g<80) or (r<85 and abs(r-b)<18 and abs(r-g)<18): O[y,x]=255
# omkleuren: luminantie -> karamelverloop (donkere lijn blijft donker)
dark=np.array([62,34,22]); mid=np.array([176,118,72]); light=np.array([226,172,116])
def kleur(p):
    L=(0.3*p[0]+0.59*p[1]+0.11*p[2])/255
    if L<0.25: return dark+(mid-dark)*(L/0.25)*0.4
    t=(L-0.25)/0.75
    return mid+(light-mid)*min(1,t*1.15) if t>0.5 else dark+(mid-dark)*(0.4+0.6*t/0.5)
for y in range(round(Y0*s),Bs.shape[0]):
    for x in range(Bs.shape[1]):
        p=Bs[y,x]
        if white(p): continue
        X,Y=x+dx,y+dy
        if 0<=X<W and 0<=Y<H and white(O[Y,X]): O[Y,X]=kleur(p)
Image.fromarray(O.clip(0,255).astype('uint8')).save('poten/r4_poten_r12.png')
