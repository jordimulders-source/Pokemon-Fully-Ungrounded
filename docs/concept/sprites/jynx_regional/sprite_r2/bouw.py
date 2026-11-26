# Regionale Jynx r2: r1 + benoemde reparaties uit sprite_r1/KEURING.md (coördinator, ronde 2). Silhouet-diff 0.
# Niets hertekend: strengpaden en lijnen uit het model (natieve modelpixels naar spritecoördinaten), tinten op bestaande vormen.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from gemeen import *
import gemeen
r1=np.asarray(Image.open('sprite_r1/jynx_regional_r1.png')).astype(int); o=r1.copy()
UIT='sprite_r2'
# palet: klauwen (15) -> haar donker (6); plek 15 = lichte haartint
PAL2=list(PAL); PAL2[15]=(200,154,104); gemeen.PAL[:]=PAL2
tel={}
def stap(n,v): tel[n]=int((v!=o).sum())
def zet(lst,k):
    for X,Y in lst: o[Y,X]=k

# --- 0. klauwen -> haar donker (paletplek vrij; oog blijft) ---
v=o.copy(); o[o==15]=6; stap('klauwen naar haar donker',v)

# --- 2. haar rechtsboven (x40-46, y11-18): één doorlopende strenglijn op het modelpad (natief (61,19)->(65,26):
#        sprite (41,11)->(43,16)), schaduw rechts ernaast, links middentint. Rij 17-18 en lager (donker achterhaar) = r1. ---
v=o.copy()
rijen={11:{40:8,41:6,42:7},12:{40:8,41:8,42:6,43:7},13:{40:8,41:8,42:6,43:7},
       14:{39:8,40:8,41:8,42:8,43:6,44:7},15:{39:8,40:8,41:8,42:8,43:6,44:7},16:{40:8,41:8,42:8,43:6,44:7}}
for Y,r in rijen.items():
    for X,k in r.items(): o[Y,X]=k
stap('haar rechtsboven (streng)',v)

# --- 1. haarvolume. a) kruinstreng uit het model (natief (53,14)->(57,20), de reductie hield alleen het onderste stuk als S/D):
#        doorlopende lijn (34,7)->(37,13), schaduw rechts ernaast. b) lichte tint per lok aan de linkerbovenkant. ---
v=o.copy()
zet([(34,7),(34,8),(35,9),(36,10),(36,11),(37,12),(37,13)],6)
zet([(35,8),(36,9),(37,10),(37,11),(38,12),(38,13)],7)
LICHT=[# kruin links van de scheiding: boog over de bolling
       (24,8),(23,8),(22,8),(21,9),(20,10),
       # kruin rechts van de scheiding: één boog die de lok volgt (van de scheiding over de bolling naar de
       # voorlok naast het gezicht), in het midden 2 px dik, smal aan de uiteinden
       (26,8),(27,8),(28,8),(29,7),(30,7),(31,7),(29,8),(30,8),(31,8),(32,8),(32,9),(33,10),(33,11),
       # linkerlok (2 px breed) waar hij van de kruin over de schouder buigt: binnenste kolom, zodat er
       # middentint tussen licht en buitenlijn blijft (geen band langs de buitenlijn)
       (17,15),(17,16),(17,17),(16,18)]
zet(LICHT,15)
stap('haarvolume',v)

# --- 3. linkervleugel bovenrand: zwart -> veerlijn (lichtkant) ---
v=o.copy(); zet([(9,17),(10,17)],2); stap('vleugelrand',v)

# --- 4. onderlip naar het model (dekking: rij 23 donker x20/x22-23, midden x21/x24; rij 24 donker x21-24; rij 25 wit):
#        ring donker langs onder en rechts, midden als één band onder de mondopening; (25,23) lijn. ---
v=o.copy()
zet([(20,23),(25,23),(21,24),(22,24),(23,24),(24,24)],11)
zet([(21,23),(22,23),(23,23),(24,23)],12)
o[25,22]=10
stap('onderlip',v)

# --- 5. rokvouwlijn x33-48 y46-49: één doorlopende 1-px lijn op rij 47 (modelpunten x34-46 op rij 46-48), einde (47,48)->(48,49);
#        kruisende vouwen B (x40) en C (x44) 1 px; gaatjes/dubbele lijnpixels -> vlak van de buren. ---
v=o.copy()
zet([(x,47) for x in range(33,47)]+[(47,48)],2)
o[46,39]=4; o[46,41]=5; o[46,45]=5
o[48,38]=4; o[48,39]=4; o[48,46]=3; o[48,48]=3
stap('rokvouwlijn',v)

# --- 6. rechterrokpaneel (x35-47, y34-46; model maar 9 helderheid lichter dan het rokmidden): licht alleen langs de
#        bovenrand onder de arm (kolommen x35-40: bovenste 2 lichte pixels, x40 1), de rest midden. Vorm = r1. ---
v=o.copy(); b=o.copy()
for X in range(35,48):
    ys=[Y for Y in range(34,47) if b[Y,X]==5]
    houd=set(ys[:2]) if X<=39 else set(ys[:1]) if X==40 else set()
    for Y in ys:
        if Y not in houd: o[Y,X]=4
stap('rechterrokpaneel',v)

assert ((o>0)==(r1>0)).all(), 'silhouet gewijzigd'
NAAM=UIT+'/jynx_regional_r2.png'; opslaan(o,NAAM)
toon(o,4,52,4,60)
print('stappen',tel,'| totaal anders dan r1: %d px'%(o!=r1).sum(),'| kleuren',len(set(o.ravel()))-1)
