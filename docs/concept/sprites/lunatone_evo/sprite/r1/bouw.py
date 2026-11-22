# Ronde 1: kale reductie (../kaal.npy) + technische opschoning. Niets getekend:
# elke gewijzigde pixel komt uit het model (puntmonster) of uit de buurtinten.
import numpy as np, sys; from PIL import Image
sys.path.insert(0,'..')
a=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(float)
k=np.load('../kaal.npy'); o=k.copy()
PAL=np.array([(0,0,0),(24,16,16),(72,28,32),(104,40,36),(136,52,44),(172,72,58),(204,108,92),(228,148,128),
              (172,22,24),(220,48,44),(228,124,108)],float)
STEEN=[3,4,5,6,7]
S=13.0; X0=51.0; Y0=126.5
J,I=np.mgrid[0:64,0:64]
def near(c,ids): return ids[int(np.argmin([((PAL[i]-c)**2).sum() for i in ids]))]
zone=np.zeros((64,64),'U6'); zone[:]='lijf'
# --- 1. OOG: puntmonster van het model (oog is bijna natief: 12,08 vs 13 px), fase dy=+0,3
EC=(28.0,35.5); ER=7.6
eye=((I-EC[1])**2+(J-EC[0])**2)<=ER**2
for j,i in zip(*np.where(eye)):
    c=a[int(Y0+(j+.8)*S),int(X0+(i+.5)*S)]
    if c.mean()<45: v=1
    elif c[0]>130 and c[0]-c[1]>90 and ((i-EC[1])**2+(j-EC[0])**2)<6.3**2: v=near(c,[8,9,10])
    else: v=near(c,STEEN)
    o[j,i]=v
zone[eye]='oog'
# --- 2. PLAKNAAD rond het oog: ring ER..ER+3; donkere boog/sikkel en rode resten -> buurtint van buiten de ring
ring=(((I-EC[1])**2+(J-EC[0])**2)>ER**2)&(((I-EC[1])**2+(J-EC[0])**2)<=(ER+3.2)**2)
zone[ring&(o>0)]='naad'
# rode resten buiten het oog
for j,i in zip(*np.where(~eye&np.isin(o,[8,9,10]))):
    nb=[o[y,x] for y,x in ((j-1,i),(j+1,i),(j,i-1),(j,i+1)) if o[y,x] in STEEN]
    o[j,i]=max(set(nb),key=nb.count) if nb else 5

# plaknaad: cirkel van het geplakte oog (middelpunt col 37,3 / rij 29,2, straal ~9,2): donkere boog + sikkel
PC=(29.2,37.3); pr=np.sqrt((I-PC[1])**2+(J-PC[0])**2)
naad=(~eye)&(pr>=7.0)&(pr<=10.2)&np.isin(o,[1,2,3])&(I>=38)   # rechterhelft: boog en donkere sikkel
zone[naad]='naad'
for _ in range(3):
    for j,i in zip(*np.where(naad)):
        nb=[o[y,x] for y in range(j-1,j+2) for x in range(i-1,i+2) if (y,x)!=(j,i) and not naad[y,x] and o[y,x] in STEEN]
        if nb: o[j,i]=max(set(nb),key=nb.count)
np.save('stap2.npy',o)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
# --- 3. omlijning: elke figuurpixel naast transparant wordt lijn; lichtkant (normaal naar linksboven) = selout 2
from scipy import ndimage
fig=(o>0)
sm=ndimage.gaussian_filter(fig.astype(float),1.2)
gy,gx=np.gradient(sm)   # wijst naar binnen
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
for j,i in zip(*np.where(rim)):
    nx,ny=-gx[j,i],-gy[j,i]  # naar buiten
    n=np.hypot(nx,ny)+1e-9; d=(-nx-ny)/n/np.sqrt(2)   # 1 = naar linksboven
    v=2 if d>0.35 else 1
    if o[j,i]!=v: zone_old=zone[j,i]; o[j,i]=v
# --- 4. ruis: losse steenpixel zonder gelijke 4-buur en met 3+ gelijke andere buren -> buurtint
for _ in range(2):
  for j in range(1,63):
    for i in range(1,63):
      v=o[j,i]
      if v not in STEEN: continue
      n4=[o[j-1,i],o[j+1,i],o[j,i-1],o[j,i+1]]
      if v in n4: continue
      st=[x for x in n4 if x in STEEN]
      if len(st)>=3:
        m=max(set(st),key=st.count)
        if st.count(m)>=2: o[j,i]=m
np.save('idx.npy',o)
save(o,'sprite.png'); save(o,'sprite_8x.png',8)
# rapport
Z=zone.copy()
nose=(J>=24)&(J<=33)&(I<=27)&(o>0)&(Z=='lijf'); Z[nose]='neus'
lab,n=ndimage.label(k>0); main=np.argmax(np.bincount(lab.ravel())[1:])+1
Z[(lab!=main)&(lab>0)]='puin'
dif=(o!=k)
with open('wijzigingen.txt','w') as f:
  f.write('Ronde 1: pixels afwijkend van de kale reductie (../kaal.png), per zone\n')
  for z in ['oog','naad','neus','lijf','puin']:
    m=(Z==z)
    f.write(f'{z:5s}: {int((dif&m).sum()):4d} van {int(((k>0)|(o>0))[m].sum())}\n')
  f.write(f'totaal: {int(dif.sum())}\n')
  f.write('alpha-diff (silhouet) t.o.v. kale reductie: %d\n'%int(((k>0)!=(o>0)).sum()))
print(open('wijzigingen.txt').read())
