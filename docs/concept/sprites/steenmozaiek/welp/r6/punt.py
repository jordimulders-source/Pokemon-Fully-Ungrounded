# Puntmeting van het originele model per spritepixel: majority-klasse in het middelste 50% van elke cel (orig = 99.3+16.9x, 191.5+16.9y).
import numpy as np
from PIL import Image
m=np.asarray(Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')).astype(int); k=16.896
def klas(c):
    r,g,b=c; l=0.299*r+0.587*g+0.114*b
    if l>238: return 'W' if min(c)>238 else 'g'
    if l<40: return 'K'
    if r>200 and g<150: return 'T'
    if max(c)-min(c)<22 and l>120: return 'g'
    if b>g+8 and l>110: return 'R' if l>160 else 'Q'
    if r>190 and g>175 and b<185: return 'C'
    if l<62: return 'd'
    if l<80: return 'S'
    if l<120: return 'M'
    return 'L'
def kaart(x0,y0,x1,y1,f=0.25):
    out=[]
    for y in range(y0,y1):
        row=''
        for x in range(x0,x1):
            X0=int(99.3+(x+f)*k);X1=int(99.3+(x+1-f)*k);Y0=int(191.5+(y+f)*k);Y1=int(191.5+(y+1-f)*k)
            cnt={}
            for c in m[Y0:Y1,X0:X1].reshape(-1,3):
                if c.min()>235 and c.max()>245 and abs(c[0]-c[2])<10 and c.mean()>246: kk='.'
                else: kk=klas(tuple(c))
                cnt[kk]=cnt.get(kk,0)+1
            row+=max(cnt,key=cnt.get)
        out.append(row)
    return out
if __name__=='__main__':
    import sys
    b=tuple(map(int,sys.argv[1].split(','))) if len(sys.argv)>1 else (0,0,50,45)
    r5=np.load('welp_r5.npy'); ch='.KdSMLPQRgWCTG'
    for j,row in enumerate(kaart(*b)):
        y=b[1]+j; print('%2d %s   %s'%(y,row,''.join(ch[v] for v in r5[y,b[0]:b[2]])))
