# r2 punt 1+3: kop opnieuw uit het natieve model. Natieve pixels -> groep (creme / roze vlam / bruine lijn), groepskaart 2x
# gladgestreken met een 3x3-meerderheid (glitter en losse korrels weg, strepen blijven aaneengesloten), daarna per spritepixel
# de groep met het grootste oppervlak. Creme in 3 tinten (3,4,5) naar de gemiddelde modelhelderheid, roze vlam = 7 (een tint).
# Silhouet in de kopzone: dekking >= 0,35 (dunne vlamtongen blijven), alleen pixels vast aan de kop.
import numpy as np, json; from PIL import Image
q=np.asarray(Image.open('natief_q_dg.png')).astype(int); n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
G=np.zeros_like(q)                       # 0 leeg, 1 lijn, 2 creme, 3 roze
G[np.isin(q,[1,2])]=1; G[np.isin(q,[3,4,5])]=2; G[np.isin(q,[6,7,8,9,10,11,12])]=3
def meerderheid(G):
    H,W=G.shape; R=G.copy()
    for y in range(1,H-1):
        for x in range(1,W-1):
            if G[y,x] not in (2,3): continue
            b=G[y-1:y+2,x-1:x+2].ravel(); c2=(b==2).sum(); c3=(b==3).sum()
            if G[y,x]==2 and c3>=6: R[y,x]=3
            if G[y,x]==3 and c2>=6: R[y,x]=2
    return R
import sys; ROZE=float(sys.argv[1]) if len(sys.argv)>1 else 0.35   # roze vlam als >= dit aandeel van creme+roze
G=meerderheid(G)
S=12/5.12; OX=(106-4.25)/5.12-0.5; OY=(120-4.25)/5.12-0.5
lum=n@[0.299,0.587,0.114]
KZ=lambda i,j: i<26 and j<31 and not (i>=22 and j>=24)
kop=np.zeros((64,64),int)
for j in range(31):
    for i in range(26):
        if not KZ(i,j): continue
        y0=OY+j*S; x0=OX+i*S; w=np.zeros(4); L=0; Lw=1e-9
        for yy in range(int(np.floor(y0)),int(np.ceil(y0+S))):
            for xx in range(int(np.floor(x0)),int(np.ceil(x0+S))):
                if not(0<=yy<G.shape[0] and 0<=xx<G.shape[1]): continue
                a=max(0,min(yy+1,y0+S)-max(yy,y0))*max(0,min(xx+1,x0+S)-max(xx,x0)); w[G[yy,xx]]+=a
                if G[yy,xx]==2: L+=lum[yy,xx]*a; Lw+=a
        w/=S*S
        if 1-w[0]<0.35: continue
        if w[1]>=0.28: kop[j,i]=2
        elif w[3]>=ROZE*(w[2]+w[3]): kop[j,i]=7
        else:
            L/=Lw; kop[j,i]=3 if L<205 else (4 if L<226 else 5)
np.save('kop.npy',kop)
for y in range(31): print('%2d'%y,''.join('.123456789ABCDEF'[v] for v in kop[y,:26]))
