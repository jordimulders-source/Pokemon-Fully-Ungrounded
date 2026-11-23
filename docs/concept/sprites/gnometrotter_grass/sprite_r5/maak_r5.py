# maak_r5.py: Gnometrotter Grass r5 = r4 + alleen de lijfzone opnieuw (romp en benen).
# Naden/nerf/ribbels komen uit het model (meet.npz van meet.py: aandeel donkere lijnpixels per spritepixel),
# volume als één bol per vorm (licht linksboven). Neus, schouder, linkerhand en rest: 0 px. Log: log_r5.txt.
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage
HIER=os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
bim=Image.open('../sprite_r4/gnometrotter_grass.png'); B=np.asarray(bim).astype(int); O=B.copy()
D=np.load('meet.npz')['donk']
PINK=[6,7,8,15]; BLAUW=[9,10,11]

# ---- lijfzone (zelfde afbakening als r4) ----
# romp: roze samenhang rond (33,30) zonder neus (links van x 26 boven rij 23), schouderovaal en rechterarm
OVAAL={21:(41,44),22:(40,47),23:(40,48),24:(40,49),25:(40,49),26:(41,49),27:(42,49),28:(44,47)}
uit=np.zeros((64,64),bool)
for y,(a,b) in OVAAL.items(): uit[y,a:b+1]=True
uit[:,:26]=True; uit[:,50:]=True; uit[26:,48:]=True; uit[:20,:]=True   # rij <= 19 (schaduw onder de muts, r4) blijft
L,_=ndimage.label(np.isin(B,PINK)&~uit); romp=L==L[30,33]
# benen: blauw vanaf rij 36, niet op de buitenrand (naast achtergrond)
been=np.zeros((64,64),bool)
for y in range(36,60):
    for x in range(1,63):
        if B[y,x] in BLAUW and not any(B[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): been[y,x]=True

def ketens(mask,drempel,minlen=3):
    """modellijnen: spritepixels met donk >= drempel die in een 8-samenhangende keten van >= minlen liggen"""
    m=mask&(D>=drempel); Lk,n=ndimage.label(m,np.ones((3,3)))
    out=np.zeros_like(m)
    for i in range(1,n+1):
        if (Lk==i).sum()>=minlen: out|=Lk==i
    return out

# ---- ROMP: één ronde ton ----
LX,LY=31.0,22.0     # lichtpunt linksboven op de ton; tinten in bogen eromheen -> sikkel rechts en onder
def tint_romp(x,y):
    r=np.hypot((x-LX)/1.15,(y-LY))
    if r< 3.0: return 15
    if r< 12.5: return 8
    return 7
naad_romp=ketens(romp,0.45,4)
# alleen echte verticale naden: kolommen met >= 4 naadpixels
for x in range(64):
    if naad_romp[:,x].sum()<4: naad_romp[:,x]=False
# naden die binnen 2 kolommen van een langere naad liggen zijn dezelfde (verdubbelde) modelnaad: alleen de langste houden
kol=sorted([x for x in range(64) if naad_romp[:,x].any()],key=lambda x:-naad_romp[:,x].sum())
gehouden=[]
for x in kol:
    if any(abs(x-g)<=2 for g in gehouden): naad_romp[:,x]=False
    else: gehouden.append(x)
# nerf: zwakke maar doorlopende modellijn (kolomgemiddelde donk >= 0,12 over >= 8 rompbijen, niet naast een naad) = 7 in het licht
nerf=np.zeros((64,64),bool)
for x in range(64):
    rij=np.nonzero(romp[:,x])[0]
    if len(rij)>=8 and D[rij,x].mean()>=0.12 and all(abs(x-g)>1 for g in gehouden): nerf[rij,x]=True
print('nerfkolommen:',[x for x in range(64) if nerf[:,x].any()])
# per kolom: sterke naad (gemiddeld donk >= 0,55) = plankennaad in 6, zwakkere = nerf in 7 (in de schaduw 6)
sterk={x:D[naad_romp[:,x],x].mean()>=0.55 for x in range(64) if naad_romp[:,x].any()}
print('naden/nerf (kolom: sterk?, rijen):',{x:(bool(v),int(naad_romp[:,x].sum())) for x,v in sterk.items()})
for y,x in zip(*np.nonzero(romp)):
    t=tint_romp(x,y)
    if naad_romp[y,x]:
        t=6 if (sterk[x] or t==7) else 7
    elif nerf[y,x] and t==8: t=7
    O[y,x]=t

# ---- BENEN: volume per bol (zoals r4) + ribbels/naden uit het model ----
DELEN={'LT':((25,44.5),6.5,3.8),'RT':((40.5,44.5),9.5,5.0),'LF':((21.5,51.0),6.0,2.6),'RF':((44.5,52.5),5.0,3.0)}
def deel(x,y):
    if y>=50 and x<=30: return 'LF'
    if y>=51 and x>=38: return 'RF'
    if 42<=y<=48 and x<=30+max(0,(y-43))*0.5: return 'LT'
    return 'RT'
def vol(x,y):
    (cx,cy),rx,ry=DELEN[deel(x,y)]
    d=0.7*(x-cx)/rx+0.6*(y-cy)/ry
    return 11 if d<0.2 else (10 if d<0.95 else 9)
def grens(x,y):   # grenslijn dij|voet (GEDEELD: voetballen met grenslijn), uit r4
    return (y==49 and 19<=x<=27) or (y==50 and 41<=x<=47)
lijn_been=ketens(been,0.42,4)
# per modellijn één tint: ligt de lijn grotendeels in het licht (11) dan ribbel 10, anders naad 9
Lb,nb=ndimage.label(lijn_been,np.ones((3,3))); lijntint={}
for i in range(1,nb+1):
    ys,xs=np.nonzero(Lb==i); licht=np.mean([vol(x,y)==11 for x,y in zip(xs,ys)])
    lijntint[i]=10 if licht>=0.5 else 9
for y,x in zip(*np.nonzero(been)):
    t=vol(x,y)
    if grens(x,y): t=9
    elif lijn_been[y,x]: t=lijntint[Lb[y,x]]
    O[y,x]=t

# opschonen in de lijfzone: losse pixel (alle 4 buren in de zone met één andere tint) krijgt die tint
zone=romp|been
for _ in range(2):
    P=O.copy()
    for y,x in zip(*np.nonzero(zone)):
        nb=[P[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if zone[y+dy,x+dx]]
        if len(nb)==4 and len(set(nb))==1 and nb[0]!=P[y,x] and not grens(x,y): O[y,x]=nb[0]

# losse vlakjes < 3 px in de lijfzone (geen naad/grenslijn): krijgen de meest voorkomende tint van hun zoneburen (8-buren)
for k in (6,7,8,15,9,10,11):
    Lc,nc=ndimage.label((O==k)&zone)
    for i in range(1,nc+1):
        ys,xs=np.nonzero(Lc==i)
        if len(ys)>=3 or ((O==k)&~zone&ndimage.binary_dilation(Lc==i,np.ones((3,3)))).any(): continue
        if any(grens(x,y) for x,y in zip(xs,ys)): continue
        nb=[O[y+dy,x+dx] for x,y in zip(xs,ys) for dx in (-1,0,1) for dy in (-1,0,1)
            if zone[y+dy,x+dx] and O[y+dy,x+dx]!=k and O[y+dy,x+dx] in PINK+BLAUW]
        if nb:
            v=max(set(nb),key=nb.count)
            for x,y in zip(xs,ys): O[y,x]=v

if __name__=='__main__':
    ver=O!=B
    zone=np.where(romp|been,'lijf','rest')
    tel={'neus':0,'schouder':0,'linkerhand':0,'lijf':int((ver&(romp|been)).sum()),'rest':int((ver&~(romp|been)).sum())}
    assert tel['rest']==0
    with open('log_r5.txt','w') as f:
        for y,x in zip(*np.nonzero(ver)): f.write('%s x=%d y=%d %d->%d\n'%(zone[y,x],x,y,B[y,x],O[y,x]))
    out=Image.new('P',(64,64)); out.putpalette(bim.getpalette()); out.putdata(O.astype('uint8').ravel().tolist())
    out.save('gnometrotter_grass.png'); out.resize((512,512),Image.NEAREST).save('gnometrotter_grass_8x.png')
    assert out.getpalette()[:48]==bim.getpalette()[:48]
    # telling t.o.v. de basis (sprite_hybride_r2) per zone = r4-telling + lijf opnieuw
    print('t.o.v. r4:',tel)
    H='0123456789abcdef'
    for y in range(17,58): print('%2d '%y+''.join('.' if O[y,x]==0 else H[O[y,x]] for x in range(14,52)))
    sys.path.insert(0,'../../gnometrotter_rock/sprite'); os.chdir('../../gnometrotter_rock/sprite')
    from kijk import sprite, model_op_schaal
    m=model_op_schaal('../../gnometrotter_grass/hybride/model_hybride.png',512); os.chdir(HIER)
    ps=[m,sprite('../sprite_hybride_r2/gnometrotter_grass_hybride.png').resize((512,512),Image.NEAREST),
        sprite('../sprite_r4/gnometrotter_grass.png').resize((512,512),Image.NEAREST),sprite('gnometrotter_grass.png').resize((512,512),Image.NEAREST)]
    W=Image.new('RGB',(len(ps)*520,512),'white')
    for k,p in enumerate(ps): W.paste(p,(k*520,0))
    W.save('vel.png')
