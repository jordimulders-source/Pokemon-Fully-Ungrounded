# maak_r6.py: Gnometrotter Grass r6 = r5 + (1) romp: gebogen duigen/nerf in perspectief, gebogen licht/donker, sikkel boven de riem;
# (2) benen: gebogen ribbels/grenslijnen; (3) rechterarm = Rock af (keuring_r5 punt A); (4) punt B, D en (60,36).
# Buiten deze zones 0 px (assert). Log: log_r6.txt.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
bim=Image.open('../sprite_r5/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
ZONE=np.full((64,64),'',dtype=object)
def zet(x,y,v,z): O[y,x]=v; ZONE[y,x]=z
PINK=[6,7,8,15]; BLAUW=[9,10,11]

# ---- zones romp en benen (zelfde afbakening als r4/r5) ----
OVAAL={21:(41,44),22:(40,47),23:(40,48),24:(40,49),25:(40,49),26:(41,49),27:(42,49),28:(44,47)}
uit=np.zeros((64,64),bool)
for y,(a,b) in OVAAL.items(): uit[y,a:b+1]=True
uit[:,:26]=True; uit[:,50:]=True; uit[26:,48:]=True; uit[:20,:]=True
L,_=ndimage.label(np.isin(B,PINK)&~uit); romp=L==L[30,33]
been=np.zeros((64,64),bool)
for y in range(36,60):
    for x in range(1,63):
        if B[y,x] in BLAUW and not any(B[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): been[y,x]=True

# ---- 1. ROMP ----
# licht: bogen rond een lichtpunt linksboven (horizontaal iets uitgerekt) -> 8/7-grens is een boog
LX,LY=31.0,22.0
def tint_romp(x,y):
    r=np.hypot((x-LX)/1.25,(y-LY))
    return 15 if r<3.0 else (8 if r<11.5 else 7)
# duigen: modellijnen (gemeten per rij, sprite_r5/meet.py-geometrie: x ±29,5/31, ±35,2, nerf ±37,6, ±43) in perspectief gebogen:
# links van het tonmidden (x ±37) buigen ze naar links, rechts ervan naar rechts; onderaan terug naar het midden.
def s1(y): return 31 if y<=23 or y>=34 else 30          # naad 6
def s2(y): return 35 if y<=23 or y>=33 else 34          # naad 6
def s3(y): return 37 if y<=24 or y>=33 else 38          # nerf (stippellijn model), 7 in het licht
def s4(y): return 44 if y<=30 else 43                   # naad 6 onder de schouder (model x ±43, rij 25-37)
onder=np.zeros((64,64),bool)
for y,x in zip(*np.nonzero(romp)):
    if B[y+1,x] in (2,3,4) and x>=31: onder[y,x]=True     # onderste rij boven de riem
rechts=np.zeros((64,64),bool)
for y in range(29,37):
    xs=[x for x in range(40,50) if romp[y,x]]
    if xs and max(xs)>=45: rechts[y,max(xs)]=True        # rand waar het lijf achter de schouder wegdraait
for y,x in zip(*np.nonzero(romp)):
    t=tint_romp(x,y)
    if x==s1(y) and y>=20 or x==s2(y) and y>=21: t=6
    elif x==s4(y) and 29<=y: t=6
    elif x==s3(y) and 22<=y and t==8: t=7
    if onder[y,x] or rechts[y,x]: t=6                    # sikkel boven de riem en rechts
    if t!=O[y,x]: zet(x,y,t,'lijf')

# ---- 2. BENEN: volume per bol (r4/r5) + gebogen lijnen uit het model ----
DELEN={'LT':((25,44.5),6.5,3.8),'RT':((40.5,44.5),9.5,5.0),'LF':((21.5,51.0),6.0,2.6),'RF':((44.5,52.5),5.0,3.0)}
GRENS_L={20:49,21:49,22:48,23:48,24:48,25:48,26:49,27:49}   # bovenrand voetbol L (bol naar boven)
GRENS_R={41:50,42:50,43:49,44:49,45:49,46:50,47:50}         # bovenrand voetbol R
def deel(x,y):
    if x<=30 and (y>=50 or (x in GRENS_L and y>GRENS_L[x])): return 'LF'
    if x>=38 and (y>=51 or (x in GRENS_R and y>GRENS_R[x])): return 'RF'
    if 42<=y<=48 and x<=30+max(0,(y-43))*0.5: return 'LT'
    return 'RT'
def vol(x,y):
    (cx,cy),rx,ry=DELEN[deel(x,y)]
    d=0.7*(x-cx)/rx+0.6*(y-cy)/ry
    return 11 if d<0.2 else (10 if d<0.95 else 9)
# lijnen (model: bovenrand + diagonale ribbel linkerdij, onderrand rechterdij; grenslijnen dij|voet) als bogen om de bol
LIJNEN={
 'ribbel LT':  ([(21,44),(22,43),(23,43),(24,43),(25,44),(26,44),(27,45),(28,46),(29,46)],None),
 'grens L':    ([(x,y) for x,y in GRENS_L.items()],9),
 'grens R':    ([(x,y) for x,y in GRENS_R.items()],9),
}
lijn={}
for naam,(pts,t) in LIJNEN.items():
    if t is None: t=10 if np.mean([vol(x,y)==11 for x,y in pts])>=0.5 else 9
    for p in pts: lijn[p]=t
for y,x in zip(*np.nonzero(been)):
    t=lijn.get((x,y),vol(x,y))
    if t!=O[y,x]: zet(x,y,t,'benen')

# losse vlakjes < 3 px in romp/benen (geen lijnpixel) -> meest voorkomende tint van de zoneburen
zone=romp|been
for k in (6,7,8,15,9,10,11):
    Lc,nc=ndimage.label((O==k)&zone)
    for i in range(1,nc+1):
        ys,xs=np.nonzero(Lc==i)
        if len(ys)>=3 or any((x,y) in lijn for x,y in zip(xs,ys)): continue
        if ((O==k)&~zone&ndimage.binary_dilation(Lc==i,np.ones((3,3)))).any(): continue
        nb=[O[y+dy,x+dx] for x,y in zip(xs,ys) for dx in (-1,0,1) for dy in (-1,0,1) if zone[y+dy,x+dx] and O[y+dy,x+dx]!=k]
        if nb:
            v=max(set(nb),key=nb.count)
            for x,y in zip(xs,ys): zet(x,y,v,'lijf' if romp[y,x] else 'benen')

# ---- 3. RECHTERARM (bovenarm + schouder) = Rock af, keuring_r5 punt A (exact) ----
A=[(41,19,7),(42,19,7),(40,20,7),(41,20,7),(42,20,7),(43,20,7),(40,21,7),(51,26,1),(40,27,7),(41,27,7),(52,27,1),(53,27,1),
   (40,28,7),(41,28,7),(48,28,7),(49,28,7),(50,28,6),(51,28,8),(52,28,15),(54,28,1),(40,29,7),(41,29,6),(42,29,8),(43,29,8),
   (51,29,7),(54,29,1),(40,30,6),(42,30,8),(43,30,8),(51,30,7),(52,30,8),(55,30,1),(41,31,8),(42,31,8),(51,31,7),(52,31,7),
   (55,31,1),(40,32,8),(53,32,7),(55,32,1),(53,33,1),(54,33,1),(53,34,0)]
for x,y,v in A: zet(x,y,v,'rechterarm')
# ---- 4. punt B, D, rechterhand ----
for x,y in ((16,28),(17,28)): zet(x,y,6,'linkerhand')
for x,y in ((21,6),(20,7),(17,12)): zet(x,y,5,'mutsrand')
zet(60,36,1,'rechterhand')

if __name__=='__main__':
    ver=O!=B
    assert not (ver&(ZONE=='')).any(), 'pixel buiten de zones'
    tel={z:int((ver&(ZONE==z)).sum()) for z in ('lijf','benen','rechterarm','linkerhand','mutsrand','rechterhand')}
    tel['rest']=int((ver&(ZONE=='')).sum()); print('t.o.v. r5:',tel,'totaal',int(ver.sum()))
    with open('log_r6.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('%s x=%d y=%d %d->%d\n'%(ZONE[y,x],x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    assert out.getpalette()[:48]==bim.getpalette()[:48]
    H='0123456789abcdef'
    for y in range(17,58): print('%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(14,62)))
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',512); os.chdir(HIER)
    ps=[m,sprite('../sprite_r5/gnometrotter_grass.png').resize((512,512),Image.NEAREST),sprite('gnometrotter_grass.png').resize((512,512),Image.NEAREST),
        sprite('../../gnometrotter_rock/af/gnometrotter_rock.png').resize((512,512),Image.NEAREST)]
    W=Image.new('RGB',(len(ps)*520,512),'white')
    for k,p in enumerate(ps): W.paste(p,(k*520,0))
    W.save('vel.png')
