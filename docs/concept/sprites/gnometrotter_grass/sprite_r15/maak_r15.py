# maak_r15.py: Gnometrotter Grass r15 = r14, alleen de muts buiten het grote linkerblad (A, bevroren), opnieuw vanuit het model.
# Bladindeling gemeten op het model (model_op_schaal, donkere modellijnen lum<60 per spritepixel; zie RAPPORT.md):
#   1 groot linkerblad A (bevroren, met zijn randlijn L1)
#   2 rechterblad: van de top naar rechtsonder, eindigt in de haakpunt boven het gat; voorrand = modellijn D
#     (34,5)(35,6)(35,7)(36,8)(37,9); middennerf = modelcurve (38,4)(39,5)(40,6)(40,7)(41,8)(41,9), taps (niet in voet en haak).
#     het donkerste blad (model): helft linksboven 12, helft rechtsonder 5 (nerf = grens), kruin rij 1-3 13, haak 12.
#   3 middenblad (wig tussen 1 en 2, punt boven bij (34,6), ligt achter 1 en 2): lichte helft links 13, schaduwhelft rechts 12.
#   4 onderblad boven de neus (onder 1, links van modellijn LL (30,12)(31,13)(32,14)): voet bij de kruising (30,12),
#     nerf naar linksonder; helft linksboven 13, helft rechtsonder 12.
# Silhouet, omlijning (5 naast buiten/zwart) en L1 (5 naast A) blijven; alles buiten de muts 0 px.
import os, sys, numpy as np
from PIL import Image, ImageDraw
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
os.chdir('../sprite_r13'); sys.path[:0]=['.','../sprite_r12','../sprite_r10']
import maak_r13 as r13; os.chdir(HIER)
bim=Image.open('../sprite_r14/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
A,muts=r13.A,r13.muts
N4=((1,0),(-1,0),(0,1),(0,-1))
def buiten(y,x): return B[y,x] in (0,1) or not muts[y,x]
rand=np.zeros((64,64),bool); L1=np.zeros((64,64),bool)
for y,x in zip(*np.nonzero(muts&~A)):
    if B[y,x]==5 and any(buiten(y+dy,x+dx) for dx,dy in N4): rand[y,x]=True
    elif B[y,x]==5 and any(A[y+dy,x+dx] for dx,dy in N4): L1[y,x]=True
VAST=A|rand|L1|~muts
E=muts&~VAST                      # bewerkbaar
BL=np.zeros((64,64),int)          # bladnummer per pixel (0 = lijn)
D=[(34,5),(35,6),(35,7),(36,8),(37,9)]
LL=[(30,12),(31,13),(32,14)]
NERF2=[(38,4),(39,5),(40,6),(40,7),(41,8),(41,9)]
dx={y:x for x,y in D}; nx={y:x for x,y in NERF2}
for y,x in zip(*np.nonzero(E)):
    if (x,y) in D or (x,y) in LL: O[y,x]=5; continue   # bladgrens: 2 ligt voor 3, 3 voor 4
    # indeling
    if y<=4 or (y in dx and x>dx[y]) or (y>=9 and x>=38): b=2
    elif y>=12 and x <= {12:29,13:30,14:31,15:31,16:31}[y]: b=4
    else: b=3
    BL[y,x]=b
    if b==2:                                        # donker blad zoals het model: licht 12 | schaduw 5, nerf = grens
        if y<=3: O[y,x]=13                          # voet/kruin bovenop, in het licht
        elif (x,y)==(42,13): O[y,x]=5               # haakpunt: 1 px tussen omlijning, blijft donker (= r14)
        elif y>=10: O[y,x]=12                       # haak (voorbij het eind van de nerf), onderkant licht
        elif x>=nx[y]: O[y,x]=5                     # schaduwhelft rechtsonder (buitenrand)
        else: O[y,x]=12                             # lichte helft linksboven
    elif b==3:
        O[y,x]=13 if (x<=34 or y<=7) else 12
    else:
        O[y,x]=13 if x < 30.5-1.25*(y-12) else 12
for x,y in D+LL: BL[y,x]=0
if __name__=='__main__':
    ver=O!=B
    assert not (ver&VAST).any(), 'bevroren pixel veranderd'
    assert not (ver&(A|~muts)).any()
    n=int(ver.sum()); print('t.o.v. r14: blad 2-4',n,'| groot blad 0 | rest 0')
    for b in (2,3,4): print(' blad',b,int((ver&(BL==b)).sum()))
    print(' lijnen D/LL',int((ver&E&(BL==0)).sum()))
    with open('log_r15.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('blad %d x=%d y=%d %d->%d\n'%(BL[y,x],x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    H='0123456789abcdef'
    open('muts_raster.txt','w').write('\n'.join('%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(14,48)) for y in range(18))+'\n')
    z=12; x0,y0,x1,y1=12,0,48,18
    # masker: genummerde bladindeling
    Mk=BL.copy(); Mk[A]=1
    kl={1:(120,200,120),2:(110,150,230),3:(240,200,90),4:(230,120,160)}
    im=Image.new('RGB',((x1-x0)*z,(y1-y0)*z),'white'); d=ImageDraw.Draw(im)
    for y in range(y0,y1):
        for x in range(x0,x1):
            c=kl.get(Mk[y,x]) if Mk[y,x]>0 else ((40,40,40) if muts[y,x] else None)
            if c: d.rectangle([(x-x0)*z,(y-y0)*z,(x-x0+1)*z-1,(y-y0+1)*z-1],fill=c)
    for k,(cx,cy) in {1:(24,8),2:(37,6),3:(33,11),4:(26,15)}.items(): d.text(((cx-x0)*z+3,(cy-y0)*z),str(k),fill=(0,0,0))
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',64*z).crop((x0*z,y0*z,x1*z,y1*z))
    mh=Image.open('../../gnometrotter_grass/hybride/model_hybride.png').convert('RGB')
    from reductie_gedeeld import P
    mhc=mh.crop((int(512+(x0-32)*P),int(523-(60-y0)*P),int(512+(x1-32)*P),int(523-(60-y1)*P))).resize(m.size,Image.LANCZOS)
    m64=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',64).crop((x0,y0,x1,y1)).resize(m.size,Image.NEAREST)
    os.chdir(HIER)
    mm=Image.new('RGB',(2*im.width+10,im.height),'white'); mm.paste(im,(0,0)); mm.paste(mhc,(im.width+10,0)); mm.save('masker_r15.png')
    ps=[mhc,m64]+[sprite(p).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST) for p in ('../sprite_r14/gnometrotter_grass.png','gnometrotter_grass.png')]
    w=(x1-x0)*z; hh=(y1-y0)*z; W=Image.new('RGB',(2*(w+10),2*(hh+10)),'white')
    for k,p in enumerate(ps): W.paste(p,((k%2)*(w+10),(k//2)*(hh+10)))
    W.save('vel.png')
