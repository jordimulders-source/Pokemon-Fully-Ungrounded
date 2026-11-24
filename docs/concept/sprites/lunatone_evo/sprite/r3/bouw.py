# Ronde 3 (vanaf r2/idx.npy): puinstukken binnenin terug naar de kale reductie (geen barstverbindingen,
# die maakten van een stukje een 'G'); losse zwarte pixels controleren. Rest bevroren.
import numpy as np; from PIL import Image; from scipy import ndimage
k=np.load('../kaal.npy'); o=np.load('../r2/idx.npy').copy(); r2=o.copy()
a=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(float); lum=a.mean(2)
S=13.0; X0=51.0; Y0=126.5
STEEN=[3,4,5,7]
fig=o>0
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
lab,n=ndimage.label(k>0); main=np.argmax(np.bincount(lab.ravel())[1:])+1
puin=(lab!=main)&(lab>0)
def tint(j,i,v):
    if v!=6: return v
    ys=slice(int(round(Y0+j*S)),int(round(Y0+(j+1)*S))); xs=slice(int(round(X0+i*S)),int(round(X0+(i+1)*S)))
    L=lum[ys,xs][lum[ys,xs]>40]; return 7 if np.median(L)>=128 else 5
for j,i in zip(*np.where(puin&~rim)):
    v=k[j,i]
    if v==1:
        nb=[k[y,x] for y in range(j-1,j+2) for x in range(i-1,i+2) if k[y,x] in (3,4,5,6,7)]
        v=max(set(nb),key=nb.count) if nb else 4
    o[j,i]=tint(j,i,v)
# losse zwarte binnenpixels (geen 8-buur lijn) in het lijf
J,I=np.mgrid[0:64,0:64]; eye=((I-35.5)**2+(J-28)**2)<=7.6**2
los=0
for j,i in zip(*np.where((o==1)&~rim&~eye)):
    n8=o[j-1:j+2,i-1:i+2]
    if (np.isin(n8,[1,2]).sum()-1)==0:
        nb=[v for v in n8.ravel() if v in STEEN]; o[j,i]=max(set(nb),key=nb.count); los+=1
print('losse zwarte pixels weg:',los)
np.save('idx.npy',o)
PAL2=np.array([(0,0,0),(24,16,16),(64,24,30),(100,36,38),(138,52,44),(180,78,62),(204,108,92),(232,152,132),
               (168,20,24),(222,50,44),(236,128,112)],float)
def save2(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL2.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
save2(o,'sprite.png'); save2(o,'sprite_8x.png',8)
# zones zoals r2
PC=(29.2,37.3); pr=np.sqrt((I-PC[1])**2+(J-PC[0])**2)
ox,oy=(530-51)/13-0.5,(508-126.5)/13-0.5; rx,ry=112/13+0.7,120/13+0.7
oud=(((I-ox)/rx)**2+((J-oy)/ry)**2<=1)&~eye
Z=np.full((64,64),'lijf',dtype=object); Z[eye]='oog'; Z[oud|((pr>=7.0)&(pr<=10.4)&(I>=38)&~eye)]='naad'
Z[(J>=24)&(J<=33)&(I<=27)&(Z=='lijf')]='neus'; Z[puin]='puin'
dif=(o!=k); fig2=(k>0)|(o>0)
with open('wijzigingen.txt','w') as f:
  f.write('Ronde 3: pixels afwijkend van de kale reductie (../kaal.png), per zone (index-verschil)\n')
  for z in ['oog','naad','neus','lijf','puin']:
    m=(Z==z)&fig2; f.write(f'{z:5s}: {int((dif&m).sum()):4d} van {int(m.sum())}\n')
  f.write(f'totaal: {int(dif.sum())}\nalpha-diff (silhouet): {int(((k>0)!=(o>0)).sum())}\n')
  f.write(f'verschil met r2: {int((o!=r2).sum())} px (alleen puin binnenin + {los} losse zwarte pixels)\n')
  f.write('Wat er gebeurde t.o.v. r2: binnenkant van de puinstukken terug naar de kale reductie (barstverbindingen maakten\n'
          'van het stukje linksonder een G-vorm); zwarte kale pixels in puin -> buurtint; tint 6 -> 7/5 volgens modelhelderheid.\n')
print(open('wijzigingen.txt').read())
