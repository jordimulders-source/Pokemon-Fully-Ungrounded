# maak_r12.py: Gnometrotter Grass r12 = r11, alleen de muts: weer losse bladeren (Jordi: "de muts heeft nu geen bladeren meer").
# Bladvlakken = de vlakken tussen de nerven van r9, en die nerven vallen samen met de donkere modellijnen (lum < 62):
#   A linkerblad (licht), B middenblad, C rechterblad (krul, donker), D onderste blad; A en C raken elkaar aan de top,
#   gescheiden op x 34 waar de modelnerf de top in loopt.
# Per blad: lichte kant linksboven, midden, schaduwkant rechtsonder; tinten 5/12/13, 14 alleen als klein hooglicht. Palet = r11.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
os.chdir('../sprite_r10'); sys.path.insert(0,'.'); import maak_r10 as r10; os.chdir(HIER)
bim=Image.open('../sprite_r11/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy(); B9=r10.B
muts=r10.ZONES['muts']
Lf,nf=ndimage.label(muts&np.isin(B9,[12,13,14]))
grootte=[(Lf==i).sum() for i in range(1,nf+1)]
volg=np.argsort(grootte)[::-1]+1           # grootste eerst: A+C, B, D, (rest)
AC,Bv,Dv=volg[0],volg[1],volg[2]
yy,xx=np.mgrid[0:64,0:64]
A=(Lf==AC)&(xx<34); C=(Lf==AC)&(xx>=34); Bm=Lf==Bv; D=Lf==Dv
rest=(Lf>0)&~A&~C&~Bm&~D
nerf=lambda y,x: B9[y,x]==5                 # nerf of mutsrand (donkerste eigen tint)
def lichtrand(y,x):   # pixel grenst links of boven aan een nerf/rand
    return nerf(y,x-1) or nerf(y-1,x)
def schaduwrand(y,x): # pixel grenst rechts of onder aan een nerf/rand of de zwarte buitenlijn
    return B9[y,x+1] in (5,1) or B9[y+1,x] in (5,1)
for y,x in zip(*np.nonzero(A)):              # linkerblad: bogen rond een klein hooglicht linksboven
    r=np.hypot(x-23.0,(y-4.5)*1.1)
    O[y,x]=14 if r<2.3 else (13 if r<7.8 else 12)
for y,x in zip(*np.nonzero(Bm)):             # middenblad: lichte rand langs de nerf linksboven, lijf 12, schaduw rechtsonder 5
    O[y,x]=13 if lichtrand(y,x) and y<=11 else (5 if schaduwrand(y,x) and y>=9 else 12)
for y,x in zip(*np.nonzero(C)):              # rechterblad: donker lijf 5, lichte rand langs de nerf/top (12), toprand 13
    if y<=2: O[y,x]=13
    elif lichtrand(y,x) or y<=4: O[y,x]=12
    else: O[y,x]=5
for y,x in zip(*np.nonzero(D)):              # onderste blad: lichte rand boven/links 13, lijf 12, schaduwkant 5
    O[y,x]=13 if lichtrand(y,x) else (5 if schaduwrand(y,x) else 12)
# vlakjes van 1 px (32,15) blijven zoals r11 (opgenomen in de nerf)
# opschonen: losse vlakjes van 1 px binnen een blad -> meest voorkomende 4-buur in hetzelfde blad
for blad in (A,Bm,C,D):
    for k in (5,12,13,14):
        Lc,nc=ndimage.label((O==k)&blad)
        for i in range(1,nc+1):
            ys,xs=np.nonzero(Lc==i)
            if len(ys)>1: continue
            y,x=ys[0],xs[0]
            nb=[O[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if blad[y+dy,x+dx]]
            if nb: O[y,x]=max(set(nb),key=nb.count)
if __name__=='__main__':
    ver=O!=B
    assert not (ver&~muts).any()
    print('t.o.v. r11: muts',int(ver.sum()),'rest 0')
    with open('log_r12.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('muts x=%d y=%d %d->%d\n'%(x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    H='0123456789abcdef'
    for y in range(0,18): print('%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(14,48)))
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    z=12; x0,y0,x1,y1=12,0,48,18
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',64*z).crop((x0*z,y0*z,x1*z,y1*z)); os.chdir(HIER)
    ps=[m]+[sprite(p).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST) for p in
        ('../sprite_r10/gnometrotter_grass.png','../sprite_r11/gnometrotter_grass.png','gnometrotter_grass.png')]
    w=(x1-x0)*z; W=Image.new('RGB',(2*(w+10),2*((y1-y0)*z+10)),'white')
    for k,p in enumerate(ps): W.paste(p,((k%2)*(w+10),(k//2)*((y1-y0)*z+10)))
    W.save('vel.png')
