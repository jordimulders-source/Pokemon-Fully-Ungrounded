# Gedeelde hulpjes: schaal, overlap natief->sprite, palet (mediaan van de modelpixels per klasse), opslaan, componenten.
import numpy as np; from PIL import Image
S=0.43                      # 144 natieve rijen -> 62 spriterijen; 128 kolommen -> 55
U0,V0=36,28                 # natieve bbox linksboven
X0,Y0=4,1                   # spriteplek linksboven (Vileplume in de game: x4-59; 1 px marge boven, voet op y62)
MODEL='../referenties/gemini_gekozen_vileplume.png'
PITCH=5.12; C0=1.57        # natieve cel i heeft midden C0+i*PITCH in het model
def overlap(X,Y,W=200,H=200):
    ua=(X-X0)/S+U0; ub=ua+1/S; va=(Y-Y0)/S+V0; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))*S*S
            if w>1e-9 and 0<=u<W and 0<=v<H: yield u,v,w
def model_op_schaal(z=1):
    # model op exact dezelfde uitsnede/schaal als de sprite (64*z px)
    m=Image.open(MODEL).convert('RGB'); k=PITCH/S
    ox=C0-PITCH/2+PITCH*U0-X0*k; oy=C0-PITCH/2+PITCH*V0-Y0*k
    big=Image.new('RGB',(3072,3072),'white'); big.paste(m,(1024,1024))
    c=big.crop((int(ox+1024),int(oy+1024),int(ox+1024+64*k),int(oy+1024+64*k)))
    return c.resize((64*z,64*z),Image.BOX if z==1 else Image.LANCZOS)
def model_crop(x0,y0,x1,y1,z):
    m=Image.open(MODEL).convert('RGB'); k=PITCH/S
    ox=C0-PITCH/2+PITCH*U0-X0*k; oy=C0-PITCH/2+PITCH*V0-Y0*k
    return m.crop((int(ox+x0*k),int(oy+y0*k),int(ox+x1*k),int(oy+y1*k))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def rgb(o,PAL,bg=(255,255,255)):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,PAL,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal); p.save(path,transparency=0,bits=4)   # 16 paletplekken, 4 bpp zoals de game
def label(mask,acht=True):
    lab=np.zeros(mask.shape,int); n=0
    nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if acht else [(-1,0),(1,0),(0,-1),(0,1)]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<mask.shape[0] and 0<=xx<mask.shape[1] and mask[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
    return lab,n
