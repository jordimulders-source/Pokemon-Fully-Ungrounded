# Volume-toonkaart voor het lijf (Gen 3: licht linksboven, sikkelschaduw rechtsonder), uit het MODEL:
# natief raster (../sprite_r2/natief.png) -> groen masker; zwarte modellijnen en roze/achtergrond zijn de randen van elke massa
# -> afstand tot de rand -> bolle hoogte (cirkelprofiel, straal R) -> normaal -> n.l met l = linksboven-voor.
# Per spritepixel het gemiddelde over het venster. Plus de gladde modelhelderheid (toonkaart) met gewicht A.
import sys,numpy as np; sys.path.append('../sprite_r2'); from groepen import laad
def chamfer(m):
    INF=1e9; d=np.where(m,INF,0.0); H,W=d.shape; s2=2**.5
    for y in range(H):
        for x in range(W):
            if d[y,x]:
                v=d[y,x]
                if y: v=min(v,d[y-1,x]+1, d[y-1,x-1]+s2 if x else INF, d[y-1,x+1]+s2 if x<W-1 else INF)
                if x: v=min(v,d[y,x-1]+1)
                d[y,x]=v
    for y in range(H-1,-1,-1):
        for x in range(W-1,-1,-1):
            if d[y,x]:
                v=d[y,x]
                if y<H-1: v=min(v,d[y+1,x]+1, d[y+1,x+1]+s2 if x<W-1 else INF, d[y+1,x-1]+s2 if x else INF)
                if x<W-1: v=min(v,d[y,x+1]+1)
                d[y,x]=v
    return d
def gauss(x,s):
    r=int(3*s)+1; k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    y=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,x); return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,y)
def kaart(R=10.0,A=0.5,L=(-0.55,-0.65,0.52),NAT='../sprite_r2/natief.png'):
    a,lum,g=laad(NAT)
    m=(g==4)
    d=chamfer(m); t=np.clip(d/R,0,1); h=R*np.sqrt(1-(1-t)**2)
    h=gauss(h,1.2)
    gy,gx=np.gradient(h); n=np.stack([-gx,-gy,np.ones_like(h)],-1); n/=np.linalg.norm(n,axis=-1,keepdims=True)
    l=np.array(L); l/=np.linalg.norm(l); sh=(n@l)
    # gladde modelhelderheid van het groen (zonder donkere rib-/lijnpixels)
    licht=m&(lum>=72); TK=gauss(lum*licht,6)/np.maximum(gauss(licht.astype(float),6),1e-6)
    TKn=(TK-np.median(TK[m]))/max(np.std(TK[m]),1e-6)
    shn=(sh-np.median(sh[m]))/max(np.std(sh[m]),1e-6)
    return m, shn+A*TKn
if __name__=='__main__':
    from PIL import Image
    m,v=kaart(); np.save('_volume.npy',np.where(m,v,np.nan))
    z=np.clip((v+2.5)/5,0,1); z[~m]=0; Image.fromarray((z*255).astype('uint8')).resize((510,510)).save('/tmp/claude-0/s/vol.png')
