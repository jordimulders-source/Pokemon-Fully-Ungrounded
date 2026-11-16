# r15 basis: gladde modelvulling. Natief model -> genormaliseerd gaussgemiddelde over alleen ijzerpixels (geen lijn <70, geen groen, geen wit),
# daarna per spritevoetafdruk (onderlaag.voet, r13-coordinaten = r14 x-2) het gewogen gemiddelde. Lijnregel = r14 (onderlaag.py).
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r14')
import onderlaag as O, numpy as np
from PIL import Image
D=O.D
N=np.array(Image.open(D+'model/natief.png').convert('RGB')).astype(float)
LUM=0.3*N[...,0]+0.59*N[...,1]+0.11*N[...,2]
IJZ=(N.min(2)<=215)&~(N[...,1]>N[...,0]+20)&(LUM>=70)
BRUIN=IJZ&((N[...,0]-N[...,2])>45); GRIJS=IJZ&~BRUIN
def glad(sig,M=None):
    M=IJZ if M is None else M
    r=int(np.ceil(3*sig)); k=np.exp(-np.arange(-r,r+1)**2/(2*sig*sig))
    def conv(a):
        a=np.apply_along_axis(lambda v:np.convolve(v,k,'same'),0,a)
        return np.apply_along_axis(lambda v:np.convolve(v,k,'same'),1,a)
    w=conv(M.astype(float)); out=np.zeros_like(N)
    for c in range(3): out[...,c]=conv(N[...,c]*M)/np.maximum(w,1e-6)
    return out
def vul(x14,y,G,DY,M=None):
    M=IJZ if M is None else M
    O.DY=DY; c=O.voet(x14-2,y)
    # voetafdruk-cellen terugvinden: voet geeft kleuren, dus opnieuw met indices
    x=x14-2; F=O.F
    x0=9+x/F; x1=9+(x+1)/F; y0=6+(y-2-DY)/F; y1=6+(y-1-DY)/F
    s=0; W=0
    for ny in range(int(np.floor(y0)),int(np.ceil(y1))):
        for nx in range(int(np.floor(x0)),int(np.ceil(x1))):
            w=(min(x1,nx+1)-max(x0,nx))*(min(y1,ny+1)-max(y0,ny))
            if w>0.02 and 0<=ny<99 and 0<=nx<99 and M[ny,nx]: s=s+w*G[ny,nx]; W+=w
    return s/W if W>0 else None
def lijnregel(DY,DREMPEL=70,AANDEEL=0.5):
    O.DY=DY; T,L,Wt,Gr=O.onderlaag(DREMPEL,AANDEEL)
    L2=np.zeros_like(L); T2=np.zeros_like(T); L2[:,2:]=L[:,:62]; T2[:,2:]=T[:,:62]   # naar r14-coordinaten
    return L2,T2
