# Ronde 9 vanaf v16_r8/B_2px_donker.png (bevroren keuze Jordi). Alleen de twee dwarsbarstjes rechts van het oog:
# ze liepen ook in A en in het model niet tegen de ring (3-4 px lijf ertussen); door de verschuiving staan ze nu dichter bij
# het oog en lezen als losse streepjes. Oplossing: taps uitlopen in de lijftint aan de oogkant (loop/lengte blijft).
import numpy as np; from PIL import Image, ImageDraw
src=Image.open('../v16_r8/B_2px_donker.png'); pal=src.getpalette()
o0=np.array(src); o=o0.copy(); log=[]
def zet(x,y,v,why):
    log.append(f'({x},{y}) {o[y,x]} -> {v}  {why}'); o[y,x]=v
# rechtsboven: zwarte barst y21 x41-45 -> oogkant taps: x41 tint 3, x42 tint 2
zet(41,21,3,'barst rechtsboven: punt aan de oogkant taps (lijf 4/5 ernaast)'); zet(42,21,2,'idem, tussenstap')
# rechtsonder: donkere barst (tint 2) y32 x41-45 -> oogkant taps: x41 tint 3
zet(41,32,3,'barst rechtsonder: punt aan de oogkant taps')
def save(a,fn,sc=1):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal)
    if sc>1: im=im.resize((64*sc,64*sc),Image.NEAREST)
    im.save(fn,transparency=0)
save(o,'sprite.png'); save(o,'sprite_8x.png',8); np.save('idx.npy',o)
P=np.array(pal[:48]).reshape(-1,3)
def rgb(a,sc=1,bg=(230,230,230)):
    b=P[a].astype('uint8'); b[a==0]=bg; return Image.fromarray(b).resize((64*sc,64*sc),Image.NEAREST)
V=Image.new('RGB',(16+2*528,640),(230,230,230)); d=ImageDraw.Draw(V)
for k,(a,t) in enumerate([(o0,'r8 B_2px_donker'),(o,'v16 r9')]):
    V.paste(rgb(a,8),(16+k*528,30)); d.text((16+k*528,10),t,fill=(0,0,0))
    for j,bg in enumerate([(240,240,240),(48,48,56)]): V.paste(rgb(a,1,bg),(16+k*528+j*80,560))
V.save('vel.png')
log.append(f'totaal {int((o!=o0).sum())} px t.o.v. B_2px_donker; oog/neus/silhouet 0. Vrijgekomen strook links van het oog (x28-31, y21-35) gecontroleerd: alleen doorlopende lijftinten 4/5, geen losse pixels of spookkas; niets veranderd.')
open('wijzigingen.txt','w').write('Ronde 9 vanaf v16_r8/B_2px_donker.png\n'+'\n'.join(log)+'\n'); print('\n'.join(log))
