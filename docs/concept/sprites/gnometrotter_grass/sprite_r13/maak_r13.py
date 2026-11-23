# maak_r13.py: Gnometrotter Grass r13 = r12, alleen de muts: bladeren zoals Game Freak-bladeren (studie_blad.png):
# elk blad een middennerf met twee verschillend belichte helften (lichte helft naar linksboven, schaduwhelft), punt taps.
# Bladvormen (A links, B midden, C rechterkrul, D onder) en nerven/omlijning = r12/r9 (geen nieuwe omtrek). Palet = r11/r12.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
os.chdir('../sprite_r12'); sys.path.insert(0,'.'); sys.path.insert(0,'../sprite_r10'); import maak_r12 as r12; os.chdir(HIER)
bim=Image.open('../sprite_r12/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
A,Bm,C,D,muts,B9=r12.A,r12.Bm,r12.C,r12.D,r12.muts,r12.B9
def rand_linksboven(y,x): return B9[y,x-1] in (5,0) or B9[y-1,x] in (5,0)
# A linkerblad (punt boven bij x 33, voet linksonder): middennerf diagonaal (32,2)->(19,12), donker (5) zoals Chikorita/Tropius;
#   helft linksboven licht 13 met een rand 14 langs de omlijning (rij 4-9), helft rechtsonder schaduw 12. Nerf taps: niet in de punt.
nerfA=lambda y: int(np.floor(32-(y-2)*1.3+0.5))
for y,x in zip(*np.nonzero(A)):
    n=nerfA(y)
    if 3<=y<=11 and x==n: O[y,x]=5
    elif x<n: O[y,x]=14 if (rand_linksboven(y,x) and 4<=y<=9) else 13
    else: O[y,x]=12
# B middenblad (punt boven): klein, zoals de kleine Shiftry-bladeren geen eigen nerflijn; lichte helft links 13, schaduwhelft rechts 12
for y,x in zip(*np.nonzero(Bm)):
    O[y,x]=13 if x < 34+(y-8)*0.45 else 12
# C rechterblad (krul, punt rechtsonder): middennerf (35,2)->(42,12) licht (13) zoals Shiftry; buitenhelft (rechtsboven) 12,
#   binnenhelft (linksonder, van het licht af) 5.
nerfC=lambda y: int(np.floor(35+(y-2)*0.7+0.5))
for y,x in zip(*np.nonzero(C)):
    n=nerfC(y)
    if 2<=y<=11 and x==n: O[y,x]=13
    elif x>n or y<=1: O[y,x]=12
    else: O[y,x]=5
# D onderste blad (liggend): lichte bovenhelft 13, schaduwhelft onder 12 (scheiding = nerf, rij 14|15)
for y,x in zip(*np.nonzero(D)):
    O[y,x]=13 if y<=14 else 12
# opschonen: losse pixels (4-samenhang, 1 px) die geen nerf- of randpixel zijn -> meest voorkomende 4-buur in hetzelfde blad;
# de bladpunt bovenaan (32-34,1) wordt één vlak (12)
NERF=np.zeros((64,64),bool)
for y,x in zip(*np.nonzero(A)):
    if 3<=y<=11 and x==nerfA(y): NERF[y,x]=True
    if O[y,x]==14: NERF[y,x]=True
for y,x in zip(*np.nonzero(C)):
    if 2<=y<=11 and x==nerfC(y): NERF[y,x]=True
for x in (32,33,34): O[1,x]=12
for blad in (A,Bm,C,D):
    for k in (5,12,13,14):
        Lc,nc=ndimage.label((O==k)&blad)
        for i in range(1,nc+1):
            ys,xs=np.nonzero(Lc==i)
            if len(ys)>1 or NERF[ys[0],xs[0]]: continue
            y,x=ys[0],xs[0]
            nb=[O[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if blad[y+dy,x+dx] and not NERF[y+dy,x+dx]]
            if nb: O[y,x]=max(set(nb),key=nb.count)
if __name__=='__main__':
    ver=O!=B
    assert not (ver&~muts).any()
    print('t.o.v. r12: muts',int(ver.sum()),'rest 0')
    with open('log_r13.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('muts x=%d y=%d %d->%d\n'%(x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    H='0123456789abcdef'
    rows=['%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(14,48)) for y in range(0,18)]
    open('muts_raster.txt','w').write('\n'.join(rows)+'\n')
    # vel: studie-uitsneden | model | r12 | r13 (muts, 12x)
    root='../../../../../graphics/pokemon/'
    st=[]
    for s,b in (('chikorita',(30,8,64,32)),('tropius',(30,4,64,40)),('shiftry',(0,4,30,24)),('swadloon',(10,8,50,40))):
        im=Image.open(root+s+'/anim_front.png').convert('RGB').crop(b); st.append(im.resize((im.width*6,im.height*6),Image.NEAREST))
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    z=12; x0,y0,x1,y1=12,0,48,18
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',64*z).crop((x0*z,y0*z,x1*z,y1*z)); os.chdir(HIER)
    ps=[m]+[sprite(p).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST) for p in ('../sprite_r12/gnometrotter_grass.png','gnometrotter_grass.png')]
    w=(x1-x0)*z; hgt=(y1-y0)*z
    sw=sum(i.width+10 for i in st); W=Image.new('RGB',(max(sw,3*(w+10)),max(i.height for i in st)+10+hgt),'white')
    x=0
    for im in st: W.paste(im,(x,0)); x+=im.width+10
    top=max(i.height for i in st)+10
    for k,p in enumerate(ps): W.paste(p,(k*(w+10),top))
    W.save('vel.png')
