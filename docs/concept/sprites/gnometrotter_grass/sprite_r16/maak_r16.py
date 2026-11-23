# maak_r16.py: Gnometrotter Grass r16 = r15, alleen de zone binnen Jordi's rode cirkel (krabbels/r15_onderblad.png):
# het onderblad boven de neus als één blad zoals in het model.
# Zone: screenshot = r15 op 13,0x, oorsprong (-103, 0) (gefit op de sprite, 0,6 % afwijkende monsterpunten);
# spritepixel in de zone als >= 50 % van zijn vlak binnen de cirkel ligt.
# Model (hybride, x 23-33, y 12-19): blad onder het grote blad (randlijn L1, bevroren), links/onder tegen de neus,
# rechterrand = modellijn (31,13)(32,14)(32,15)(31,16)(31,17) (bestaande 5), onderrand tegen de neus/baard rij 18.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
bim=Image.open('../sprite_r15/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
# --- zone uit de krabbel
k=np.asarray(Image.open('../krabbels/r15_onderblad.png').convert('RGB')).astype(int)
s,ox,oy=13.0,-103,0
red=(k[...,0]>180)&(k[...,1]<90)&(k[...,2]<90)
fill=ndimage.binary_fill_holes(ndimage.binary_closing(red,iterations=6))
Z=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        y0,y1,x0,x1=int(oy+Y*s),int(oy+(Y+1)*s),int(ox+X*s),int(ox+(X+1)*s)
        if y0<0 or x0<0 or y1>k.shape[0] or x1>k.shape[1]: continue
        Z[Y,X]=fill[y0:y1,x0:x1].mean()>=0.5
# --- nieuw blad (alleen pixels in Z worden geschreven)
# Model: voet rechtsboven bij de kruising (30,12)-(31,12), middennerf schuin naar linksonder (modellijn (30,13)->(26,17)),
# punt linksonder tegen de neus. Nerf = grens x+y=43: helft linksboven (naar het licht, onder het grote blad) 13, rest 12.
NIEUW={}
for p in [(30,18)]: NIEUW[p]=5                 # onderrand: 1 px 5 doorgetrokken (lag als lichte baardpixel in het blad)
BLAD={13:range(28,30),14:range(26,32),15:range(24,32),16:range(25,31),17:range(26,31)}
for y,xs in BLAD.items():
    for x in xs: NIEUW[(x,y)]=13 if x+y<=43 else 12
for (x,y),v in NIEUW.items():
    if Z[y,x]: O[y,x]=v
if __name__=='__main__':
    ver=O!=B
    assert not (ver&~Z).any()
    print('zone',int(Z.sum()),'px:',sorted((int(x),int(y)) for y,x in zip(*np.nonzero(Z))))
    print('t.o.v. r15: zone',int(ver.sum()),'| buiten de zone 0')
    with open('log_r16.txt','w') as f:
        f.write('zone (%d px): %s\n'%(Z.sum(),' '.join('(%d,%d)'%(x,y) for y,x in zip(*np.nonzero(Z)))))
        for y,x in zip(*np.nonzero(ver)): f.write('x=%d y=%d %d->%d\n'%(x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    np.save('zone.npy',Z)
    # vel: krabbel-uitsnede | model | r15 | r16 (16x)
    z=16; X0,Y0,X1,Y1=20,9,38,21
    kr=Image.open('../krabbels/r15_onderblad.png').convert('RGB').crop((int(ox+X0*s),int(oy+Y0*s),int(ox+X1*s),int(oy+Y1*s))).resize(((X1-X0)*z,(Y1-Y0)*z),Image.LANCZOS)
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite
    from reductie_gedeeld import P
    mh=Image.open('../../gnometrotter_grass/hybride/model_hybride.png').convert('RGB')
    m=mh.crop((int(512+(X0-32)*P),int(523-(60-Y0)*P),int(512+(X1-32)*P),int(523-(60-Y1)*P))).resize(((X1-X0)*z,(Y1-Y0)*z),Image.LANCZOS)
    os.chdir(HIER)
    ps=[kr,m]+[sprite(p).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST) for p in ('../sprite_r15/gnometrotter_grass.png','gnometrotter_grass.png')]
    w=(X1-X0)*z; W=Image.new('RGB',(4*(w+8),(Y1-Y0)*z),'white')
    for i,p in enumerate(ps): W.paste(p,(i*(w+8),0))
    W.save('vel.png')
