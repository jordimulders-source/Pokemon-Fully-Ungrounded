"""r6-basis: Gemini-masker op schaal 1:10,8 incl. snorharen (geheel past in 64x64), dunne delen apart, onderlaag gekwantiseerd naar het palet."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
sys.path.insert(0,D+'kleur_r6'); from palet import PAL
src=Image.open(D+'referenties/gemini_gekozen_ronde6.png').convert('RGB'); im=np.array(src).astype(int)
m=nd.binary_fill_holes(np.abs(im-255).sum(2)>60)
lab,n=nd.label(m,structure=np.ones((3,3))); sz=nd.sum(m,lab,range(1,n+1))
m=np.isin(lab,1+np.where(sz>40)[0])            # dier + snorharen (vlekjes weg)
body=nd.binary_opening(m,structure=np.ones((7,7)))
lab2,n2=nd.label(body); body=lab2==(1+np.argmax(nd.sum(body,lab2,range(1,n2+1))))
thin=m&~body
ys,xs=np.nonzero(m); X0,X1,Y0,Y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
S=(X1-X0)/63.0; w=int(np.ceil((X1-X0)/S)); h=int(np.ceil((Y1-Y0)/S)); ox=0; oy=63-h
print('bbox',X0,X1,Y0,Y1,'S=%.3f'%S,'dier',w,'x',h,'offset',ox,oy)
def down(a,mode):
    out=np.zeros((64,64)); 
    for y in range(h):
        for x in range(w):
            b=a[int(Y0+y*S):int(Y0+(y+1)*S),int(X0+x*S):int(X0+(x+1)*S)]
            if b.size: out[oy+y,ox+x]=b.mean() if mode=='mean' else b.max()
    return out
cb=down(body.astype(float),'mean'); ct=down(thin.astype(float),'mean')
sil=cb>=0.5; dun=(~sil)&(ct>=0.12)
np.save(D+'kleur_r6/meta.npy',np.array([X0,Y0,S,ox,oy]))
open(D+'kleur_r6/silhouet_auto.txt','w').write('\n'.join(''.join('#' if sil[y,x] else ('+' if dun[y,x] else '.') for x in range(64)) for y in range(64))+'\n')
# onderlaag: gemiddelde kleur per spritepixel (alleen lichaamspixels), gekwantiseerd
f=np.zeros((64,64,3))
for y in range(h):
    for x in range(w):
        b=im[int(Y0+y*S):int(Y0+(y+1)*S),int(X0+x*S):int(X0+(x+1)*S)]; mm=m[int(Y0+y*S):int(Y0+(y+1)*S),int(X0+x*S):int(X0+(x+1)*S)]
        f[oy+y,ox+x]=b[mm].mean(0) if mm.any() else 255
Image.fromarray(f.clip(0,255).astype(np.uint8)).save(D+'kleur_r6/gemini64.png')
K='1345679ABC'
rows=[]
for y in range(64):
    s=''
    for x in range(64):
        if not sil[y,x]: s+='+' if dun[y,x] else '.'; continue
        s+=min(K,key=lambda k:sum((f[y,x,i]-PAL[int(k,16)][i])**2 for i in range(3)))
    rows.append(s)
open(D+'kleur_r6/onderlaag.txt','w').write('\n'.join(rows)+'\n')
