# Hoofd vergroten v2: boven Jordi's rode lijn; op de lijn schaal 1 (sluit naadloos aan), daarboven oplopend
# naar S over D natieve px; horizontaal anker = gezichtsmidden, verticaal anker = de lijn per kolom.
import sys; from PIL import Image; import numpy as np
S=float(sys.argv[1]); D=float(sys.argv[2]) if len(sys.argv)>2 else 8
J=np.array(Image.open('../gemini/jordi_rode_lijn_hoofd.png').convert('RGB')).astype(int)
r=(J[:,:,0]>180)&(J[:,:,1]<80)&(J[:,:,2]<80)
ys,xs=np.where(r); sx=xs/9.8+9; sy=ys/9.8+7; nx=3*sx+3; ny=3*sy-9
N=np.array(Image.open('../sprite/natief.png').convert('RGB')); H,W=N.shape[:2]
lijn=np.full(W,np.nan)
for x in range(W):
    m=np.abs(nx-x)<1.0
    if m.any(): lijn[x]=ny[m].mean()
xl=np.where(~np.isnan(lijn))[0]
lijn=np.interp(np.arange(W),xl,lijn[xl],left=-1e9,right=-1e9)   # buiten de lijn: niets vergroten
ax=90.0
bg=(N.min(2)>240)
out=N.copy()
for y in range(H):
    for x in range(W):
        L=lijn[x]
        if L<0 or y>=L: continue
        # zoek bronpunt: s hangt af van de afstand tot de lijn in de bron; 3 iteraties
        sxx,syy=x,y
        for _ in range(4):
            Ls=np.interp(sxx,np.arange(W),lijn) if 0<=sxx<W else L
            t=np.clip((Ls-syy)/D,0,1); s=1+(S-1)*t
            sxx=ax+(x-ax)/s; syy=Ls-(Ls-y)/s
        ix,iy=int(round(sxx)),int(round(syy))
        if 0<=ix<W and 0<=iy<H and iy<lijn[ix]: out[y,x]=N[iy,ix]
        elif not bg[y,x] and y<L: out[y,x]=(255,255,255)
Image.fromarray(out).save('natief_hoofd2_%s.png'%sys.argv[1])
