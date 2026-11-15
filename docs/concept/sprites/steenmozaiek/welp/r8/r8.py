# Ronde 8: gerichte reparaties uit r7/keuring.md op basis van welp_r7 (spritecoordinaten 50x45; keuring 64x64: x+7, y+18).
import numpy as np, sys
r7=np.load('welp_r7.npy'); H,W=r7.shape
CH='.KdSMLPQRgWCTGHU'; IX={c:i for i,c in enumerate(CH)}
a=r7.copy(); log={}
def zet(naam,pix,c):
    n=0
    for x,y in pix:
        if a[y,x]!=IX[c]: a[y,x]=IX[c]; n+=1
    log[naam]=log.get(naam,0)+n
OOG=sys.argv[1] if len(sys.argv)>1 else 'B'   # B gekozen uit A/B/C (open, alert; sclera rechts wit)
# MOET 1 neus als driehoek: y13 x2-6, y14 x3-5, y15 x4 (punt omlaag); snuitrand (1,14) weg, rand (2,14) in S
zet('neus',[(2,13),(3,13),(4,13),(5,13),(3,14),(4,14),(4,15)],'d'); zet('neus',[(6,13),(5,14)],'K')
zet('neus',[(1,14)],'.'); zet('neus',[(2,14)],'S')
# MOET 2 voorhoofdsband rechtereinde gaaf
zet('band_einde',[(14,3),(15,3),(13,4),(14,4)],'R'); zet('band_einde',[(16,4)],'L')
# MOET 3 tenen opgeheven poot: teenlijnen x3 en x6 (y25-26), tenen x1-2, x4-5, x7-8 in L
zet('tenen_poot',[(3,25),(3,26),(6,25),(6,26)],'d'); zet('tenen_poot',[(1,25),(2,25),(4,25),(5,25),(7,25),(8,25),(1,26),(2,26),(4,26),(5,26),(7,26),(8,26)],'L')
# MOET 4 tong linkerrand een randsoort (d)
zet('tong_rand',[(4,21)],'d')
# MOET 5 elleboog: brede vlakke onderkant (rij 32 vulling S, rij 33 buitenlijn x10-14), rechts aan de lijn x15
zet('elleboog',[(10,32),(11,32),(12,32),(13,32),(14,32),(15,31)],'S'); zet('elleboog',[(9,32),(15,32),(10,33),(11,33),(12,33),(13,33),(14,33)],'K')
# MAG oog: open en alert (iris boven licht i.p.v. schaduw, lid alleen boven de pupil zwart, uiteinden lijnbruin); resterende C-iris -> g
zet('oog',[(12,10)],'g')
if OOG in 'AB': zet('oog',[(12,9)],'g'); zet('oog',[(10,8),(13,8)],'d')
if OOG=='B': zet('oog',[(13,9)],'W')
# MAG rug: lila tot de buitenlijn (geen dubbele rand)
zet('rug',[(28,15),(29,16),(30,17),(31,18)],'R')
# MAG staart: ring dwars over de staartbasis (creme x45 y35-38, lila x46 y36-37), rechterkolom middenbruin
zet('staart',[(45,35),(45,36),(45,37),(45,38)],'C'); zet('staart',[(46,36),(46,37)],'Q'); zet('staart',[(48,32),(48,33),(48,34),(48,35)],'M')
# MAG spiralen: losse lila in schouderspiraal weg; dijspiraal met binnenarm (37-39,33), losse c weg
zet('spiralen',[(23,23)],'M'); zet('spiralen',[(38,33)],'C'); zet('spiralen',[(38,34)],'S')
zet('restkorrel',[(8,24)],'L')   # teen x7-8 doorlopend
np.save('welp_r8.npy',a)
print(OOG,log,'totaal diff r7:',int((a!=r7).sum()),'silhouet-diff:',int(((a>0)!=(r7>0)).sum()))
