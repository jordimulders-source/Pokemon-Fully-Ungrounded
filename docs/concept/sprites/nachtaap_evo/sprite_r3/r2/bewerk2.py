# r2: alleen tinten binnen bestaande vlakken (silhouet en kop bevroren). Elke wijziging gelogd met zone.
import sys; sys.path.insert(0,'r1'); from pal import *
r1=np.load('r1/r1.npy'); g=r1.copy(); log=[]
def zet(x,y,v,zone):
    assert g[y,x]!=0, (x,y)                       # nooit buiten het silhouet
    if g[y,x]!=v: log.append((zone,x,y,int(g[y,x]),v)); g[y,x]=v
def KOP(x,y): return x<=24 and y>=33 and y<=55     # kop vanaf de nek omhoog: bevroren

# 1) schaduwsikkel langs de rechterkant (achterste deel): 4 -> 3 op de 2 (y37-43) / 3 (y44-53) pixels binnen de rechterlijn
for y in range(37,54):
    xs=np.where(g[y]>0)[0]; xr=xs.max()
    k=2 if y<44 else 3
    for x in range(xr-k,xr):
        if g[y,x]==4: zet(x,y,3,'sikkel rechts')
# 2) rug->staartaanzet rustiger
zet(41,35,6,'staartaanzet')            # losse 3 in het lavendel vlakje -> 6: een vlakje (41-43,34-35)
for (x,y,v) in [(47,33,3),(48,33,3),(46,34,4),(47,34,3),(45,35,4),(46,35,3),(47,35,3),(46,36,3)]:
    zet(x,y,v,'staartaanzet')          # staartvoet: licht links (5/4), schaduw 3 rechts, zoals de staart erboven (y32: 5 4 4 3 3); lijnpixels 2 binnen de staart weg

# 3) achterpoot: een tint donkerder dan de nabije voorpoot (die heeft 5 bovenaan / 4), dijvolume alleen met tint:
#    bovenkant van de dij 4 (licht), onderkant 3 (schaduw onder, sluit aan op de sikkel rechts). Geen vormwijziging.
zet(38,47,4,'achterpoot')               # losse 5 (model) -> 4: de achterpoot krijgt geen 5
for x in range(37,43):
    if g[49,x]==4: zet(x,49,3,'achterpoot')
for (x,y) in [(38,50),(39,50),(40,50),(41,50),(38,51),(39,51),(40,51)]: zet(x,y,3,'achterpoot')
# 4) licht/volume lijf (zoals de oude sprite): lichtste lijftint 5 linksboven op de rugbult, 4 op de flank,
#    sikkel 3 rechts/achter; tintgrenzen zijn cirkelbogen rond het lichtpunt (21,30) (y x1,3), dus ze volgen de bult.
#    Alleen pixels die 4 of 5 zijn, niet in kop, staart, nabije voorpoot of achterpoot.
sys.path.insert(0,'r2'); from proef import licht
lg=[]; licht(g,21,30,10,24,lg); log+=lg

# 5) grens schaduw boven de dij afgerond (was een rechte rand y43/44 over x39-43): sikkel buigt terug om de dij
zet(39,43,4,'achterpoot'); zet(40,43,4,'achterpoot'); zet(43,44,3,'achterpoot')

if __name__=='__main__':
    sys.path.insert(0,'r2'); from export import export
    export(g,r1,log)
    if '-v' in sys.argv:
        for z,x,y,o,n in log: print(z,(x,y),S[o],'->',S[n])
