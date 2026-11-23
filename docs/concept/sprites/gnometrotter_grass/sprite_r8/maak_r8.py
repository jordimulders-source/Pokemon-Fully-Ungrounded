# maak_r8.py: Gnometrotter Grass r8 = r7, alleen de blauwe benen (keuring_r6 R3-R5).
# R3 rechterheup = Rock af (pixellijst keuring + alle blauw/lijn in x43-50, y36-42, riem uitgezonderd).
# R4 dijen: Gen 3-volume per bol (11 linksboven, 10, 9-sikkel rechts/onder, hoeveelheid naar Rock af) + per dij één
#    diagonale plankvorm uit het model (naad 9, schaduwkant 10), vloeiende lijn die meebuigt met de bol.
# R5 laarzen: 9-sikkel rechts/onder. Rest 0 px (assert). Log: log_r8.txt.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
bim=Image.open('../sprite_r7/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
R=np.asarray(Image.open('../../gnometrotter_rock/af/gnometrotter_rock.png')).astype(int)
BLAUW=[9,10,11]
been=np.zeros((64,64),bool)          # binnenpixels van de benen (buitenrand naast achtergrond blijft)
for y in range(36,60):
    for x in range(1,63):
        if B[y,x] in BLAUW and not any(B[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): been[y,x]=True
heup=np.zeros((64,64),bool); heup[36:43,43:51]=True

# ---- delen en volume ----
GRENS_L={20:49,21:49,22:48,23:48,24:48,25:48,26:49,27:49}   # bovenrand voetbol L (r6)
GRENS_R={41:50,42:50,43:49,44:49,45:49,46:50,47:50}         # bovenrand voetbol R (r6)
def deel(x,y):
    if x<=30 and (y>=50 or (x in GRENS_L and y>GRENS_L[x])): return 'LF'
    if x>=38 and (y>=51 or (x in GRENS_R and y>GRENS_R[x])): return 'RF'
    if 42<=y<=48 and x<=30+max(0,(y-43))*0.5: return 'LT'
    if x<=plank_RT(y): return 'KR'       # binnenkant rechterdij (kruisstuk), model: donkerder vlak
    return 'RT'
# plankvormen uit het model (op 20x bekeken): linkerdij diagonale naad van ±(21,44) naar ±(28,47);
# rechterdij: grens kruisstuk | dij van ±(36,42) naar ±(38,48). Vloeiend, 2-px-treden.
def plank_LT(x): return {20:44,21:44,22:44,23:45,24:45,25:46,26:46,27:47,28:47}.get(x)
def plank_RT(y): return {42:35,43:36,44:36,45:37,46:37,47:38,48:38}.get(y,-1)
DELEN={'LT':((24,44.0),6.0,3.5),'RT':((42.0,43.5),8.0,5.5),'KR':((33,44.5),4.0,3.0),'LF':((21.0,51.0),6.0,2.6),'RF':((44.0,52.5),5.0,3.0)}
def vol(x,y):
    p=deel(x,y); (cx,cy),rx,ry=DELEN[p]
    d=0.7*(x-cx)/rx+0.6*(y-cy)/ry
    if p=='KR': return 10 if d<0.9 else 9          # kruisstuk ligt in de schaduw: geen 11
    return 11 if d<0.0 else (10 if d<0.45 else 9)
def tint(x,y):
    if (x in GRENS_L and y==GRENS_L[x]) or (x in GRENS_R and y==GRENS_R[x]): return 9
    p=deel(x,y)
    if p=='LT':
        g=plank_LT(x)
        if g is not None:
            if y==g: return 9                       # naad
            if y>g: return 10 if vol(x,y)==11 else vol(x,y)   # schaduwkant van de plank
    return vol(x,y)
for y,x in zip(*np.nonzero(been)):
    if heup[y,x]: continue
    O[y,x]=tint(x,y)
# ---- R3 heup = Rock af ----
for y in range(36,43):
    for x in range(43,51):
        if B[y,x] in BLAUW+[1] and R[y,x] in BLAUW: O[y,x]=R[y,x]   # zwart van Rock hier = Rock-riemrand: niet
for x,y,v in [(48,37,9),(48,38,9),(49,38,9),(47,39,9),(48,39,9),(46,40,9),(47,40,9),(48,40,9),(48,41,9),
              (45,40,10),(43,41,10),(44,41,10),(45,41,10),(46,41,10),(47,41,10),(48,36,1),(49,36,1)]: O[y,x]=v
zone=been|(heup&np.isin(B,BLAUW+[1])); zone[36,48]=zone[36,49]=True   # keuringslijst R3 (48,36) was riem 3 -> 1 zoals Rock af
# ---- opschonen: vlakjes < 3 px in de zone -> meest voorkomende zonebuur ----
def lijnpixel(x,y): return (x in GRENS_L and y==GRENS_L[x]) or (x in GRENS_R and y==GRENS_R[x]) or plank_LT(x)==y 
for _ in range(2):
    for k in BLAUW:
        Lc,nc=ndimage.label((O==k)&zone)
        for i in range(1,nc+1):
            ys,xs=np.nonzero(Lc==i)
            if len(ys)>=3 or any(lijnpixel(x,y) for x,y in zip(xs,ys)) or any(heup[y,x] for x,y in zip(xs,ys)): continue
            if ((O==k)&~zone&ndimage.binary_dilation(Lc==i,np.ones((3,3)))).any(): continue
            nb=[O[y+dy,x+dx] for x,y in zip(xs,ys) for dx in (-1,0,1) for dy in (-1,0,1) if zone[y+dy,x+dx] and O[y+dy,x+dx]!=k]
            if nb:
                v=max(set(nb),key=nb.count)
                for x,y in zip(xs,ys): O[y,x]=v

if __name__=='__main__':
    ver=O!=B
    print("buiten zone:",[(int(x),int(y),int(B[y,x]),int(O[y,x])) for y,x in zip(*np.nonzero(ver&~zone))]); assert not (ver&~zone).any()
    z=lambda m:int((ver&m).sum())
    print('t.o.v. r7: heup',z(heup),'benen',z(~heup),'rest 0')
    sub=O[42:49,17:51]; L11,n=ndimage.label(sub==11)
    print('dijen x17-50 y42-48: 9 =',int((sub==9).sum()),' grootste 11-vlak =',max([(L11==i).sum() for i in range(1,n+1)] or [0]))
    print('R3 diff met Rock af (blauw/lijn):',int(sum(1 for y in range(36,43) for x in range(43,51) if O[y,x]!=R[y,x] and R[y,x] in BLAUW+[1] and B[y,x] in BLAUW+[1])))
    with open('log_r8.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('%s x=%d y=%d %d->%d\n'%('heup' if heup[y,x] else 'benen',x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    H='0123456789abcdef'
    for y in range(35,58): print('%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(14,52)))
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    zz=12; x0,y0,x1,y1=14,35,52,58
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',64*zz).crop((x0*zz,y0*zz,x1*zz,y1*zz)); os.chdir(HIER)
    ps=[m]+[sprite(p).crop((x0,y0,x1,y1)).resize(((x1-x0)*zz,(y1-y0)*zz),Image.NEAREST) for p in
        ('../sprite_r7/gnometrotter_grass.png','gnometrotter_grass.png','../../gnometrotter_rock/af/gnometrotter_rock.png')]
    w=(x1-x0)*zz; W=Image.new('RGB',(4*(w+10),(y1-y0)*zz),'white')
    for k,p in enumerate(ps): W.paste(p,(k*(w+10),0))
    W.save('vel.png')
