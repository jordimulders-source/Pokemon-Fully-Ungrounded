# bouw.py ronde 8 (vanaf r7): precies de 6 keurdersreparaties uit sprite_r7/keuring.md, niets anders.
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r8/bouw.py
# Paletnamen (index): 2 bruin-lijn (96/56/32), 3 bruin-donker, 4 bruin-midden, 6 crème-tan (h), 7 crème licht (k),
# 8 stamkleur (e), 10 NIEUW crème-midden (vrijgemaakt), 15 crème-donker (m).
import numpy as np,sys,collections; sys.path.insert(0,'sprite_r1'); from gemeen import PAL as PAL7, laad
from PIL import Image
r7=laad('sprite_r7/sprite.png'); o=r7.copy()
B,C3,D4,S,C,E,M,D=2,3,4,6,7,8,10,15
PAL=list(PAL7); PAL[10]=(228,204,166)          # crème-midden: lum 207 tussen k 234 en h 182
log=collections.defaultdict(list)
def zet(n,pts,van,naar):
    for x,y in pts:
        assert r7[y,x] in (van if isinstance(van,tuple) else (van,)),(n,x,y,r7[y,x])
        o[y,x]=naar; log[n].append((x,y))
# ---- 1a. paletplek vrij: oude 140/120/100 (idx 10) -> dichtstbijzijnde tint idx 15 (176/138/96)
oud10=[(int(x),int(y)) for y,x in np.argwhere(r7==10)]
zet('1a palet',oud10,10,D)
# ---- 1b/2. crème-middentint als sikkel: rechterhelft borststuk (om het zakje) en midden buik
SIK={35:[36,37],36:[35,36],37:[35,36],38:[34,35,36],39:range(34,38),40:range(34,40),41:range(34,39),42:range(34,38),43:range(34,37),
     44:range(33,36),45:range(29,36),46:range(27,35),47:range(27,34),48:range(26,33),49:range(25,31),50:range(24,29),51:range(24,27)}
for y,xs in SIK.items(): zet('1 middentint',[(x,y) for x in xs],(C,S),M)
zet('2 zakje onderzoom',[(24,44)],C,S)
# ---- 3. rechterrand crème: buigt naar het kruis (randkolom 42,40,38,37,37,36,36,36,35,34), donkere sikkel dikker naar onder
zet('3 rand',[(39,46)],D,S)
zet('3 rand',[(39,47),(38,48),(38,49)],D,D4)                          # dij (bruin-midden zoals de buren)
zet('3 rand',[(37,47),(36,48),(37,48),(35,49),(34,50),(35,50),(34,51),(33,52),(33,53),(33,54)],S,D)
zet('3 rand',[(36,52),(35,53)],C3,D)
# ---- 4. bovenrand borststuk tussen de bandjes: boog (rand r34,35,35,36,35,35,34 i.p.v. recht r35)
zet('4 boog',[(26,34)],C3,C); zet('4 boog',[(32,34)],D4,C); zet('4 boog',[(29,35)],C,C3)
# ---- 5. borst: stamkleur weg, één plooi zoals model r10_k8_64 (verticaal x30 + band r30; rechts schouderplooi r27-30)
zet('5 borst',[(29,26),(35,29),(36,29)],E,B)
zet('5 borst',[(31,31)],E,C3)
zet('5 borst',[(37,29),(35,30)],C3,B)
zet('5 borst',[(34,27),(36,27),(31,27),(29,28),(31,29)],C3,D4)
# ---- 6. linkerbovenarm: binnenlijn alleen bruin-lijn, stamkleur alleen hand/stam
zet('6 arm',[(16,28),(16,29),(20,28),(10,27),(19,34)],E,B)
zet('6 arm',[(11,34)],E,C3)
zet('6 arm',[(11,27)],D4,B)
zet('6 arm',[(21,27)],C3,D4)
# ---- opslaan
def save(idx,pad,z=None):
    im=Image.new('P',(64,64)); im.putpalette([v for p in PAL for v in p]+[0]*3*(256-len(PAL)))
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad,transparency=0)
    if z: Image.fromarray(np.array(PAL,'uint8')[idx]).resize((64*z,64*z),Image.NEAREST).save(pad.replace('.png',f'_{z}x.png'))
save(o,'sprite_r8/sprite.png',8)
# ---- bewijs: diff buiten de zones = 0
ZONES={'1':(24,39,35,51),'3':(33,42,45,54),'4':(26,32,34,35),'5':(26,38,26,33),'6':(10,21,26,34)}
inz=lambda x,y:(x,y) in oud10 or any(a<=x<=b and c<=y<=d for a,b,c,d in ZONES.values())
dd=[(int(x),int(y)) for y,x in np.argwhere(o!=r7)]
print('gewijzigd:',len(dd),'| buiten zones:',[p for p in dd if not inz(*p)],'| silhouet gelijk:',((o>0)==(r7>0)).all())
for k,v in log.items(): print(k,len(v),v if len(v)<20 else '')
print('kleuren:',len(np.unique(o)),'| idx10 oud-pixels:',oud10)
# ---- vel: r8 | r7 | Gemini r5 | model (8x); tuinbroek en borst 12x; 1x licht/donker
from PIL import ImageDraw
fig=np.load('sprite_r1/masker.npy'); yy,xx=np.where(fig)
MK=np.asarray(Image.open('model/r10_k8.png').convert('RGB')); mx0,my0=xx.min(),yy.min(); s_=64/(xx.max()-mx0+1); oy=64-round((yy.max()-my0+1)*s_)
def modelvak(x0,y0,x1,y1,Z):
    W,H=(x1-x0)*Z,(y1-y0)*Z; out=np.full((H,W,3),255,'uint8')
    py,px=np.mgrid[0:H,0:W]; X=(mx0+(x0+px/Z)/s_).astype(int); Y=(my0+(y0+py/Z-oy)/s_).astype(int)
    ok=(X>=0)&(X<99)&(Y>=0)&(Y<99); out[ok]=MK[Y[ok],X[ok]]; return Image.fromarray(out)
def spr(idx,pal,z,box=None):
    im=Image.fromarray(np.array(pal,'uint8')[idx])
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),Image.NEAREST)
G5=Image.open('gemini/r5.png').convert('RGB')
V=Image.new('RGB',(2110,1560),'white'); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(spr(o,PAL,8),'r8'),(spr(r7,PAL7,8),'r7'),(G5.crop((60,100,960,1000)).resize((512,512),Image.LANCZOS),'Gemini r5 (vorm)'),(modelvak(0,0,64,64,8),'model r10_k8')]):
    V.paste(im,(10+i*522,30)); d.text((10+i*522,10),t+' 8x',fill='black')
y=570; bb=(14,24,46,58)
for i,(im,t) in enumerate([(spr(o,PAL,12,bb),'tuinbroek+borst r8 12x'),(spr(r7,PAL7,12,bb),'r7 12x'),(G5.crop((290,330,730,820)).resize((384,408),Image.LANCZOS),'Gemini r5 uitsnede'),(modelvak(*bb,12),'model r10 12x')]):
    V.paste(im,(10+i*398 if i<2 else 20+i*398,y+20)); d.text((10+i*398 if i<2 else 20+i*398,y),t,fill='black')
y+=440; bb=(8,24,40,36)
for i,(im,t) in enumerate([(spr(o,PAL,12,bb),'arm+borst r8 12x'),(spr(r7,PAL7,12,bb),'r7 12x'),(modelvak(*bb,12),'model r10 12x')]):
    V.paste(im,(10+i*400,y+20)); d.text((10+i*400,y),t,fill='black')
y+=190
for j,bg in enumerate([(248,248,248),(40,40,48)]):
    for i,(idx,pal) in enumerate([(o,PAL),(r7,PAL7)]):
        im=Image.new('RGB',(64,64),bg); im.paste(Image.fromarray(np.array(pal,'uint8')[idx]),(0,0),Image.fromarray(((idx>0)*255).astype('uint8')))
        V.paste(im,(10+i*80,y+20+j*80))
d.text((10,y),'1x licht/donker: r8, r7',fill='black')
V.crop((0,0,2110,y+190)).save('sprite_r8/vel.png')
