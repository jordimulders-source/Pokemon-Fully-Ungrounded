# maak_r4.py: Gnometrotter Grass r4 uit de basis (sprite_hybride_r2) + Rock af.
# Vier zones: neus, schouder (rechts), linkerhand, lijf. Elke gewijzigde pixel wordt gelogd (log_r4.txt).
import numpy as np
from PIL import Image
from scipy import ndimage
BASIS='../sprite_hybride_r2/gnometrotter_grass_hybride.png'
ROCK='../../gnometrotter_rock/af/gnometrotter_rock.png'
bim=Image.open(BASIS); B=np.asarray(bim).astype(int); R=np.asarray(Image.open(ROCK)).astype(int)
O=B.copy(); ZONE=np.zeros_like(B)   # 1 neus, 2 schouder, 3 linkerhand, 4 lijf
PINK=[6,7,8,15]; BLAD=[5,12,13,14]
def zet(x,y,v,z):
    O[y,x]=v; ZONE[y,x]=z
ROCK2GRASS={12:6}   # Rock-index 12 (zeer donker roze) bestaat niet in het Grass-palet -> 6 (donkerste roze)

# 1. NEUS: Rock af-neus (zelfde modelneus: centrum 21,27/19,59 in beide modellen); bladpixels van de baard blijven.
L,_=ndimage.label(np.isin(R,[7,8,15])); binnen=L==L[19,21]
ring=ndimage.binary_dilation(binnen,np.ones((3,3)))&~binnen&np.isin(R,[6,12])
neus=binnen|ring
for y,x in zip(*np.nonzero(neus)):
    if B[y,x] in (13,14): continue
    zet(x,y,ROCK2GRASS.get(R[y,x],R[y,x]),1)
# oude neuspixels buiten de nieuwe neus
oud=np.zeros_like(neus); Lb,_=ndimage.label(np.isin(B,PINK)); oud=(Lb==Lb[19,20])&~neus
for y,x in zip(*np.nonzero(oud)): print('oude neuspixel buiten masker',x,y,B[y,x])

# 2. SCHOUDER RECHTS: ovaal van Rock af (zelfde model-ovaal), rij 21-28; ligt voor de rugtak.
OVAAL={21:(41,44),22:(40,47),23:(40,48),24:(40,49),25:(40,49),26:(41,49),27:(42,49),28:(44,47)}
for y,(a,b) in OVAAL.items():
    for x in range(a,b+1): zet(x,y,R[y,x],2)

# 3. LINKERHAND (vuist + arm): Rock af in x 0-19, rij 27-36 waar Rock hand/omlijning is;
#    houten stok blijft van de basis, alleen waar de vuist de stok overlapt volgt Rock af. Baardblad blijft.
HAND=[1,6,7,8,15]
for y in range(27,37):
    for x in range(0,20):
        r,b=R[y,x],B[y,x]
        if b in BLAD: continue
        if y==36:   # onderrand vuist: alleen zwarte vuistrand op achtergrond/roze, stok blijft
            if r==1 and b in (0,1,6,7,8,15): zet(x,y,1,3)
            elif b in PINK and r==0: zet(x,y,0,3)
            continue
        if r in HAND or (r==0 and b in PINK+[1]):
            if b in (2,3,4) and r==0: continue
            zet(x,y,r,3)

# 4a. LIJF, ROMP: roze romp als ton van drie planken (model: naden op x 29,5 en x 35), Gen 3-volume, licht linksboven.
#     Silhouet blijft; alleen tinten 6/7/8/15 binnen de bestaande roze rompvlakken.
Lr,_=ndimage.label(np.isin(O,PINK)&(ZONE==0))
romp=(Lr==Lr[30,33])
romp[:23,:32]=False            # band achter de neus blijft
romp[:, 50:]=False; romp[26:,48:]=False   # rechterarm (elleboog/hand) hoort niet bij de romp
def rompkleur(x,y):
    if x in (29,35): return 6                      # plankennaden in de donkerste eigen tint
    if x<=28: return 7                             # plank A (in de schaduw van de baardbladeren)
    if x<=34:                                      # plank B
        if x==30: return 15 if y<=25 else 8
        if x==34: return 7
        return 8 if y<=31 else 7
    # plank C
    if x==36: return 15 if y<=24 else (8 if y<=32 else 7)
    if x==37: return 8 if y<=32 else 7
    if x<=42: return 8 if y<=29 else 7
    if x<=46: return 8 if y<=21 else 7
    return 6
for y,x in zip(*np.nonzero(romp)):
    v=rompkleur(x,y)
    if v!=O[y,x]: zet(x,y,v,4)

# bovenrand romp naast de neus (was een 6/8-dambord): rij 19 = schaduw onder de muts (7), rij 20-22 plank, naad x29 vanaf rij 21
for y in range(19,23):
    for x in range(26,34):
        if O[y,x] in PINK and ZONE[y,x] in (0,4):
            v = 7 if y==19 else (6 if (x==29 and y>=21) else (7 if x==29 else 8))
            if v!=O[y,x]: zet(x,y,v,4)

# 4b. LIJF, BENEN: vier bollen uit het model (dij L, dij R, onderbeen/voet L, voet R), elk Gen 3-volume
#     met 11 (licht linksboven), 10, 9 (sikkel rechtsonder); naden in 9 (kruisvouw dij|dij, grenslijn dij|voet).
#     Buitenrand (pixels naast achtergrond) en zwart blijven; silhouet blijft.
BLAUW=[9,10,11]
DELEN={'LT':((25,44.5),6.5,3.8),'RT':((40.5,44.5),9.5,5.0),'LF':((21.5,51.0),6.0,2.6),'RF':((44.5,52.5),5.0,3.0)}
def deel(x,y):
    if y>=50 and x<=30: return 'LF'
    if y>=51 and x>=38: return 'RF'
    if y<=48 and x<=30+max(0,(y-43))*0.5 and y>=42: return 'LT'
    return 'RT'
def naad(x,y):
    if y==49 and 19<=x<=27: return True          # grenslijn dij|onderbeen L
    if y==50 and 41<=x<=47: return True          # grenslijn dij|voet R
    if 43<=y<=47 and x==int(30+(y-43)*0.5): return True   # kruisvouw tussen de dijen
    return False
def benen(x,y):
    if naad(x,y): return 9
    (cx,cy),rx,ry=DELEN[deel(x,y)]
    d=0.7*(x-cx)/rx+0.6*(y-cy)/ry
    return 11 if d<0.2 else (10 if d<0.95 else 9)
for y in range(36,60):
    for x in range(64):
        if O[y,x] not in BLAUW: continue
        if any(O[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): continue
        v=benen(x,y)
        if v!=O[y,x]: zet(x,y,v,4)

def toon(A,y0,y1,x0,x1):
    H='0123456789abcdef'
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join('.' if A[y,x]==0 else H[A[y,x]] for x in range(x0,x1)))
if __name__=='__main__':
    import sys
    sys.path.insert(0,'../../gnometrotter_rock/sprite')
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    assert out.getpalette()[:48]==bim.getpalette()[:48]
    NAAM={1:'neus',2:'schouder',3:'linkerhand',4:'lijf',0:'rest'}
    ver=O!=B; tel={NAAM[z]:int((ver&(ZONE==z)).sum()) for z in NAAM}
    with open('log_r4.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('%s x=%d y=%d %d->%d\n'%(NAAM[ZONE[y,x]],x,y,B[y,x],O[y,x]))
    print(tel, 'totaal', int(ver.sum()))
    # vel: model op schaal | basis | r4 (8x)
    import os; cwd=os.getcwd(); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',512)
    os.chdir(cwd)
    ps=[m,sprite(BASIS).resize((512,512),Image.NEAREST),sprite('gnometrotter_grass.png').resize((512,512),Image.NEAREST)]
    W=Image.new('RGB',(3*520,512),'white')
    for k,p in enumerate(ps): W.paste(p,(k*520,0))
    W.save('vel.png')
