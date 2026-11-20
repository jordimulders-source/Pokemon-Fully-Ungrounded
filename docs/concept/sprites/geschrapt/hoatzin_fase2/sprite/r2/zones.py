# Zonekaart op het natieve model (200x200), alleen kleurregels + vakken op modelcoördinaten
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
R,G,B=N[...,0],N[...,1],N[...,2]; L=N.mean(2); MX=N.max(2); MN=N.min(2)
H,W=L.shape; yy,xx=np.mgrid[:H,:W]
def flood(m):
    r=np.zeros_like(m); st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    while st:
        y,x=st.pop()
        if 0<=y<H and 0<=x<W and m[y,x] and not r[y,x]:
            r[y,x]=1; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    return r.astype(bool)
fg=~flood(L>232)
# ingesloten modelgaten (tussen de poten): witte componenten >= 20 px zijn achtergrond
m=fg&(L>215); seen=np.zeros_like(m)
for y0 in range(H):
  for x0 in range(W):
    if m[y0,x0] and not seen[y0,x0]:
      st=[(y0,x0)]; c=[]; seen[y0,x0]=1
      while st:
        a,b=st.pop(); c.append((a,b))
        for d,e in ((1,0),(-1,0),(0,1),(0,-1)):
          p,q=a+d,b+e
          if 0<=p<H and 0<=q<W and m[p,q] and not seen[p,q]: seen[p,q]=1; st.append((p,q))
      if len(c)>=20:
        for a,b in c: fg[a,b]=False
Z=np.full((H,W),'.',dtype='<U1'); Z[fg]='M'                      # M = mauve lijf/vleugel
Z[fg&(R-B>=22)&(G-B>=-2)&(yy<75)]='C'                            # kuif bruin
Z[fg&(B-R>=20)&(B-G>=25)]='F'                                    # blauw gezicht
Z[fg&(R-G>=30)&(B-G<=10)&(yy>=100)&(yy<=160)&(xx<=120)]='P'      # buik
Z[fg&(B>=R)&(MX-MN<=25)&(yy>=150)&(L>=55)]='T'                   # tenen/poten (grijs)
beakbox=(xx<=58)&(yy>=62)&(yy<=88)
Z[fg&beakbox&(MX-MN<=20)&(L>=50)]='S'                            # snavel grijs
eyebox=(xx>=44)&(xx<=58)&(yy>=63)&(yy<=74)
Z[fg&eyebox&(R-B>=10)&(R-G>=40)]='E'                             # oog roze/rood
Z[fg&eyebox&(MX<70)&(R>B)]='E'
Z[fg&(L<62)&(xx>=112)&(yy>=128)&np.isin(Z,['M'])]='D'                # staart donker
Z[fg&(Z=='M')&(L>=150)]='W'                                     # lichte vleugelstrepen
Z[fg&(MX<34)]='K'                                                # lijn/zwart
np.save('zones_nat.npy',Z)
cmap={'.':(255,255,255),'M':(140,110,130),'C':(200,110,40),'F':(60,90,230),'P':(240,170,170),'T':(120,200,120),'S':(200,200,0),'E':(255,0,0),'K':(0,0,0),'D':(70,40,60),'W':(250,200,240)}
img=np.array([[cmap[z] for z in r] for r in Z],'uint8')
Image.fromarray(img).resize((800,800),Image.NEAREST).save('zones_nat.png')
for z in cmap: print(z,(Z==z).sum())
