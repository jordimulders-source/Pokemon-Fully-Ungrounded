# Swablu (onweerswolk) r2: "swablu is nog wat blurry" (Jordi over r1).
# Basis = r1 (silhouet bevroren, alpha-diff 0). Oorzaak blur gemeten: r1 koos per spritepixel de tint bij de GEMIDDELDE modelkleur,
# daardoor werden randen tussen modelvlakken middentinten (verloop). r2 telt per spritepixel de modeltonen (stemming per natieve pixel,
# oppervlaktegewogen) en neemt de meest voorkomende: heldere vlakken zoals het model, dat zelf al in 3 tonen per materiaal staat.
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); from klassen import klassen
import gemeen as G
from gemeen import overlap, label, S
a,c,L=klassen()
# --- palet r2: wolk 5 tonen (2 materialen à 3 + selout), stappen ±30-45; vogel 3; geel feller; wit 2 ---
PAL=[(152,208,160),(13,17,24),
     (62,72,90),(92,104,122),(124,136,154),(162,174,190),(208,214,226),   # 2 wolk diep, 3 donker, 4 midden, 5 licht, 6 wit
     (68,90,110),(106,130,152),(150,174,194),                            # 7 vogel donker, 8 midden, 9 licht
     (200,158,40),(248,214,64),(255,246,160),                            # 10 oker, 11 geel, 12 lichtgeel
     (214,220,230),(250,251,253)]                                        # 13 snavelwit, 14 glans
G.PAL=PAL; G.CH='.K01234abcoyYwW'
WOLK={2,3,4,5,6}; VOGEL={7,8,9}; GEEL={10,11,12}; WIT={13,14}
# r1 -> r2 indexvertaling (zelfde betekenis, nieuw palet)
R1={0:0,1:1,2:2,3:3,4:4,5:4,6:5,7:6,8:7,9:8,10:9,11:10,12:11,13:12,14:13,15:14}
r1=np.asarray(Image.open('sprite_r1/swablu_r1.png')).astype(int); o=np.vectorize(R1.get)(r1)
start=o.copy()
tel={}
def stap(n,v): tel[n]=tel.get(n,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
# --- 1. toonstemming per spritepixel (modeltonen per natieve pixel) ---
def wolktoon(l): return 6 if l>=188 else 5 if l>=152 else 4 if l>=118 else 3 if l>=86 else 2
def vogeltoon(l): return 9 if l>=145 else 8 if l>=105 else 7
STEM=np.zeros((64,64,15)); FK=np.zeros((64,64)); FD=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        for u,v,w in overlap(X,Y):
            k=c[v,u]
            if k==1: FK[Y,X]+=w
            if k in (1,3) and L[v,u]<70: FD[Y,X]+=w        # donkere lijn (zwart of donkergrijze bultnaad)
            if k==3: STEM[Y,X,wolktoon(L[v,u])]+=w
            elif k==2: STEM[Y,X,vogeltoon(L[v,u])]+=w
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,list(WOLK|VOGEL)))):
    grp=WOLK if o[Y,X] in WOLK else VOGEL
    s=STEM[Y,X]; ks=sorted(grp); t=[s[k] for k in ks]
    if max(t)>0: o[Y,X]=ks[int(np.argmax(t))]
stap('toonstemming (vlakken i.p.v. verloop)',v)
# --- 2. naden tussen de bollen: waar het model een donkere lijn heeft (zwart of donkergrijs, L<70) die door de gemiddelde-kleurregel wegviel.
#        Rug-regel: >=15% lijn en meer lijn dan de buren dwars op de lijn -> zwart als het model daar zwart is, anders wolk diep. Alleen binnen de figuur, niet op de rand. ---
v=o.copy(); fg=o>0
for Y,X in zip(*np.where(np.isin(o,list(WOLK|VOGEL)))):
    if any(not fg[Y+dy,X+dx] for dy,dx in N4): continue
    f=FD[Y,X]
    if f<0.15: continue
    h=f>=FD[Y,X-1] and f>=FD[Y,X+1]; vv=f>=FD[Y-1,X] and f>=FD[Y+1,X]
    if h or vv: o[Y,X]=1 if FK[Y,X]>=0.5*f else 2
stap('naden tussen bollen',v)
