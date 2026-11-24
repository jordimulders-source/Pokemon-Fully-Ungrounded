import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
import k7b
a0,pal=laad('../k6/tempel.png'); H,W=a0.shape; k7b.a0=a0
LIJN={7,1}
LICHT={4:3,5:4,6:5}; DONKER={3:4,4:5,5:6,6:15}
vast=np.zeros_like(a0,bool)
for (x0,y0,x1,y1) in OGEN: vast[y0:y1+1,x0:x1+1]=True
vast|=deurmasker(a0)
vast[45:61,13:16]=True; vast[45:61,22:26]=True   # deurstijlen ongemoeid
isl=np.isin(a0,list(LIJN))
LH=np.zeros_like(a0,bool); LV=LH.copy(); DH=LH.copy(); DV=LH.copy()
TAPS=len(sys.argv)<2 or sys.argv[1]!='vol'
def strepen(mask_row):
    out=[];x=0;n=len(mask_row)
    while x<n:
        if mask_row[x]:
            s=x
            while x<n and mask_row[x]: x+=1
            out.append((s,x))
        else: x+=1
    return out
for y in range(H):
    for s,e in strepen(isl[y]):
        n=e-s
        if n<3: continue
        lo,hi=(s,s+int(np.ceil(2*n/3))) if (TAPS and n>=5) else (s,e)
        dlo=s+n//3 if (TAPS and n>=5) else s
        for u in range(lo,hi):
            if y+1<H: LH[y+1,u]=True
        for u in range(dlo,e):
            if y-1>=0: DH[y-1,u]=True
for x in range(W):
    for s,e in strepen(isl[:,x]):
        n=e-s
        if n<3: continue
        lo,hi=(s,s+int(np.ceil(2*n/3))) if (TAPS and n>=5) else (s,e)
        dlo=s+n//3 if (TAPS and n>=5) else s
        for v in range(lo,hi):
            if x+1<W: LV[v,x+1]=True
        for v in range(dlo,e):
            if x-1>=0: DV[v,x-1]=True
L=LH|LV; D=DH|DV
# hoeken verdikken: binnenhoek linksboven licht, rechtsonder donker
for y in range(1,H-1):
    for x in range(1,W-1):
        if LH[y,x] and LV[y,x] and not D[y+1,x+1]: L[y+1,x+1]=True
        if DH[y,x] and DV[y,x] and not L[y-1,x-1]: D[y-1,x-1]=True
a=a0.copy()
for y in range(H):
    for x in range(W):
        T=a0[y,x]
        if vast[y,x] or T not in DONKER: continue
        if L[y,x] and not D[y,x] and T in LICHT: a[y,x]=LICHT[T]
        elif D[y,x] and not L[y,x]: a[y,x]=DONKER[T]
a=k7b.filt(a)
np.save('auto.npy',a)
bewaar(a,pal,'tempel_auto.png'); print((a!=a0).sum())
from PIL import Image
def big(p):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',(64,64),(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB').resize((512,512),Image.NEAREST)
V=Image.new('RGB',(1034,512),(255,255,255)); V.paste(big('tempel_auto.png'),(0,0)); V.paste(big('../k6/tempel.png'),(522,0)); V.save('auto8.png')
