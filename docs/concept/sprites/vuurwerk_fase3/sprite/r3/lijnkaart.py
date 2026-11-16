# r3: lijnkaart van het natieve model -> sprite. Elke natieve pixel van een groep (roze vlam / bruine lijn) zet de spritepixel
# waarin zijn middelpunt valt. Componenten < 3 natieve px tellen niet (losse korrels). Zo blijven 1-natieve-px strepen en
# lijnen aaneengesloten 1 spritepx breed, met richting en lengte uit het model.
import numpy as np; from PIL import Image
q=np.asarray(Image.open('natief_q_dg.png')).astype(int); H,W=q.shape
S=12/5.12; OX=(106-4.25)/5.12-0.5; OY=(120-4.25)/5.12-0.5
def comp(m):
    seen=np.zeros_like(m,bool); out=np.zeros_like(m,bool)
    for y in range(H):
        for x in range(W):
            if not m[y,x] or seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=1; c=[]
            while st:
                p=st.pop(); c.append(p)
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        r=(p[0]+dy,p[1]+dx)
                        if 0<=r[0]<H and 0<=r[1]<W and m[r] and not seen[r]: seen[r]=1; st.append(r)
            if len(c)>=3:
                for p in c: out[p]=1
    return out
def kaart(ks):
    m=comp(np.isin(q,ks)); k=np.zeros((64,64),int)
    ys,xs=np.where(m)
    for y,x in zip(ys,xs):
        i=int(np.floor((x+0.5-OX)/S)); j=int(np.floor((y+0.5-OY)/S))
        if 0<=i<64 and 0<=j<64: k[j,i]+=1
    return k
roze=kaart([6,7,8,9,10,11,12]); bruin=kaart([1,2])
np.save('kaart_roze.npy',roze); np.save('kaart_bruin.npy',bruin)
for y in range(2,29): print('%2d'%y,''.join('#' if bruin[y,x] else ('r' if roze[y,x] else '.') for x in range(26)))
