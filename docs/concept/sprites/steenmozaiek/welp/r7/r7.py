# Ronde 7: gerichte reparaties uit r6/keuring.md op basis van welp_r6. Alleen benoemde pixelbewerkingen;
# coordinaten hier in spriteraster 50x45 (keuring gebruikt 64x64: x+7, y+18). Per zone diff t.o.v. r6 gelogd.
import numpy as np
r6=np.load('welp_r6.npy'); r5=np.load('welp_r5.npy'); H,W=r6.shape
CH='.KdSMLPQRgWCTGHU'; IX={c:i for i,c in enumerate(CH)}
a=r6.copy(); log={}
def zet(naam,pix,c):
    n=0
    for x,y in pix:
        v=IX[c]
        if a[y,x]!=v: a[y,x]=v; n+=1
    log[naam]=log.get(naam,0)+n

# MOET 2 neus: volle donkere neus (K-bovenrij, d-vulling, 1 px glans G), losse K (tip/philtrum) weg
zet('neus',[(2,14),(3,14),(4,14)],'d'); zet('neus',[(3,13)],'G')
zet('neus',[(4,15),(4,16)],'M')
# MAG linkerrand kop: een lijntype (d) op de lichte kant
zet('linkerrand_d',[(3,9),(3,10),(1,14),(2,16),(3,17)],'d')
# MOET 3 oog: rondom omlijnd, onderrand y12, iris grijsbeige (g/G, niet het creme C)
zet('oog',[(10,10),(10,11),(11,11),(12,11)],'g'); zet('oog',[(9,11),(13,11),(10,12),(11,12),(12,12)],'d')
# MOET 4 tong: tweede roze U (rand links/onder, middengroef x6), ronde punt
zet('tong',[(5,19),(6,19),(6,20),(4,21),(6,21),(6,22)],'U'); zet('tong',[(5,20),(5,21),(5,22),(7,19),(7,20)],'T')
# MOET 5 korrels kop
zet('korrels_kop',[(8,8)],'L'); zet('korrels_kop',[(4,11)],'H'); zet('korrels_kop',[(6,12)],'M')
# MOET 5 korrels lijf
zet('korrels_lijf',[(28,15),(29,16),(30,17),(31,18)],'S')           # rugstreepje M/S om en om -> S
zet('korrels_lijf',[(11,20)],'d')                                     # mondholte
zet('korrels_lijf',[(27,21),(28,22),(28,23),(28,24),(28,25)],'M')    # spleet creme/lila schouderspiraal: een tint
zet('korrels_lijf',[(40,28)],'d'); zet('korrels_lijf',[(39,29),(40,30)],'M')  # dijrand
# staartaanzet / dijring (x38-46, y33-38): lila ring doorlopend, dijcontour d, staartbasis M/S, ring creme+lila
zet('staartaanzet',[(39,36),(40,35),(41,34),(41,33)],'R')
zet('staartaanzet',[(39,35),(39,34),(40,34)],'M')
zet('staartaanzet',[(42,34),(42,35),(42,36),(42,37),(42,38)],'d')
zet('staartaanzet',[(41,35),(41,36),(41,37),(40,36),(39,37),(40,37),(39,38),(40,38),(41,38)],'S')
zet('staartaanzet',[(43,36),(44,36)],'M'); zet('staartaanzet',[(43,37),(44,37),(45,37),(43,38),(44,38),(45,38)],'S')
# MOET 6 spiraallijnen doorlopend
zet('spiralen',[(21,20),(25,20),(26,20)],'R')          # bovenrand lila ring dicht
zet('spiralen',[(17,23)],'C')                          # creme boog links aaneen
zet('spiralen',[(20,28),(21,29)],'M')                  # losse lila stippen onder de ring
# fout uit r6 hersteld: beenlijnen (r5 lijnbruin) waren door een commentaarfout weggevallen
zet('beenlijnen_terug',[(19,y) for y in range(32,37) if r5[y,19]==2]+[(27,y) for y in range(32,40) if r5[y,27]==2],'d')
# MAG voorhoofdsband rechts 2 px doortrekken (bocht naar het oor)
zet('band_rechts',[(15,3),(16,4)],'R')
# MAG teenpixels consequent (elke teen >= 2 px)
zet('tenen',[(17,43),(20,43),(16,43),(18,43),(19,43),(21,43)],'M'); zet('tenen',[(20,41)],'d')
zet('tenen',[(31,41)],'L'); zet('tenen',[(31,42)],'M')
# restkorrels na de reparaties (eigen controle met korrel.py)
zet('restkorrels',[(13,12),(26,32),(22,43)],'M')
np.save('welp_r7.npy',a)
if __name__=='__main__':
    print(log,'totaal diff r6:',int((a!=r6).sum()),'silhouet-diff:',int(((a>0)!=(r6>0)).sum()))
