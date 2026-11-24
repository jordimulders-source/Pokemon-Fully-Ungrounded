# Ronde 7 vanaf r6: alleen benoemde pixelreparaties uit de keuring van r5.
import numpy as np; from PIL import Image, ImageDraw
PAL=np.array([(0,0,0),(24,16,16),(60,22,28),(88,32,34),(138,56,50),(182,86,76),(204,108,92),(214,122,102),
              (168,20,24),(222,50,44),(236,128,112),(112,12,18)],float)
def save(o,fn,sc=1):
  im=Image.fromarray(o.astype('uint8'),'P'); p=[int(v) for v in PAL.ravel()]; im.putpalette(p+[0]*(768-len(p)))
  if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
  im.save(fn,transparency=0)
def rgb(o,sc=1,bg=(230,230,230)):
  a=PAL[o].astype('uint8'); a[o==0]=bg; return Image.fromarray(a).resize((64*sc,64*sc),Image.NEAREST)
o0=np.load('../v16_r6/idx.npy'); o=o0.copy(); log=[]
def zet(x,y,v,why):
    log.append(f'({x},{y}) {o[y,x]} -> {v}  {why}'); o[y,x]=v
# 1 niet uitgevoerd: het model heeft op (10-13,32), (13-15,33), (14-16,34) zelf tint 4 tussen tint 2 (lichte lip onder de neus)
log.append('punt 1: NIET gedaan - model v16 heeft daar zelf tint 4 tussen tint 2 (lichte lip langs de neusbuik); gemeld en gelaten')
# 2 puin rechtsonder: lichte bovenrand van 4 px (44-47,45)
zet(45,45,5,'punt 2: lichte bovenrand puin rechtsonder (44-47,45)')
# 3
zet(14,23,5,'punt 3'); zet(14,24,5,'punt 3'); zet(17,35,2,'punt 3 (punt 1 vervallen)')
# 4 buurtint
zet(39,47,1,'punt 4: alleen omringd door lijn (5 van 8 buren zwart, steen alleen diagonaal 3) -> lijnkleur')
for x,y in [(50,15),(40,11),(52,19)]:
    st=[int(v) for v in o[y-1:y+2,x-1:x+2].ravel() if v in (2,3,4,5,7)]; st.remove(int(o[y,x])) if int(o[y,x]) in st else None
    st=[v for v in st if v!=o[y,x]] or st
    zet(x,y,max(set(st),key=st.count),'punt 4: buurtint')
zet(31,53,1,'punt 4: onderrand')
np.save('idx.npy',o); save(o,'sprite.png'); save(o,'sprite_8x.png',8)
r5=np.load('../v16_r5/idx.npy')
V=Image.new('RGB',(16+2*528,640),(230,230,230)); d=ImageDraw.Draw(V)
for k,(a,t) in enumerate([(r5,'v16 r5'),(o,'v16 r7')]):
    V.paste(rgb(a,8),(16+k*528,30)); d.text((16+k*528,10),t,fill=(0,0,0))
    for j,bg in enumerate([(240,240,240),(48,48,56)]): V.paste(rgb(a,1,bg),(16+k*528+j*80,560))
V.save('vel.png')
dif=o!=o0
log.append(f'totaal t.o.v. r6: {int(dif.sum())} px (alle in de lijst hierboven; verder pixeldiff 0)')
open('wijzigingen.txt','w').write('Ronde 7 vanaf v16_r6 (keuring r5, benoemde pixels)\n'+'\n'.join(log)+'\n'); print('\n'.join(log))
