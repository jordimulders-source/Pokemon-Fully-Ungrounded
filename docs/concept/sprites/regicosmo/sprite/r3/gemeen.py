# Gedeelde metingen en palet (geen neveneffecten bij import).
# Natief raster (natief.py, cel 5,86 px) -> 7 hemellichamen als losse delen; per deel een eigen deelpalet.
import numpy as np, os; from PIL import Image; from scipy import ndimage
D=os.path.dirname(os.path.abspath(__file__))
# Palet: index 0 transparant. Tinten = modelclusters (k-means per deel), richting Gen 3 gezet (verzadigd, stappen ±30-40).
PAL=[(152,208,160),   # 0 transparant
 (16,16,16),          # 1 zwart (buitenlijn schaduwkant, alle delen)
 (168,64,48),         # 2 Mars donkerrood (model 172,83,57): schaduw, kratertjes, selout Mars/Saturnus
 (220,96,68),         # 3 Mars rood (222,97,71)
 (240,148,96),        # 4 Mars oranje (236,149,95)
 (248,192,152),       # 5 Mars perzik (243,181,144)
 (84,60,50),          # 6 bruin donker: donkere band Mars (77,49,43), asteroide donker, ring donker
 (120,90,74),         # 7 bruin midden: band Mars (110,84,73), asteroide midden, zandvoet donker (113,93,61)
 (120,216,212),       # 8 stip cyaan (model 155,210,189 met wit hart) = ook ijsplaneet midden (Jordi: stipkleuren in de planeet linksboven)
 (214,238,246),       # 9 bijna-wit: stiplicht = ijsplaneet licht (210,239,247)
 (152,122,106),       # 10 asteroide licht (150,124,110) (vrijgekomen door ijs = stipkleuren)
 (200,200,204),       # 11 lichtgrijs: maan licht (197-210), ring licht
 (52,64,84),          # 12 leisteen donker: blauwe voet (54,68,83), selout ijs/maan, maanschaduw
 (118,126,142),       # 13 grijsleisteen: maankraters (135-164), blauwe voet licht (97,114,138 / 114,131,156), ring (143,125,110)
 (150,126,86),        # 14 zand midden (139,118,81)
 (206,182,136)]       # 15 zand licht (199,176,133)
NAMEN=['Mars','ijs','Saturnus','asteroide','maan','voet blauw','voet zand']
# toegestane kleuren per deel (alleen voor de dichtstbijzijnde-kleurkeuze van de kale reductie)
SUB={'Mars':[1,2,3,4,5,6,7],'ijs':[1,12,13,8,9],'Saturnus':[1,6,13,11,2,3,4,5],'asteroide':[1,6,7,10],
     'maan':[1,12,13,11],'voet blauw':[1,12,13],'voet zand':[1,7,14,15]}
SELOUT={'Mars':2,'ijs':13,'Saturnus':6,'asteroide':6,'maan':13,'voet blauw':12,'voet zand':7}
def natief():
    a=np.array(Image.open(os.path.join(D,'natief.png')).convert('RGB')).astype(int)
    wh=a.min(2)>=246                     # achtergrond = puur wit (>=252) dat met de rand samenhangt; lichte ijspixels blijven figuur
    wl,wn=ndimage.label(wh); rand=np.unique(np.r_[wl[0],wl[-1],wl[:,0],wl[:,-1]]); rand=rand[rand>0]
    fg=~np.isin(wl,rand)
    # gaten in de ring van Saturnus zijn wel achtergrond: wit dat niet met de rand samenhangt maar >= 2 px groot is
    gat=wh&~np.isin(wl,rand)
    gl,gn=ndimage.label(gat)
    for h in range(1,gn+1):
        if (gl==h).sum()>=2: fg[gl==h]=False
    lab,n=ndimage.label(fg,np.ones((3,3)))
    sz=np.bincount(lab.ravel())
    deel=np.full(fg.shape,-1)
    for c in range(1,n+1):
        if sz[c]<50: continue
        ys,xs=np.where(lab==c)
        cx,cy=xs.mean(),ys.mean()
        if sz[c]>2000: nm='Mars'
        elif cy<70: nm='ijs' if cx<120 else 'Saturnus'
        elif cy<95: nm='asteroide' if cx<120 else 'maan'
        else: nm='voet blauw' if cx<120 else 'voet zand'
        deel[lab==c]=NAMEN.index(nm)
    # gaten binnen een deel (wit/hooglicht in de ring van Saturnus is wel achtergrond: alleen gaten < 4 px vullen)
    for k in range(7):
        m=deel==k; f=ndimage.binary_fill_holes(m)&~m
        hl,hn=ndimage.label(f)
        for h in range(1,hn+1):
            if (hl==h).sum()<4: deel[hl==h]=k
    dot=(deel==0)&(a[...,1]>170)&(a[...,1]-a[...,0]>40)&(a[...,2]>150)
    return a,deel,dot
def dichtst(rgb,idxs):
    P=np.array(PAL,float)[idxs]
    d=((P-np.array(rgb,float))**2*[0.35,0.45,0.2]).sum(1)
    return idxs[int(d.argmin())]
