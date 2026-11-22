# Ronde 2 (vanaf r1/idx.npy): ontkorrelen (1-staps-tintvlekjes < 3 px), losse lijnpixels weg,
# binnenbarsten in donkere steentint (variant B) of zwart (variant A). Silhouet, oog en neuslijn bevroren.
import numpy as np, sys; from PIL import Image; from scipy import ndimage
k=np.load('../kaal.npy'); o=np.load('../r1/idx.npy').copy()
PAL=np.array([(0,0,0),(24,16,16),(72,28,32),(104,40,36),(136,52,44),(172,72,58),(204,108,92),(228,148,128),
              (172,22,24),(220,48,44),(228,124,108)],float)
RANK={7:0,6:1,5:2,4:3,3:4}
J,I=np.mgrid[0:64,0:64]
EC=(28.0,35.5); eye=((I-EC[1])**2+(J-EC[0])**2)<=7.6**2
fig=o>0
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
neuslijn=(J==29)&(I<=21)
frozen=eye|rim|neuslijn
# 0. barsten verbinden: binnenpixel waar het model >= 20 % zwart heeft, naast een lijnpixel,
#    zonder 2x2-lijnblok te maken (lijnkaart uit ../zwartfrac.npy, modelmeting)
fr=np.load('../zwartfrac.npy')
PC=(29.2,37.3); pr=np.sqrt((I-PC[1])**2+(J-PC[0])**2)
naad=(~eye)&(pr>=7.0)&(pr<=10.4)&(I>=38)
toegevoegd=0
for _ in range(2):
  for j,i in zip(*np.where((fr>=0.2)&(o!=1)&~frozen&~(pr<=10.4)&fig)):
    L=(o==1)
    if not L[j-1:j+2,i-1:i+2].any(): continue
    ok=True
    for dj in (-1,0):
      for di in (-1,0):
        b=L[j+dj:j+dj+2,i+di:i+di+2].copy(); b[-dj,-di]=True
        if b.all(): ok=False
    if ok: o[j,i]=1; toegevoegd+=1
print('barstpixels verbonden:',toegevoegd)
# 1. losse lijnpixels (1) binnenin zonder 8-buur die lijn is -> buurtint
for j,i in zip(*np.where((o==1)&~frozen)):
    n8=o[j-1:j+2,i-1:i+2]
    if ((n8==1)|(n8==2)).sum()<=1:
        st=[v for v in n8.ravel() if v in RANK]; o[j,i]=max(set(st),key=st.count) if st else 4
# 2. ontkorrelen: tintvlekjes < 3 px die 1 stap van de buurmeerderheid afwijken
for _ in range(3):
  for v in RANK:
    lab,n=ndimage.label(o==v)
    for c in range(1,n+1):
        m=lab==c
        if m.sum()>=3 or (m&frozen).any(): continue
        ring=ndimage.binary_dilation(m)&~m
        st=[x for x in o[ring] if x in RANK]
        if not st: continue
        mj=max(set(st),key=st.count)
        if abs(RANK[mj]-RANK[v])==1: o[m]=mj
# 3. plaknaad: lichte resten van de plakcirkel in/tegen de zwarte oogrand -> meerderheid van de 8-buren
for j,i in zip(*np.where(eye&np.isin(o,[6,7]))):
    if ((I[j,i]-EC[1])**2+(J[j,i]-EC[0])**2)<5.0**2: continue
    n8=[v for v in o[j-1:j+2,i-1:i+2].ravel()]
    n8.remove(o[j,i]) if o[j,i] in n8 else None
    if n8.count(1)>=3: o[j,i]=1
# 4. plaknaad: binnen de oude v11-oogellips (opgevuld met verschoven textuur in plak2.py) en buiten de oogrand
#    zijn lijnen synthetisch -> steentint van de buren (zelfde ellips als plak2: (418,388)-(642,628))
ox,oy=(530-51)/13-0.5,(508-126.5)/13-0.5; rx,ry=112/13+0.7,120/13+0.7
oud=(((I-ox)/rx)**2+((J-oy)/ry)**2<=1)&~eye&~rim
STEEN=[3,4,5,6,7]
for _ in range(3):
  for j,i in zip(*np.where(oud&(o==1))):
    n8=[v for v in o[j-1:j+2,i-1:i+2].ravel() if v in STEEN]
    if n8: o[j,i]=max(set(n8),key=n8.count)
np.save('naadzone.npy',oud)
np.save('idxA.npy',o)
B=o.copy()
binnen=(o==1)&~eye&~rim&~neuslijn
B[binnen]=2
np.save('idxB.npy',B)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
save(o,'A.png'); save(B,'B.png')
print('A wijkt af van kaal:',int((o!=k).sum()),' B:',int((B!=k).sum()))

# ---- definitief r2: variant A (zwarte barsten zoals het model) + tint 6 opgeheven:
# elke 6-pixel naar 7 of 5 volgens de mediaan-helderheid van het modelblok (dichtstbijzijnde modeltint),
# zodat steen 4 tinten heeft (zoals de Gen 3-Lunatone) + selout 2 + zwart. Palet iets uit elkaar getrokken.
a=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(float); lum=a.mean(2)
S=13.0; X0=51.0; Y0=126.5
D=np.load('idxA.npy').copy()
for j,i in zip(*np.where(D==6)):
    ys=slice(int(round(Y0+j*S)),int(round(Y0+(j+1)*S))); xs=slice(int(round(X0+i*S)),int(round(X0+(i+1)*S)))
    L=lum[ys,xs][lum[ys,xs]>40]; D[j,i]=7 if np.median(L)>=128 else 5
PAL2=np.array([(0,0,0),(24,16,16),(64,24,30),(100,36,38),(138,52,44),(180,78,62),(204,108,92),(232,152,132),
               (168,20,24),(222,50,44),(236,128,112)],float)
np.save('idx.npy',D)
def save2(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL2.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
save2(D,'sprite.png'); save2(D,'sprite_8x.png',8)
# rapport per zone t.o.v. de kale reductie
Z=np.full((64,64),'lijf',dtype=object)
Z[eye]='oog'; Z[oud|((pr>=7.0)&(pr<=10.4)&(I>=38)&~eye)]='naad'
Z[(J>=24)&(J<=33)&(I<=27)&(Z=='lijf')]='neus'
lab,n=ndimage.label(k>0); main=np.argmax(np.bincount(lab.ravel())[1:])+1
Z[(lab!=main)&(lab>0)]='puin'
dif=(D!=k); fig2=(k>0)|(D>0)
with open('wijzigingen.txt','w') as f:
  f.write('Ronde 2: pixels afwijkend van de kale reductie (../kaal.png), per zone (index-verschil; paletkleur telt niet)\n')
  for z in ['oog','naad','neus','lijf','puin']:
    m=(Z==z)&fig2
    f.write(f'{z:5s}: {int((dif&m).sum()):4d} van {int(m.sum())}\n')
  f.write(f'totaal: {int(dif.sum())}\nalpha-diff (silhouet): {int(((k>0)!=(D>0)).sum())}\n')
  f.write('''Wat er gebeurde:
- oog: puntmonster uit het model (oog is bijna natief, 12,08 vs 13 px), fase +0,3 px verticaal; lichte resten van de plakcirkel in de zwarte rand -> zwart.
- naad: binnen de oude v11-oogellips (in plak2.py opgevuld met verschoven textuur) en de donkere boog rechts: lijnen -> steentint van de buren.
- omlijning: elke randpixel lijn; lichtkant (linksboven) selout donker steenrood, rest zwart.
- barsten: onderbroken modelbarsten verbonden waar het model >= 20 % zwart heeft (lijnkaart), losse lijnpixels weg.
- ontkorrelen: tintvlekjes < 3 px die 1 stap van de buren afwijken -> buurtint.
- tint 6 opgeheven (naar 7/5 volgens modelhelderheid): steen = 4 tinten + selout + zwart.
''')
print(open('wijzigingen.txt').read())
