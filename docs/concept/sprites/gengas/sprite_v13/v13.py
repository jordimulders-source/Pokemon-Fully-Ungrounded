# v13 = v12 + eindkeuring v12 (EINDKEURING_v12.md MOET 1-5, KEURING_v12.md MOET 1-2, enkele MAG's). Keurder-tintnummers:
# 1=K 2=a 3=b 5=m 6=l b=g e=H. Diff buiten de genoemde pixels en de twee zones (wang x8-15 y37-41, band x31-47 y30-38) = 0.
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
V12=[l.rstrip('\n') for l in open(D+'../sprite_v12/raster.txt')][:64]
R=[list(r) for r in V12]; log=[]; toegestaan=set()
def zet(x,y,c,reden):
    toegestaan.add((x,y))
    if R[y][x]!=c: log.append(f'({x},{y}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
# EINDKEURING MOET 1-5 (1-op-1)
for p in ((14,18),(13,19)): zet(*p,'a','E-MOET1 zwarte binnenlijn lichtkant linkeroor -> a')
for p in ((34,15),(35,15)): zet(*p,'a','E-MOET2 zwart/lila om en om voet rechteroor -> a')
zet(43,53,'g','E-MOET3 maan raakt lijf zonder lijn -> g')
for p in ((32,33),(32,34),(32,35),(31,36)): zet(*p,'m','E-MOET4 contour rechts van het rechteroog')
zet(12,38,'l','E-MOET5 wangvlak één geheel'); zet(15,41,'m','E-MOET5 los l-brokje')
# MAG
for x in (45,46,47): zet(x,50,'K','MAG maan vóór donker lijf: omlijning')
for p in ((26,2),(27,3)): zet(*p,'g','MAG bovenste maan: lichtkant één doorlopende g-lijn (geen K/g om en om)')
# KEURING MOET 2: linkerwang. Plooi ingekort tot 2 px vóór de mondhoek (zoals Gengar (18,33),(19,33) vóór 7 op (19,34)):
# (10,40),(11,40) blijven; de rest van de plooi wordt wangvlak l. Donker randje onder het oog (Gengar d -> b).
for p in ((9,38),(9,39),(10,39),(11,39)): zet(*p,'l','K-MOET2 plooi ingekort, wangvlak')
for p in ((13,39),(14,39),(15,38)): zet(*p,'b','K-MOET2 donker randje onder/naast de onderkant van het oog')
# KEURING MOET 1 + MAG: lichte band begint >=2 px rechts van het oog (m ertussen), linkereinde taps, bovenrand zonder
# bultjes, 1 rij breder (onderaan). Per kolom eerste en laatste l-rij; overige l in de zone -> m.
band={34:(33,34),35:(33,35),36:(32,36),37:(32,36),38:(32,37),39:(32,37),40:(32,37),41:(31,37),42:(31,36),43:(31,36),44:(32,34)}
for y in range(30,39):
    for x in range(31,48):
        if R[y][x] not in 'lm': continue
        c='l' if x in band and band[x][0]<=y<=band[x][1] else 'm'
        zet(x,y,c,'K-MOET1 band los van het oog, taps, glad')
open(D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
def zone(x,y): return (x,y) in toegestaan
print(len(log),'wijzigingen; buiten de genoemde pixels/zones:',sum(1 for y in range(64) for x in range(64) if V12[y][x]!=R[y][x] and not zone(x,y)))
