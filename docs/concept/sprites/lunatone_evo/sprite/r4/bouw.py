# Ronde 4 (vanaf r3/idx.npy), keuring r3: netheid. Niets getekend:
# - steentint T per pixel = helderheid van het modelblok (mediaan, zonder lijnen) -> 4 tinten
# - barsten in zones A/B/R: alles weg, alleen lange modelbreuken terug als goedkoopste pad
#   over de barstkaart van het model (../barstfrac.npy: black-hat van de modelhelderheid)
import numpy as np, heapq; from PIL import Image; from scipy import ndimage
k=np.load('../kaal.npy'); r3=np.load('../r3/idx.npy'); o=r3.copy()
fr=np.load('../barstfrac.npy')
a=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(float); lum=a.mean(2)
S=13.0; X0=51.0; Y0=126.5
J,I=np.mgrid[0:64,0:64]
fig=o>0
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
eye=((I-35.5)**2+(J-28)**2)<=7.6**2
neus=(J>=24)&(J<=33)&(I<=21)          # neusvorm (bevroren, behalve de naad y29)
lab,n=ndimage.label(k>0); main=np.argmax(np.bincount(lab.ravel())[1:])+1
puin=(lab!=main)&(lab>0)
# --- modeltint T
med=np.zeros((64,64))
for j,i in zip(*np.where(fig)):
    ys=slice(int(round(Y0+j*S)),int(round(Y0+(j+1)*S))); xs=slice(int(round(X0+i*S)),int(round(X0+(i+1)*S)))
    L=lum[ys,xs]; L=L[(L>45)&(a[ys,xs].min(-1)<235)]
    med[j,i]=np.median(L) if L.size else 60
def tint(m): return 7 if m>=128 else (5 if m>=86 else (4 if m>=64 else 3))
T=np.vectorize(tint)(med)*fig
STEEN=[3,4,5,7]; RK={3:0,4:1,5:2,7:3}
# --- 1. barstzones leeg + lange modelbreuken als pad
zA=(I>=20)&(I<=30)&(J>=17)&(J<=24)
zB=(I>=16)&(I<=30)&(J>=33)&(J<=39)
zR=(I>=44)&(I<=61)&(J>=17)&(J<=35)
zones=(zA|zB|zR)&fig&~rim&~eye&~neus
o[zones&np.isin(o,[1,2])]=T[zones&np.isin(o,[1,2])]
def pad(p0,p1):
    cost=np.where(fig&~eye,1.05-np.clip(fr,0,1),99.0)
    dist=np.full((64,64),1e9); prev={}; dist[p0]=0; h=[(0,p0)]
    while h:
        d,p=heapq.heappop(h)
        if p==p1: break
        if d>dist[p]: continue
        for dj in (-1,0,1):
            for di in (-1,0,1):
                q=(p[0]+dj,p[1]+di)
                if q==p or not(0<=q[0]<64 and 0<=q[1]<64): continue
                nd=d+cost[q]*(1.0 if dj==0 or di==0 else 1.3)
                if nd<dist[q]: dist[q]=nd; prev[q]=p; heapq.heappush(h,(nd,q))
    P=[p1]
    while P[-1]!=p0: P.append(prev[P[-1]])
    return P[::-1]
# (rij, kolom); eindpunten op modelbarsten met hoge barstfractie
PADEN={'A: lange barst naar linksboven':[(23,23),(20,22),(17,21),(16,19)],
       'B1: neusbasis -> links':[(30,22),(32,21),(33,20),(34,18),(35,16)],
       'B2: neusbasis -> linksonder':[(34,24),(35,22),(36,20),(38,19),(39,18)],
       'B3: neusbasis -> onder':[(35,24),(36,25),(38,26),(39,26)],
       'R1: plaatgrens dwars':[(21,47),(22,50),(23,55)],
       'R2: boog onder de hap omlaag':[(17,56),(18,55),(23,54),(28,55),(31,54)],
       'R3: plaatgrens onder':[(31,54),(31,51),(32,47)],
       'R4: naar de opening rechtsonder':[(31,54),(33,52),(37,52)]}
barst=np.zeros((64,64),bool)
for nm,wp in PADEN.items():
  for p0,p1 in zip(wp[:-1],wp[1:]):
    for p in pad(p0,p1):
        if fig[p] and not rim[p] and not eye[p]: barst[p]=True
o[barst]=1
# --- 2. hap rechtsboven (x44-51, y10-16): één doorlopende zwarte buitenlijn, binnenwand = modeltint
zH=(I>=44)&(I<=51)&(J>=10)&(J<=16)
o[zH&rim]=1
hb=zH&fig&~rim
o[hb]=np.where(fr[hb]>=0.6,1,T[hb])
# --- 3. kraterringen onderste helft (x24-30, y44-48): modeltint (subtiel, alleen 3/4/5)
zK=(I>=24)&(I<=30)&(J>=44)&(J<=48)&fig&~rim
o[zK]=np.clip(T[zK],3,5)
# --- 4. lichtste tint niet als band langs de rand: 7 direct naast de rand -> 5
nb_rim=ndimage.binary_dilation(rim,structure=[[0,1,0],[1,1,1],[0,1,0]])&~rim
o[nb_rim&(o==7)&~puin&~neus]=5
# --- 5. vlekjes < 3 px (steentinten) -> buurtint die het dichtst bij de modeltint ligt
for _ in range(3):
  for v in STEEN:
    L,nl=ndimage.label(o==v)
    for c in range(1,nl+1):
        m=L==c
        if m.sum()>=3 or (m&(eye|neus)).any(): continue
        ring=ndimage.binary_dilation(m,structure=np.ones((3,3)))&~m
        st=sorted(set(x for x in o[ring] if x in STEEN and x!=v))
        if not st: continue
        t=int(np.median(T[m])); t=t if t in RK else 5
        best=min(st,key=lambda x:abs(RK[x]-RK[t]))
        o[m]=best
# losse/korte binnenlijnen buiten de paden (componenten < 3 px) -> modeltint
inner_line=(o==1)&~rim&~eye&~neus
L,nl=ndimage.label(inner_line,structure=np.ones((3,3)))
for c in range(1,nl+1):
    m=L==c
    touch=(ndimage.binary_dilation(m,structure=np.ones((3,3)))&(rim|eye|neus)&(o==1)).any()
    if m.sum()<3 and not touch: o[m]=T[m]
# --- 6. barstkleur: zwart alleen aan de schaduwkant; in licht/midden -> donkere tint 2; nooit zwart naast 7
for j,i in zip(*np.where((o==1)&~rim&~eye&~neus)):
    st=[x for x in o[j-1:j+2,i-1:i+2].ravel() if x in STEEN]
    four=[o[j-1,i],o[j+1,i],o[j,i-1],o[j,i+1]]
    licht=(not st) or (np.mean([RK[x] for x in st])>=1.5) or (7 in four)
    if licht: o[j,i]=2
# --- 7. naad over de neus (y29, x4-22) selout
o[(J==29)&(I>=4)&(I<=22)&(o==1)]=2
# --- 8. oog: donkerrode vlekjes < 3 px in de iris -> iristint ernaast (hooglicht 10 blijft)
L,nl=ndimage.label((o==8)&eye)
oogfix=0
for c in range(1,nl+1):
    m=L==c
    if m.sum()<3:
        ring=ndimage.binary_dilation(m)&~m; st=[x for x in o[ring] if x in (9,10)]
        if st: o[m]=9; oogfix+=int(m.sum())
PAL=np.array([(0,0,0),(24,16,16),(60,22,28),(88,32,34),(138,56,50),(182,86,76),(204,108,92),(214,122,102),
              (168,20,24),(222,50,44),(236,128,112)],float)
np.save('idx.npy',o)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
save(o,'sprite.png'); save(o,'sprite_8x.png',8)
# ---- rapport
zw_in=int(((o==1)&~rim&~eye).sum()); zw_in_r3=int(((r3==1)&~rim&~eye).sum())
zw_all_in=int(((o==1)&~rim).sum()); zw_all_in_r3=int(((r3==1)&~rim).sum())
vl=0; vls=0
for v in [2,3,4,5,7,8,9]:
    L,nl=ndimage.label(o==v); s=np.bincount(L.ravel())[1:]; vl+=int((s<3).sum())
    if v in STEEN: vls+=sum(1 for c in range(1,nl+1) if s[c-1]<3 and not ((L==c)&(eye|neus|puin)).any())
vl3=0
for v in [2,3,4,5,7,8,9]:
    L,nl=ndimage.label(r3==v); s=np.bincount(L.ravel())[1:]; vl3+=int((s<3).sum())
gez=(eye|neus)
gez_diff=(o!=r3)&gez; naad_neus=(J==29)&(I>=4)&(I<=22)
Z=np.full((64,64),'lijf',dtype=object); Z[eye]='oog'; Z[neus]='neus'; Z[puin]='puin'
dif=(o!=k)
with open('wijzigingen.txt','w') as f:
  f.write('Ronde 4 (keuring r3: netheid)\n')
  f.write('Pixels afwijkend van de kale reductie per zone:\n')
  for z in ['oog','neus','lijf','puin']:
    m=(Z==z)&((k>0)|(o>0)); f.write(f'  {z:5s}: {int((dif&m).sum()):4d} van {int(m.sum())}\n')
  f.write(f'  totaal: {int(dif.sum())}; verschil met r3: {int((o!=r3).sum())}\n')
  f.write(f'Silhouet (alpha) t.o.v. r3 en kale reductie: {int(((o>0)!=(r3>0)).sum())} / {int(((o>0)!=(k>0)).sum())} px\n')
  f.write(f'Gezicht t.o.v. r3: oog {int((gez_diff&eye).sum())} px (punt 4: {oogfix} donkerrode irisvlekjes -> iris), '
          f'neus {int((gez_diff&neus&~naad_neus).sum())} px buiten de naad, naad y29 {int((gez_diff&naad_neus).sum())} px zwart -> selout (punt 6)\n')
  f.write(f'Zwart binnenin (geen rand, zonder oog): {zw_in} (r3: {zw_in_r3}); met oogrand+pupil: {zw_all_in} (r3: {zw_all_in_r3})\n')
  f.write(f'Vlekjes < 3 px (tinten 2,3,4,5,7,8,9, incl. lijnstukjes en selout-stukjes): {vl} (r3: {vl3}); steentint-vlekjes in het lijf: {vls}\n')
  f.write('Tinthelderheid (r+g+b)/3: '+', '.join(f'{i}:{int(PAL[i].mean())}' for i in [1,2,3,4,5,7,8,9,10])+'\n')
  f.write('Barstpaden (goedkoopste route over de modelbarstkaart):\n')
  for nm,wp in PADEN.items(): f.write(f'  {nm}: '+' -> '.join(f'(x{p[1]},y{p[0]})' for p in wp)+'\n')
print(open('wijzigingen.txt').read())
