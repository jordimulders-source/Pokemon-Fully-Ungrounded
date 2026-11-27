# Ronde 2 = r1 met alleen benoemde reparaties (NOTITIES). Gebruik vanuit sneeuwmonster_fase3: python3 sprite_r2/bouw.py
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from gemeen import label
o=np.asarray(Image.open('sprite_r1/sauna_yeti_r1.png')).astype(int).copy(); r1=o.copy(); log=[]
def zet(X,Y,t,why):
    if o[Y,X]!=t: log.append((X,Y,CH[o[Y,X]]+'>'+CH[t],why)); o[Y,X]=t
# G1 wenkbrauwlijn (model y190-202 -> rij 22) direct boven de oogleden (rij 23): lijntint -> s, zodat lid en pupil
#    loskomen van de wenkbrauw (zelfde plek, lichtere tint; het model tekent de vachtlijnen lichter dan de oogleden).
for X in range(25,38):
    if o[22,X]==2: zet(X,22,3,'G1')
# G2 rij 23 buiten de oogleden (wangvacht naast het gezicht, X24-25 en X37-38): lijntint -> s
for X in (24,25,37,38):
    if o[23,X]==2: zet(X,23,3,'G2')
# Z1 losse zwarte pixels (binnenlijn-stukjes uit de lijnoverdracht, raken geen andere zwarte pixel of de rand) -> lijntint;
#    stenen en gezicht uitgezonderd.
fg=o>0
for Y,X in zip(*np.where(o==1)):
    if 20<=Y<30 and 24<=X<40: continue
    nb=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    if any(v in (13,14,15) for v in nb): continue
    if all(v not in (0,1) for v in nb): zet(X,Y,2,'Z1')
# S1 steenrand: gloeit waar het model >=40 % gloed heeft (r1: 50 %); zelfde drempel als de scheuren binnenin.
#    Kleine buiksteentjes lazen op 1x als zwarte vlekjes met alleen een oranje onderrand; het model heeft een gloeirand
#    rondom behalve linksboven. Gloedaandeel blijft onder ±30 %.
from klassen import klassen
a,c,L=klassen(); idx=spriteindex(); ok=idx>=0; I=idx[ok]; cu=up(c)[ok]; n=np.maximum(np.bincount(I,minlength=4096),1)
gf=(np.bincount(I,np.isin(cu,[6,7]).astype(float),minlength=4096)/n).reshape(64,64)
stf=(np.bincount(I,np.isin(cu,[5,6,7]).astype(float),minlength=4096)/n).reshape(64,64)
st=(stf>=0.45)&fg
for Y,X in zip(*np.where(st&(o==1))):
    if gf[Y,X]>=0.40: zet(X,Y,14,'S1')
print('gloed/steen',np.isin(o,[14,15])[st].sum(),'/',st.sum())
opslaan(o,'sprite_r2/sauna_yeti_r2.png')
print('r1->r2',(o!=r1).sum(),'px'); [print(l) for l in log]
