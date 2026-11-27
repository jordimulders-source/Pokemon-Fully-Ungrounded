# Ronde 3 (op B, gezicht b als basis): Jordi's punten + keurder. Alleen verschuiven, weghalen, tinten kiezen.
import numpy as np; from PIL import Image
import maak_r1 as m1, maak_r2 as m2, reduceer3, schoon, bouw, bewerk, ogen
LOG={}
def log(k,v): LOG.setdefault(k,[]).extend(v if isinstance(v,list) else [v])
def basis():
    a=m1.natief('B',(-8,-14),(0,-8),0)          # geen lijnweg meer in het lijf; lijnen: zwart >=2 of (zwart+bruin) >=5
    lab=reduceer3.reduceer(a,(2,2),2,bouw.Z_HOOFD,3,bouw.Z_HOOFD.copy(),'gem',None,5)[2:66,0:64].copy()
    lab=schoon.tintclusters(lab,6); lab=schoon.losse_lijnen(lab,3)
    lab,gw=m1.glasspikkels_weg(lab); log('glasspikkels weg',gw)
    return lab
def zand(lab,p):
    n=schoon.buurtint(lab,p,1,set()); return n if n else 12
def boeilijn(lab):
    """Model heeft een donkere lijn rond de boeien: zandpixels die aan een boei grenzen krijgen de lijntint."""
    g=(lab>=20)&(lab<30); g[:19]=False; g[38:]=False; gezet=[]
    for y in range(19,38):
        for x in range(8,44):
            if 10<=lab[y,x]<20 and any(g[y+dy,x+dx] for dy,dx in schoon.N4): lab[y,x]=1; gezet.append((y,x))
    log('boeilijn (tint)',gezet); return lab
# hersenwindingen: alle binnenlijnen in de hersenzone weg, daarna 3 krullen terug uit de kale r5-reductie (kz=2)
KAAL=None
def kaal():
    global KAAL
    if KAAL is None:
        a=bewerk.maak((-8,-14),(0,-8))
        KAAL=(reduceer3.reduceer(a,(2,2),2,bouw.Z_HOOFD,2,None,'gem')[2:66,0:64].copy(),
              reduceer3.reduceer(a,(2,2),2,bouw.Z_HOOFD,3,None,'gem')[2:66,0:64].copy())
    return KAAL
KRULLEN=[(8,29),(8,30),(8,31),(9,32),(10,32),(10,31),(11,28),(11,29),     # middenspiraal
         (8,27),(9,27),(10,26),(11,26),                                     # linkerkrul
         (9,35),(9,34),(10,34),(11,34),(11,35)]                             # rechterkrul
def windingen(lab):
    k2,k3=kaal(); weg=[]
    for y in range(7,13):
        for x in range(24,37):
            if lab[y,x] not in (1,10): continue
            if any(lab[y+dy,x+dx]==0 for dy,dx in schoon.N8): continue     # buitenlijn blijft
            t=k3[y,x]; lab[y,x]=t if 10<t<20 else zand(lab,(y,x)); weg.append((y,x))
    for p in KRULLEN:
        assert k2[p]==1, p          # elke krulpixel is een lijnpixel in de kale reductie
        lab[p]=1
    log('windingen weg',weg); log('krullen uit kale r5',KRULLEN); return lab
def wenkbrauwen(lab):
    """Losse, schuine wenkbrauwen (boos, naar het midden omlaag zoals r5/r8): de brug tussen de ogen (x27-28) weg,
    de buitenste 2 pixels van elke wenkbrauw 1 rij omhoog geschoven (links x23-24, rechts x31 en x33 -> x32)."""
    for x in (27,28):
        if lab[13,x] in (1,10): lab[13,x]=zand(lab,(13,x)); log('wenkbrauwbrug weg',(13,x))
    for (y,x),(Y,X) in [((13,23),(12,23)),((13,24),(12,24)),((13,31),(12,31)),((13,33),(12,32))]:
        if lab[y,x] in (1,10):
            v=lab[y,x]; lab[y,x]=zand(lab,(y,x)); lab[Y,X]=v; log('wenkbrauw verschoven',((y,x),(Y,X)))
    return lab
def oogzone_leeg(lab):
    for y in range(13,17):
        for x in range(21,37):
            if lab[y,x] in (2,3,23): lab[y,x]=zand(lab,(y,x))
    return lab
def ogen_r8_3(lab,x0=23,y0=13,dr=1):
    """(i) r8-ogen op de echte schaal (/3, fase 1,1): per oog wit (oogwit), zwart (pupil), donkerbruin (ooglid)."""
    o=ogen.oog((80,52,107,63),(1,1),f=3)[:3]
    for r in range(3):
        for c in range(9):
            v=o[r,c]
            if v not in (1,23,10): continue
            if r==0 and v!=1: continue
            dx=dr if c>=4 else 0
            lab[y0+r,x0+c+dx]={1:2,23:3,10:10}[v]
    return lab
def ogen_gen3(lab,naam,links,rechts,mp,doel_l,doel_r):
    """Oog 1-op-1 uit een Gen 3-sprite: links/rechts = (x0,x1,y0,y1) in de bron, doel = linkerbovenhoek in de sprite.
    rechts=None: het linkeroog gespiegeld voor het rechteroog."""
    a=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%naam)).astype(int)
    def plak(box,doel,spiegel=False):
        x0,x1,y0,y1=box
        for y in range(y0,y1):
            for x in range(x0,x1):
                v=a[y,x]
                if v not in mp: continue
                X=(x1-1-x) if spiegel else (x-x0)
                lab[doel[1]+y-y0,doel[0]+X]=mp[v]
    plak(links,doel_l)
    if rechts: plak(rechts,doel_r)
    else: plak(links,doel_r,True)
    return lab
def keurder(lab):
    fix={(0,33):10,(2,29):10,(3,29):10,(5,29):10,(6,26):10,(6,27):10,(7,25):10,(9,23):10,
         (20,41):14,(20,43):14,(21,44):13,(51,23):31,(27,39):12}
    for p,t in fix.items():
        if lab[p]!=0: lab[p]=t; log('keurder (tint)',(p,t))
    return lab
OOG={'i':('r8 /3',lambda l:ogen_r8_3(l)),
     'ii':('Graveler',lambda l:ogen_gen3(l,'graveler',(25,30,25,28),(33,39,24,28),{15:10,14:11,1:3,4:2,2:3},(22,13),(27,12))),
     'iii':('Geodude (gespiegeld voor het 2e oog)',lambda l:ogen_gen3(l,'geodude',(31,36,33,37),None,{15:2,14:10,1:3,2:3},(22,12),(28,12)))}
def bouw_sprite(oog='i'):
    LOG.clear()
    lab=basis(); lab=boeilijn(lab); lab=windingen(lab)
    lab=oogzone_leeg(lab); lab=wenkbrauwen(lab); lab=OOG[oog][1](lab)
    lab=m1.barst_r5_weg(lab); lab,gb=m1.barst(lab); log('barst r10',gb)
    lab=m2.schouderglas(lab); lab,_=m2.linkerbol(lab)
    lab=bouw.binnenlijnen(bouw.buitenlijn(lab))
    lab=keurder(lab)
    return lab
