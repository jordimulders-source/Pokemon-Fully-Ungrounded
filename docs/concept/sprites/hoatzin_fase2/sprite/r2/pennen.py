# Pennen segmenteren op het natieve model: vleugelvlak minus (verdikte) scheidingslijnen -> verbonden gebieden = pennen
import numpy as np, os; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
Z=np.load('zones_nat.npy'); LOC=np.load('loc_nat.npy'); L=N.mean(2)
LIJN=np.load('lijn_nat.npy')|(np.isin(Z,['M','W','K','D'])&(L<LOC-float(os.environ.get('SEGD',12)))&(L<LOC*0.9)); H,W=Z.shape
yy,xx=np.mgrid[:H,:W]; VLEUGEL=((xx>=92)|(yy<60))&np.isin(Z,['M','W','K','D'])
d=LIJN.copy()
for dy,dx in ((0,1),(1,0)): d|=np.roll(LIJN,(dy,dx),(0,1))
vrij=VLEUGEL&~d&(Z!='K')
lab=np.zeros((H,W),int); n=0
for y0 in range(H):
  for x0 in range(W):
    if vrij[y0,x0] and not lab[y0,x0]:
      n+=1; st=[(y0,x0)]; lab[y0,x0]=n
      while st:
        a,b=st.pop()
        for e,f in ((1,0),(-1,0),(0,1),(0,-1)):
          p,q=a+e,b+f
          if 0<=p<H and 0<=q<W and vrij[p,q] and not lab[p,q]: lab[p,q]=n; st.append((p,q))
sz=np.bincount(lab.ravel()); klein=[i for i in range(1,n+1) if sz[i]<25]
for i in klein: lab[lab==i]=0
print('pennen',n-len(klein),'groottes',sorted(sz[1:][sz[1:]>=25])[::-1][:30])
np.save('pen_nat.npy',lab)
rng=np.random.RandomState(1); cols=rng.randint(60,255,(n+1,3)); cols[0]=0
img=N.copy(); m=lab>0; img[m]=cols[lab[m]]*0.7+N[m]*0.3
Image.fromarray(img.astype('uint8')).resize((800,800),Image.NEAREST).save('pennen.png')
