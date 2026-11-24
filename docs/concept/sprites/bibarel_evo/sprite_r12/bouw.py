# bouw.py ronde 12 (vanaf sprite_r11 = A+B). Jordi 24 nov. Bevroren: tanden, onderkant lijf, potlood, staart, ogen/neus.
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r12/bouw.py
import numpy as np
from PIL import Image, ImageDraw
im11=Image.open('sprite_r11/sprite.png'); PAL=np.array(im11.getpalette()[:48]).reshape(16,3).astype('uint8')
r11=np.asarray(im11).astype(int); r10=np.asarray(Image.open('sprite_r10/sprite.png')).astype(int)
L={'K':1,'b':2,'c':3,'d':4,'f':5,'S':6,'C':7,'e':8,'M':10,'D':15}
o=r11.copy(); log={}
def zet(n,d):
    for (x,y),v in d.items(): o[y,x]=L[v] if isinstance(v,str) else v; log.setdefault(n,[]).append((x,y))
# 1. helm: rechte klep-onderrand r14 x21-34 (14 px) -> boog die de kop volgt (rijen 13,14,15,14,13; runs <= 3)
H={}
for x in range(21,35): H[(x,14)]='c'                     # onderkant helm (schaduwkant van de klep)
for x in (21,22): H[(x,14)]='S'                           # vrijgekomen: gezicht zoals rij 15 eronder
for x in (32,33,34): H[(x,14)]='C'
for x in (20,21,22,32,33,34): H[(x,13)]='b'
for x in (23,24,25,29,30,31): H[(x,14)]='b'
for x in (26,27,28): H[(x,15)]='b'
zet('1 helm',H)
# 2. rechterkant kraag: rechte verticale lijn x43 r20-23 -> bolletjesrand (uitbol r19-22, inkeping r23)
zet('2 kraag rechts',{(43,19):'K',(43,20):'c',(44,20):'K',(43,21):'c',(44,21):'K',(42,23):'K'})
# 3. linkerkant kraag: bollen heel en rond (over de rand van hand/stam)
zet('3 kraag links',{(17,17):'b',(18,17):'f',(17,18):'b',(18,18):'f',
                     (17,20):'b',(16,21):'b',(17,21):'f',(16,22):'b',(17,23):'b'})
# 4. zakje: één tint donkerder (licht crème -> crème-midden), afgeronde hoeken
Z={}
for y in range(38,44):
    for x in range(23,33): Z[(x,y)]='M'
for x in range(22,34): Z[(x,37)]='D' if 24<=x<=31 else 'C'
for y in range(38,44): Z[(22,y)]='S' if 39<=y<=42 else 'C'; Z[(33,y)]='S' if 39<=y<=42 else 'M'
for p in ((23,38),(32,38),(23,43),(24,43),(31,43),(32,43)): Z[p]='S'
for x in range(23,33): Z[(x,44)]='S' if 25<=x<=30 else ('C' if x<25 else 'M')
zet('4 zakje',Z)
# 5. inham bovenrand borststuk 1 px naar links; schouderpuntjes terug naar r10
zet('5 inham',{(26,34):'c',(27,34):'c',(28,34):'d',(29,34):'d',(30,34):'d',(31,34):'C',(28,35):'c',(29,35):'C'})
zet('5 puntjes terug',{(x,y):int(r10[y,x]) for x,y in ((34,29),(35,29),(36,29),(37,29),(34,30),(35,30))})
def save(idx,pad,z=None):
    im=Image.new('P',(64,64)); im.putpalette(PAL.ravel().tolist()+[0]*3*240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad,transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64*z,64*z),Image.NEAREST).save(pad.replace('.png',f'_{z}x.png'))
save(o,'sprite_r12/sprite.png',8)
# ---- bewijs
ZONES={'helm':(20,34,13,15),'kraag r':(42,44,19,23),'kraag l':(16,18,17,23),'zakje':(22,33,37,44),'inham':(26,31,34,35),'puntjes':(34,37,29,30)}
inz=lambda x,y:any(a<=x<=b and c<=y<=d for a,b,c,d in ZONES.values())
dd=[(int(x),int(y)) for y,x in np.argwhere(o!=r11)]
print('gewijzigd:',len(dd),'| buiten zones:',[p for p in dd if not inz(*p)],'| silhouet gelijk:',((o>0)==(r11>0)).all())
B={'tanden':(22,28,22,27),'onderkant':(14,46,45,63),'potlood':(0,12,12,30),'staart':(46,63,18,50),'ogen':(22,23,15,18),'ogen r':(30,32,15,18),'neus':(22,25,19,21)}
for n,(a,b_,c,d) in B.items(): print('bevroren',n,int((o[c:d+1,a:b_+1]!=r11[c:d+1,a:b_+1]).sum()))
print('puntjes gelijk aan r10:',all(o[y,x]==r10[y,x] for x,y in ((34,29),(35,29),(36,29),(37,29),(34,30),(35,30))))
for k,v in log.items(): print(k,len(v))
# runs in helm-onderrand
for y in (13,14,15):
    run=0;mx=0
    for x in range(19,37):
        run=run+1 if o[y,x]==2 else 0; mx=max(mx,run)
    print('helm rij',y,'langste lijnrun',mx)
print('kraag rechts lijnkolommen:',{x:[y for y in range(18,26) if o[y,x]==1] for x in (42,43,44)})
# ---- vel: r12 | r11 (8x); kop 12x; borststuk 12x met pijl bij de inham
big=lambda idx,z,box=(0,0,64,64):Image.fromarray(PAL[idx]).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
V=Image.new('RGB',(1060,1500),'white'); d=ImageDraw.Draw(V)
for i,(idx,t) in enumerate([(o,'r12'),(r11,'r11')]):
    V.paste(big(idx,8),(10+i*522,30)); d.text((10+i*522,10),t+' 8x',fill='black')
y0=580; kb=(12,6,48,32)
for i,(idx,t) in enumerate([(o,'kop r12 12x'),(r11,'kop r11 12x')]):
    V.paste(big(idx,12,kb).resize((36*12//1*1,26*12)),(10+i*450,y0+20)); d.text((10+i*450,y0),t,fill='black')
y0+=360; bb=(16,30,40,46)
for i,(idx,t,px) in enumerate([(o,'borststuk r12 12x (pijl: inham, nu 1 px links)',28),(r11,'borststuk r11 12x (pijl: inham)',29)]):
    X0=10+i*450; V.paste(big(idx,12,bb),(X0,y0+20)); d.text((X0,y0),t,fill='black')
    cx,cy=X0+(px-bb[0])*12+6,y0+20+(35-bb[1])*12+6
    d.line([(cx-40,cy-60),(cx-3,cy-6)],fill=(0,90,255),width=3); d.polygon([(cx-1,cy-2),(cx-12,cy-8),(cx-5,cy-14)],fill=(0,90,255))
y0+=230
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,idx in enumerate((o,r11)):
        t=Image.new('RGB',(64,64),bg); t.paste(Image.fromarray(PAL[idx]),(0,0),Image.fromarray(((idx>0)*255).astype('uint8'))); V.paste(t,(10+i*80,y0+20+j*80))
d.text((10,y0),'1x: r12, r11',fill='black')
V.crop((0,0,1060,y0+190)).save('sprite_r12/vel.png')
