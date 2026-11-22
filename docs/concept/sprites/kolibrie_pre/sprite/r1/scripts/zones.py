# Zonekaart op het natieve model (100x100): alleen kleurregels + een paar vakken op modelcoördinaten
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
R,G,B=N[...,0],N[...,1],N[...,2]; L=N.mean(2)
def flood(m):
    H,W=m.shape; r=np.zeros_like(m); st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    while st:
        y,x=st.pop()
        if 0<=y<H and 0<=x<W and m[y,x] and not r[y,x]:
            r[y,x]=1; st+= [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    return r.astype(bool)
Z=np.full(N.shape[:2],'L',dtype='<U1')   # L = lila lijf/kop
bg=flood(L>236); Z[bg]='.'
yy,xx=np.mgrid[:100,:100]
Z[(~bg)&(L>=195)]='W'                    # buik licht
Z[(~bg)&(B-R>45)&(L<125)]='V'            # blauwe vleugel/staart
Z[(~bg)&(R-B>60)]='F'                    # pootjes
Z[(~bg)&(R>170)&(G>140)&(B<120)&(yy<40)]='Y'  # gele mondhoek
Z[(~bg)&(N.max(2)<48)]='K'               # zwarte lijn
np.save('zones_nat.npy',Z)
for y in range(17,88): print('%2d '%y+''.join(Z[y,10:92]))
# extra zones: snavel, oog, spikkels
S=(~bg)&(Z!='K')&(L<120)&(yy<35)&(xx<45)&(Z!='Y')&(Z!='F'); Z[S]='S'
Z[(~bg)&(xx<33)&(yy<34)&np.isin(Z,['L','W'])]='S'
eb=(yy>=27)&(yy<=34)&(xx>=46)&(xx<=56)
Z[eb&(~bg)&((Z=='K')|(L<135)|(Z=='W'))]='E'
W=(Z=='W').astype(int); P=np.pad(W,2); cnt=sum(P[2+dy:102+dy,2+dx:102+dx] for dy in range(-2,3) for dx in range(-2,3))
Z[(Z=='L')&(cnt>=13)&(yy>=33)&(yy<58)&(xx<48)]='P'
np.save('zones_nat.npy',Z)
print()
for y in range(19,58): print('%2d '%y+''.join(Z[y,10:70]))
