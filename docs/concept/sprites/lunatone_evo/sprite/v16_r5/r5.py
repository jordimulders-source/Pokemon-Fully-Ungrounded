# Ronde 5 vanaf v16_r2 A (Jordi: "r2a is wel de beste" / "over het hele lichaam slim met schaduw spelen voor het perspectief").
# Silhouet, lijnen, oog, neusvorm en de donkere rechterband (incl. scheiding) blijven; alleen steentinten worden opnieuw verdeeld:
#  basis = bol met licht linksboven (Lambert, c=(35.2,30.5), R=23.5), niveaus 3/4/5/7; modeltextuur blijft als +-1 niveau t.o.v. de
#  gladgestreken modeltint; kraters: donker aan de lichtkant binnenin, lichte rand rechtsonder; neusschaduw op de bol eronder;
#  puin per stuk licht linksboven / donker rechtsonder, stukken rechts (achter de bol) 1 niveau donkerder.
import numpy as np; from scipy import ndimage; import tool
o0=np.load('../v16_r2/idx.npy'); o=o0.copy()
J,I=np.mgrid[0:64,0:64]; fig=o>0
LV=[2,3,4,5,7]; RK={2:0,3:1,4:2,5:3,7:4}
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
lab,n=ndimage.label(fig); s=np.bincount(lab.ravel()); s[0]=0; main=lab==np.argmax(s)
ring=(o==1)&(I>=24)&(I<=40)&(J>=20)&(J<=38)
eye=ndimage.binary_dilation(ndimage.binary_fill_holes(ring),iterations=2)
neus=(I<=24)&(J>=22)&(J<=34)&main
# rechterband: donker gebied (1/2/3) dat aan de rechterrand hangt
dark=np.isin(o,[1,2,3])&main&(I>=44)
bl,bn=ndimage.label(dark); band=np.zeros((64,64),bool)
for k in range(1,bn+1):
    m=bl==k
    if (m&rim&(I>=50)).any() and m.sum()>=20: band|=m
band=ndimage.binary_fill_holes(band|(rim&(I>=50)))&main&(I>=44)
stone=np.isin(o,[3,4,5,7])
tgt=main&stone&~rim&~eye&~neus&~band
# 1. bol-belichting
cx,cy,R=35.2,30.5,23.5
dx=(I+.5-cx)/R; dy=(J+.5-cy)/R; rr=np.clip(dx*dx+dy*dy,0,0.98); dz=np.sqrt(1-rr)
L=np.array([-0.62,-0.62,0.48]); L/=np.linalg.norm(L)
lam=dx*L[0]+dy*L[1]+dz*L[2]
base=np.select([lam>0.80,lam>0.52,lam>0.22],[4,3,2],1)   # niveau-index in LV
# 2. modeltextuur als +-1
lv=np.vectorize(lambda v:RK.get(v,2))(o).astype(float)
sm=ndimage.uniform_filter(np.where(stone&main,lv,np.nan_to_num(lv)),5)
det=np.clip(np.round((lv-sm)*0.9),-1,1)
new=np.clip(base+det,1,4).astype(int)
# 3. neusschaduw op de bol: strook direct onder/rechts van de neus
nsch=main&~neus&~eye&(J>=33)&(J<=37)&(I>=12)&(I<=27)&ndimage.binary_dilation(neus,iterations=3)
new[nsch]-=1
# 4. kraters: donkere modelvlekken (niveau <= 2, 4-40 px) in het lichte deel
K=tgt&(lv<=2)&(lam>0.5)
kl,kn=ndimage.label(K); krat=0
for k in range(1,kn+1):
    m=kl==k
    if not 4<=m.sum()<=40: continue
    new[m]=np.minimum(new[m],2)
    ul=m&~np.roll(np.roll(m,1,0),1,1)            # binnenrand linksboven: donkerst
    new[ul]=1
    lr=np.roll(np.roll(m,1,0),1,1)&~m&tgt       # rand rechtsonder buiten de krater: licht
    new[lr]=np.minimum(new[lr]+1,4); krat+=1
new=np.clip(new,1,4)
o[tgt]=np.array(LV)[new[tgt]]
# 5. puin: per stuk
puin=fig&~main; pl,pn=ndimage.label(puin)
for k in range(1,pn+1):
    m=pl==k; ys,xs=np.where(m); pcx,pcy=xs.mean(),ys.mean()
    achter=pcx>40
    inn=m&~rim&np.isin(o,[3,4,5,7])
    for y,x in zip(*np.where(inn)):
        t=-(x-pcx)-(y-pcy)
        v=4 if t>0.8 else (3 if t>-0.8 else 2)
        if achter: v-=1
        o[y,x]=LV[max(v,1)]
# 5b. oog (Jordi: "ook rechts in het oog"): iris rechts/rechtsonder donkerder (9 -> 8), pupil en hooglicht blijven
IR=np.isin(o,[8,9,10])&eye
ys,xs=np.where(IR); ecx,ecy=xs.mean()+.5,ys.mean()+.5; er=max(np.ptp(xs),np.ptp(ys))/2+.5
el=-0.75*(I+.5-ecx)/er-0.45*(J+.5-ecy)/er
oogm=IR&(o==9)&(el<-0.30)
o[oogm]=8
# 6. technische punten keurder
def box(x0,x1,y0,y1): return (I>=x0)&(I<=x1)&(J>=y0)&(J<=y1)
m=box(6,19,30,31)&(o==2)&~rim; o[m]=3; t4=int(m.sum())
t5=0
for x,y in [(45,10),(45,13),(44,14),(44,16),(44,17),(45,18)]:
    if o[y,x]==2: o[y,x]=1; t5+=1
m=box(17,21,33,35)&rim&(o==2); o[m]=1; t5+=int(m.sum())
t7=0
for x,y in [(37,44),(37,45),(38,46),(39,49),(39,50),(39,51)]:
    if o[y,x]==1 and not rim[y,x]:
        st=[v for v in o[y-1:y+2,x-1:x+2].ravel() if v in (3,4,5)]; o[y,x]=max(set(st),key=st.count); t7+=1
# tintvlekjes < 3 px -> meest voorkomende buurtint (niet in oog/neus)
vl=0
for _ in range(3):
  for v in (3,4,5,7):
    L2,nl=ndimage.label(o==v)
    for c in range(1,nl+1):
        m=L2==c
        if m.sum()>=3 or (m&(eye|neus)).any(): continue
        r2=ndimage.binary_dilation(m,structure=np.ones((3,3)))&~m
        st=[t for t in o[r2] if t in (3,4,5,7) and t!=v]
        if st: o[m]=max(set(st),key=st.count); vl+=int(m.sum())
np.save('idx.npy',o); tool.save(o,'sprite.png'); tool.save(o,'sprite_8x.png',8)
dif=o!=o0
rep0=0
rep=[f'v16_r5 (vanaf v16_r2 A): {int(dif.sum())} px gewijzigd; oog {int((dif&eye).sum())}; silhouet {int(((o>0)!=(o0>0)).sum())}; rechterband {int((dif&band).sum())}; neusvorm (zwart/selout in neus) {int((dif&neus&(np.isin(o0,[1,2])|np.isin(o,[1,2]))).sum())}',
 f'  oog: {int(oogm.sum())} irispixels 9->8 (rechterkant donkerder; pupil, hooglicht en ring ongewijzigd)',
 f'  lijf herbelicht: {int((dif&tgt).sum())} px; kraters: {krat}; neusschaduw: {int(nsch.sum())} px; puin: {int((dif&puin).sum())} px',
 f'  keurderpunten: onder de neus 2->3: {t4}; randpixels ->zwart: {t5}; dubbele barst: {t7}; vlekjes: {vl}']
print('\n'.join(rep)); open('wijzigingen.txt','w').write('\n'.join(rep)+'\n')
np.save('band.npy',band)
