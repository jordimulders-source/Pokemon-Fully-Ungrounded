# maak_r14.py: Gnometrotter Grass r14 = r13, alleen de muts buiten het grote linkerblad (A, bevroren).
# Indeling naar het model (12x): 1 groot linkerblad (A, bevroren), 2 middenblad (punt boven bij x 34, tussen modellijnen
# L1 en L2, ligt vóór 3), 3 krulblad rechts (punt rechtsonder bij x 43, in de schaduw, achter 2), 4 onderste blad
# (onder 1 en 2, boven de neus). Elk blad als A: eigen omtrek 5 waar het vóór een buurblad ligt, twee helften (licht|schaduw)
# met de nerf als grens, taps toelopende punt. Palet = r13.
import os, sys, numpy as np
from PIL import Image, ImageDraw
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
os.chdir('../sprite_r13'); sys.path.insert(0,'.'); sys.path.insert(0,'../sprite_r12'); sys.path.insert(0,'../sprite_r10')
import maak_r13 as r13; os.chdir(HIER)
bim=Image.open('../sprite_r13/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
A,muts,B9=r13.A,r13.muts,r13.B9
# bladvlakken opnieuw indelen tussen de vaste rand (buitenomlijning naast achtergrond/zwart) en het bevroren blad A:
# de dikke nerfklodders van r9 in het midden (rij 3-9) worden weer blad 2 met dunne lijnen L1 (rechtsrand A) en L2 (model).
yy,xx=np.mgrid[0:64,0:64]
def buitenrand(y,x): return any(B[y+dy,x+dx] in (0,1) or not muts[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
binnen=muts&~A
L1={}
for y in range(1,14):
    xs=np.nonzero(A[y])[0]
    if len(xs): L1[y]=xs.max()+1
L2={3:35,4:35,5:35,6:36,7:36,8:37,9:37}     # modellijn tussen blad 2 en 3: (34,3)->(37,9)
M=np.zeros((64,64),int)                     # 0 = blijft (lijn/rand), 2/3/4 = blad
for y,x in zip(*np.nonzero(binnen)):
    if r13.D[y,x]: M[y,x]=4; continue
    if buitenrand(y,x) and B[y,x]==5: continue
    if y in L1 and x==L1[y] and B9[y,x]==5: continue          # L1 blijft
    if y in L2 and x==L2[y]: M[y,x]=-1; continue              # L2 wordt lijn
    if y<=2: M[y,x]=3 if x>=34 else 0; continue
    if y in L2: M[y,x]=2 if x<L2[y] else 3
    elif r13.Bm[y,x] or (y>=10 and x<=37 and B9[y,x]!=5): M[y,x]=2
    elif r13.C[y,x] or B9[y,x]==5: M[y,x]=3 if x>=37 else 0
for y,x in zip(*np.nonzero(M==-1)): O[y,x]=5
# blad 2: punt boven (taps, rij 3-6 één pixel), middennerf 5 op x 34 (rij 8-12), helft links 13, rechts 12
for y,x in zip(*np.nonzero(M==2)):
    if 8<=y<=12 and x==34: O[y,x]=5
    else: O[y,x]=13 if x<34 or y<=7 else 12
# blad 3 (krul, schaduw): buitenhelft (boven/rechts) 12, binnenhelft 5, nerf = grens (36,2)->(42,12); punt/toprand 13
for y,x in zip(*np.nonzero(M==3)):
    n=36+(y-2)*0.6
    if y<=2: O[y,x]=13                       # punt/toprand in het licht
    elif x>n: O[y,x]=13 if y<=4 else 12      # buitenhelft: boven licht, verder 12
    else: O[y,x]=12 if y<=6 else 5           # binnenhelft: schaduw, het donkerst onderaan bij de krul
for y,x in zip(*np.nonzero(M==4)): O[y,x]=13 if y<=14 else 12
if __name__=='__main__':
    ver=O!=B
    assert not (ver&(A|~muts)).any(), 'A of buiten de muts veranderd'
    print('t.o.v. r13: muts (blad 2-4)',int(ver.sum()),'A 0, rest 0')
    with open('log_r14.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('blad %d x=%d y=%d %d->%d\n'%(M[y,x],x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    H='0123456789abcdef'
    open('muts_raster.txt','w').write('\n'.join('%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(14,48)) for y in range(18))+'\n')
    # masker: genummerde bladindeling op 12x
    z=12; x0,y0,x1,y1=12,0,48,18
    Mk=M.copy(); Mk[A]=1
    kl={1:(120,200,120),2:(240,200,90),3:(110,150,230),4:(230,120,160)}
    im=Image.new('RGB',((x1-x0)*z,(y1-y0)*z),'white'); d=ImageDraw.Draw(im)
    for y in range(y0,y1):
        for x in range(x0,x1):
            c=kl.get(Mk[y,x]) if Mk[y,x]>0 else ((40,40,40) if muts[y,x] or (B9[y,x]==5 and y<17) else None)
            if c: d.rectangle([(x-x0)*z,(y-y0)*z,(x-x0+1)*z-1,(y-y0+1)*z-1],fill=c)
    for k,(cx,cy) in {1:(24,8),2:(34,10),3:(40,5),4:(27,15)}.items():
        d.text(((cx-x0)*z,(cy-y0)*z),str(k),fill=(0,0,0))
    big=im.resize((im.width*2,im.height*2),Image.NEAREST); big.save('masker_r14.png')
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',64*z).crop((x0*z,y0*z,x1*z,y1*z)); os.chdir(HIER)
    ps=[m]+[sprite(p).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST) for p in
        ('../sprite_r12/gnometrotter_grass.png','../sprite_r13/gnometrotter_grass.png','gnometrotter_grass.png')]
    w=(x1-x0)*z; hh=(y1-y0)*z; W=Image.new('RGB',(2*(w+10),2*(hh+10)),'white')
    for k,p in enumerate(ps): W.paste(p,((k%2)*(w+10),(k//2)*(hh+10)))
    W.save('vel.png')
