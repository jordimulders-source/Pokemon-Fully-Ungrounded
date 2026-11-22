# Ronde 4 = keuring v16_r3 punten 1-7 (keurdertint k = paletindex k+1: tint 1 = index 2, tint 2 = 3, tint 3 = 4; zwart = index 1).
# Niets getekend: tinten uit model (modellum.npy = helderheid van het natieve modelraster op spritecoördinaten) of omgeving.
import sys, numpy as np; from scipy import ndimage; import tool
VAR,src,dst=sys.argv[1],sys.argv[2],sys.argv[3]
o0=np.load(src); o=o0.copy(); gm=np.load('../v16_r1/groot_model.npy'); ML=np.load('modellum.npy')
J,I=np.mgrid[0:64,0:64]; fig=o>0
rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
cnt={}
def box(x0,x1,y0,y1): return (I>=x0)&(I<=x1)&(J>=y0)&(J<=y1)
def zet(m,v,k):
    m=m&(o!=v); o[m]=v; cnt[k]=cnt.get(k,0)+int(m.sum())
# 1 (B) puinstuk rechtsonder: index-2-vlak -> 3/4 naar modelhelderheid (<37 -> 3, anders 4); zwarte naad blijft
if VAR=='B':
    f=box(42,50,43,53)&(o==2)&~rim
    zet(f&(ML<37),3,'1 puinstuk ->3'); zet(f&(ML>=37),4,'1 puinstuk ->4')
# 2 rechterrand y21-38: index 2 direct binnen de zwarte rand -> 3
nb=ndimage.binary_dilation(rim&(o==1),structure=[[0,1,0],[1,1,1],[0,1,0]])&~rim
zet(box(50,63,21,38)&nb&(o==2),3,'2 rand-binnenkolom')
# 3 gebogen barst uit het model (zwarte modelpixels x40-52, y8-31, binnen 3/4/5, geen rand) -> 3
curve=box(40,52,8,31)&(gm==1)&~rim&np.isin(o,[4,5])
zet(curve,3,'3 gebogen barst (index 3)')
# dwarsbarsten: index 2, laatste pixel rechts 3 (taps)
for y,x0,x1 in [(23,47,51),(30,47,50),(36,53,55)]:
    m=box(x0,x1,y,y)&(o==1)&~rim
    xs=np.where(m[y])[0]
    if len(xs):
        zet(box(xs.min(),xs.max()-1,y,y)&m,2,'3 dwarsbarst ->2'); zet(box(xs.max(),xs.max(),y,y)&m,3,'3 dwarsbarst eind ->3')
# 4 onder de neus y30-31, x6-19: index 2 -> 3 (buitenrand blijft)
zet(box(6,19,30,31)&(o==2)&~rim,3,'4 onder de neus')
# 5 één lijnkleur per randstuk (schaduwkant zwart)
P=[(45,10),(45,13),(44,14),(44,16),(44,17),(45,18)]
m=np.zeros((64,64),bool)
for x,y in P: m[y,x]=o[y,x]==2
m|=box(17,21,33,35)&rim&(o==2)
zet(m,1,'5 randpixels ->zwart')
# 6 tintvlekjes -> meest voorkomende buurtint (8-buren, zelfde tintgroep)
V=[(50,15),(14,23),(14,24),(17,35),(52,19),(4,30),(5,30),(31,53)]+([(44,45),(39,47)] if VAR=='A' else [(47,45),(41,47),(41,48)])
for x,y in V:
    st=[v for v in o[y-1:y+2,x-1:x+2].ravel() if v in (2,3,4,5,7) and v!=o[y,x]]
    if st and o[y,x] in (2,3,4,5):
        mm=np.zeros((64,64),bool); mm[y,x]=True; zet(mm,max(set(st),key=st.count),'6 vlekjes')
# 7 dubbele verticale barst onderrand: binnenste (niet-rand) lijn weg -> buurtint, de doorlopende houden
if VAR=='B': D=[(39,44),(39,45),(39,46)]
else: D=[(37,44),(37,45),(38,46),(39,49),(39,50),(39,51)]
for x,y in D:
    if o[y,x]==1 and not rim[y,x]:
        st=[v for v in o[y-1:y+2,x-1:x+2].ravel() if v in (3,4,5)]
        mm=np.zeros((64,64),bool); mm[y,x]=True; zet(mm,max(set(st),key=st.count),'7 dubbele barst')
np.save(f'{dst}/idx.npy',o); tool.save(o,f'{dst}/sprite.png'); tool.save(o,f'{dst}/sprite_8x.png',8)
ring=(o0==1)&box(24,40,20,38); eye=ndimage.binary_dilation(ndimage.binary_fill_holes(ring),iterations=2)
dif=o!=o0
r=[f'v16_r4{VAR}: {int(dif.sum())} px gewijzigd t.o.v. r3{VAR}; oog {int((dif&eye).sum())} px; silhouet {int(((o>0)!=(o0>0)).sum())} px']
r+= [f'  {k}: {v}' for k,v in cnt.items()]
print('\n'.join(r)); open(f'{dst}/wijzigingen_{VAR}.txt','w').write('\n'.join(r)+'\n')
