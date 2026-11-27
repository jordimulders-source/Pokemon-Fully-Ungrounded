# r5 (= r1b met het 7-kleurenpalet): oppervlaktegewogen verkleining i.p.v. schrappen. Per spritepixel de paletkleur met het grootste
# overlappende oppervlak in het gekwantiseerde natieve raster (lijn x1,5). Oogzone (natief rij 24-31, kol 28-37) 1-op-1 (factor 1),
# de rest stuksgewijs lineair verkleind zodat de figuur 40x64 wordt.
import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
q=np.load(D+'natief_q.npy'); pal=eval(open(D+'pal.txt').read())
def randen(N,a,b,A,uit):
    # natief 0..a -> uit 0..A ; a..b 1-op-1 ; b..N -> rest. A geheel, zodat de oogzone precies op hele pixels valt.
    k1=a/A; B=A+(b-a); k2=(N-b)/(uit-B); out=[]
    for i in range(uit+1):
        out.append(i*k1 if i<=A else (a+(i-A) if i<=B else b+(i-B)*k2))
    return out
def ov(e,i):
    lo,hi=e[i],e[i+1]; r=[]
    for n in range(int(np.floor(lo)),int(np.ceil(hi))):
        w=min(hi,n+1)-max(lo,n)
        if w>1e-6: r.append((n,w))
    return r
H,W=q.shape
# A zo kiezen dat oogrijen op hele pixels vallen: afronden
ry=randen(H,24,32,18,64); cx=randen(W,28,38,21,40)
S=np.zeros((64,40),int)
for y in range(64):
    for x in range(40):
        sc=np.zeros(16)
        for n,wy in ov(ry,y):
            for m,wx in ov(cx,x):
                if n<H and m<W: sc[q[n,m]]+=wy*wx*(1.5 if q[n,m]==1 else 1)
        S[y,x]=sc.argmax()
np.save(D+'r5/idx.npy',S); save_p64(S,pal,D+'r5/sprite.png'); save_idx(S,pal,D+'r5/r5_8x.png',8)
print([round(v,2) for v in ry[16:30]]); print([round(v,2) for v in cx[18:32]])
