# Ronde 8 vanaf r7. (1) neus-lijfaansluiting: één naad (tint 2) die de barst x18 doortrekt naar de bestaande naad x21 (y25-27),
# rafelpixels -> neusbasis-schaduw (4, zoals de modelstrook x19-20) of lijftint (5, zoals ernaast). (2) oog naar Lunatone:
# pupil 1 px omlaag (gecentreerd in de iris zoals Lunatone, blik niet meer omhoog); irisrand links/onder donker 1 (8) zoals Lunatones
# donkere irisrand rondom; hooglicht, ring en de donkere sikkel rechts (r6) blijven. (3) varianten: oog 0/2/4 px naar rechts.
import numpy as np; from PIL import Image, ImageDraw; from scipy import ndimage
PAL=np.array([(0,0,0),(24,16,16),(60,22,28),(88,32,34),(138,56,50),(182,86,76),(204,108,92),(214,122,102),
              (168,20,24),(222,50,44),(236,128,112),(112,12,18)],float)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
def rgb(a,sc=1,bg=(230,230,230)):
  b=PAL[a].astype('uint8'); b[a==0]=bg; return Image.fromarray(b).resize((a.shape[1]*sc,a.shape[0]*sc),Image.NEAREST)
o0=np.load('../v16_r7/idx.npy'); o=o0.copy(); log=[]
def zet(x,y,v,why):
    if o[y,x]!=v: log.append(f'({x},{y}) {o[y,x]} -> {v}  {why}'); o[y,x]=v
# 1. neus
for x,y in [(18,23),(19,24),(20,25),(21,26),(21,27)]: zet(x,y,2,'naad neus/lijf')
zet(19,23,5,'rafel rechts van de naad -> lijftint'); zet(20,24,5,'idem'); zet(21,25,5,'dubbele naad -> lijftint')
zet(18,24,4,'rafel links van de naad -> neusbasis-schaduw'); zet(19,25,4,'idem'); zet(19,27,4,'neusbasis-strook doorlopend')
zet(20,31,3,'los pixel in de neusbuik -> buiktint')
n1=len(log)
# 2. oog
J,I=np.mgrid[0:64,0:64]
blk=(o==1)&(I>=24)&(I<=40)&(J>=20)&(J<=38)
eye=ndimage.binary_fill_holes(blk)
bl,bn=ndimage.label(blk); sz=np.bincount(bl.ravel()); sz[0]=0
ring=bl==np.argmax(sz)                      # grootste zwarte stuk = oogring
eye=ndimage.binary_fill_holes(ring)
pup=eye&blk&~ring                           # zwart binnen de ring = pupil
inside=eye&~ring
ys,xs=np.where(pup)
for y,x in sorted(zip(ys,xs),reverse=True): pass
newp=np.zeros_like(pup); newp[1:]=pup[:-1]
vac=pup&~newp
for y,x in zip(*np.where(newp&~pup)): zet(x,y,1,'pupil 1 px omlaag')
for y,x in zip(*np.where(vac)):
    st=[v for v in o[y-1:y+2,x-1:x+2].ravel() if v in (8,9,10)]
    zet(x,y,9 if 9 in st else max(set(st),key=st.count),'vrijgekomen pupilplek -> iris')
IR=inside&np.isin(o,[9])
ecx=np.where(inside)[1].mean()
adj=IR&ndimage.binary_dilation(ring,structure=[[0,1,0],[1,1,1],[0,1,0]])&((I<ecx)|(J>=np.where(inside)[0].mean()+2))
for y,x in zip(*np.where(adj)): zet(x,y,8,'irisrand links/onder donker 1 (Lunatone)')
n2=len(log)-n1
np.save('idx.npy',o); save(o,'sprite.png'); save(o,'sprite_8x.png',8); save(o,'A_0px.png')
# 3. varianten
def schuif(o,dx):
    s=o.copy(); E=eye
    for y in range(64):
        xs_=np.where(E[y])[0]
        if not len(xs_): continue
        x0=xs_.min(); left=o[y,x0-1]
        for x in range(x0,x0+dx): s[y,x]=left if left in (3,4,5,7) else 5
    for y,x in zip(*np.where(E)): s[y,x+dx]=o[y,x]
    return s
B=schuif(o,2); C=schuif(o,4); save(B,'B_2px.png'); save(C,'C_4px.png'); save(B,'B_2px_8x.png',8); save(C,'C_4px_8x.png',8)
np.save('B.npy',B); np.save('C.npy',C)
# vel
L=Image.open('../../../../../../graphics/pokemon/lunatone/anim_front.png').convert('RGB').crop((0,0,64,64))
V=Image.new('RGB',(16+4*528,1000),(230,230,230)); d=ImageDraw.Draw(V)
for k,(a,t) in enumerate([(o0,'v16 r7'),(o,'r8 A (0 px)'),(B,'r8 B (2 px)'),(C,'r8 C (4 px)')]):
    V.paste(rgb(a,8),(16+k*528,30)); d.text((16+k*528,10),t,fill=(0,0,0))
    cx=[0,0,0,0,2,4][k+1] if k>0 else 0
    sh=[0,0,2,4][k]
    V.paste(rgb(a[18:38,24+sh:42+sh],16),(16+k*528,560))
    for j,bg in enumerate([(240,240,240),(48,48,56)]): V.paste(rgb(a,1,bg),(16+k*528+j*80,900))
d.text((16,545),'oog 16x',fill=(0,0,0))
V2=Image.new('RGB',(V.width,V.height+340),(230,230,230)); V2.paste(V,(0,0))
V2.paste(L.crop((30,20,48,40)).resize((288,320),Image.NEAREST),(16,1010)); ImageDraw.Draw(V2).text((320,1010),'Lunatone (Gen 3) oog 16x',fill=(0,0,0))
V2.save('vel.png')
rep=['Ronde 8 vanaf v16_r7']+log+[f'neus: {n1} px; oog: {n2} px; totaal A t.o.v. r7: {int((o!=o0).sum())} px; silhouet {int(((o>0)!=(o0>0)).sum())}',
 f'varianten: B = oog (ring+binnen) 2 px naar rechts ({int((B!=o).sum())} px anders dan A), C = 4 px ({int((C!=o).sum())} px); vrijgekomen strook links = lijftint direct links van het oog in die rij']
open('wijzigingen.txt','w').write('\n'.join(rep)+'\n'); print('\n'.join(rep))
