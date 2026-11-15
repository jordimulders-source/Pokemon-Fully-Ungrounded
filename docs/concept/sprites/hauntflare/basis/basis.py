# Nieuwe basis Hauntflare 64x64: (1) model opschonen (bijna-wit -> wit), (2) verkleinen met oppervlak-middeling
# i.p.v. rijen/kolommen schrappen (bol blijft rond, ringpunt blijft), (3) kwantiseren naar modelkleuren, alpha >= drempel.
import sys; from PIL import Image; import numpy as np
T=float(sys.argv[1]) if len(sys.argv)>1 else 0.5
a=np.asarray(Image.open('model/model_claude_natief.png').convert('RGB')).astype(int)
wit=(a.min(2)>=0xe0)                       # bijna-wit is achtergrond (Gemini-ruis)
a[wit]=255
ys,xs=np.where(~wit); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
print('inhoud natief',x1-x0,'x',y1-y0)
crop=a[y0:y1,x0:x1]; alpha=(~wit[y0:y1,x0:x1]).astype(float)
s=62/max(crop.shape[:2]); W,H=round(crop.shape[1]*s),round(crop.shape[0]*s)
big=lambda arr: np.kron(arr,np.ones((10,10,1)) if arr.ndim==3 else np.ones((10,10)))
# kleur gemiddeld alleen over dekkende pixels
cb=big(crop*alpha[...,None]); ab=big(alpha)
ci=Image.fromarray(cb.astype('float32')[...,0]); 
def area(arr):
    im=Image.fromarray(arr.astype('float32')); return np.asarray(im.resize((W,H),Image.BOX))
C=np.stack([area(cb[...,k]) for k in range(3)],2); A=area(ab)
C=C/np.maximum(A,1e-6)[...,None]
# palet = de kleuren van het model (frequente), dichtstbijzijnde
pal,cnt=np.unique(crop[alpha>0].reshape(-1,3),axis=0,return_counts=True)
pal=pal[cnt>=3]
out=np.zeros((64,64,4),'uint8'); ox=(64-W)//2; oy=64-H-1
for y in range(H):
    for x in range(W):
        if A[y,x]>=T:
            k=np.argmin(((pal-C[y,x])**2).sum(1)); out[oy+y,ox+x,:3]=pal[k]; out[oy+y,ox+x,3]=255
Image.fromarray(out).save('basis/basis_64.png'); print('maat',W,H,'pos',ox,oy,'palet',len(pal))
