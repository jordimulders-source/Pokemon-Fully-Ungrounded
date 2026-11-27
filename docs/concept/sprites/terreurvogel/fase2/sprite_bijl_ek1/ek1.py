# Eindkeuring ek1 (Dragonfly Cave: schaduw + belijning + kleurtinten) op ../sprite_bijl_r4/terreurvogel_bijl_r4.png.
# Alleen uitvoering: silhouet, oog B, onderdelen en kleurkeuze bevroren (met check bewezen).
import numpy as np; from PIL import Image
SRC='../sprite_bijl_r4/terreurvogel_bijl_r4.png'
B0=Image.open(SRC); B=np.array(B0).astype(int); S=B.copy(); PAL=B0.getpalette()[:48]
CH='.#WSmlDAHrRtOpPq'; IX={c:i for i,c in enumerate(CH)}
OOG={(29,17),(29,18),(30,14),(30,15),(30,16),(30,17),(30,18),(31,15),(31,16),(31,17),(31,18),(32,16),(32,17)}
LOG=[]
def zet(zone,cells,c):
    for (y,x) in cells:
        assert (y,x) not in OOG and B[y,x]>0, (y,x)
        if S[y,x]!=IX[c]: LOG.append((zone,y,x,CH[S[y,x]],c)); S[y,x]=IX[c]
def rij(zone,y,x0,x1,c): zet(zone,[(y,x) for x in range(x0,x1+1)],c)

# --- snavel (steen): licht als sikkel linksboven (dik in de hoek, taps naar de punt), schaduwsikkel rechtsonder ---
zet('snavel',[(30,5),(31,5),(31,6),(31,7),(32,4)],'l')                     # hoeklicht: band -> sikkel
zet('snavel',[(38,3),(39,3),(40,3)],'m')                                    # band taps naar de punt (1 px)
zet('snavel',[(34,12),(34,13),(35,10),(35,11),(36,8),(36,9),(36,10),(37,6),(37,7),(38,6),
                  (33,13),(34,11),(35,9),(36,7)],'A')  # wig: 1-3-3-4-2-1 breed, niet parallel aan de D-rand  # koele kernschaduw, breed in het midden
# --- kop/kuif: hooglicht als bolling op het voorhoofd i.p.v. alleen een rand-band ---
zet('kop',[(27,15),(28,13),(28,14)],'O')
# --- vleugel: lichte plaat uit het model (licht vlak tot aan de vleugellijn), schaduw als taps sikkel onderaan ---
rij('vleugel',35,36,43,'H'); rij('vleugel',36,34,39,'H')
zet('vleugel',[(33,32),(34,34)],'S')                                        # hooglicht iets voller op de bolling
# --- borst/buik onder de vleugel (r41-45): bolling met hooglicht + schaduwsikkel ---
zet('buik',[(39,26),(40,25),(40,26),(40,27),(41,25),(41,26),(42,25)],'H')
zet('buik',[(40,25),(40,26),(41,25)],'S')                                   # hooglichtkern 3 px
zet('buik',[(44,33),(44,34),(45,28),(45,29),(45,30),(45,31)],'D')          # schaduwsikkel taps naar de borst
# --- slagschaduw onder de vleugellijn: wig (breder in het midden), geen parallelle trapjes ---
zet('slagschaduw',[(41,35),(41,36),(42,37),(42,38),(43,37)],'D')
im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL+[0]*(768-48)); im.save('terreurvogel_ek1.png',transparency=0)
if __name__=='__main__':
    from collections import Counter
    for z,n in Counter(l[0] for l in LOG).items(): print(z,n)
    print('totaal',len(LOG))
