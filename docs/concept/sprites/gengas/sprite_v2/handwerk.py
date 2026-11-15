# Bewuste correcties per pixel (na kwantiseer.py -> gezicht_schuif.py -> ontruis.py), elk met reden.
# Alles wat hier niet staat is de dichtstbijzijnde gemeten tint van de modelpixel.
import sys
R=[list(l.rstrip('\n')) for l in open(sys.argv[1])][:64]
log=[]
def zet(y,x,c,reden):
    if R[y][x]!=c: log.append(f'({y},{x}) {R[y][x]}->{c}  {reden}'); R[y][x]=c
# --- buitenlijn lijf ---
zet(14,21,'a','inkeping oor/kop: donkere lijn van het linkeroor loopt door (model 161,72,95 lag op de rand)')
zet(14,22,'r','selout bovenrand kop sluit aan op rij 13 (r)')
zet(14,38,'a','inkeping tussen kop en rechteroor: lijn volgt de V (model-lijn rij 13 = a)')
zet(14,39,'a','idem')
for y,x in ((22,11),(23,10),(24,10),(25,9)):
    zet(y,x,'K','gat in de linker omlijning (model 68-84 lum, bijna zwart) tussen K-stukken rij 16-21 en 26+')
zet(52,15,'K','onderrand linksonder: middentint op de buitenrand -> omlijning (schaduwkant)')
zet(53,16,'K','idem, sluit trap 53,15 -> 54,18')
zet(53,17,'K','idem')
zet(56,40,'K','linkerrand rechteronder-maan: donkerlila op de rand tussen K')
zet(10,32,'.','los omlijningsstaartje onder de bovenste maan (1 px, nergens aan vast behalve 9,32)')
# --- gezicht (na het schuiven) ---
zet(29,14,'b','meegeschoven randselout van de oude plek: los in het masker')
zet(35,26,'R','lichtroze ruispixel midden in het rechteroog')
zet(31,24,'m','gedempte punt van de lichte wig tussen de ogen (model 153-159,88-90,105-109; v was te fel)')
zet(31,25,'m','idem')
# rechteroog: het model heeft hier geen pupil, Gengar wel (het linkeroog van het model ook). Gengars pupil
# (2 px naast elkaar + 1 eronder rechts) aan de binnenkant van het oog, direct onder het eind van de wenkbrauw.
zet(34,27,'K','pupil rechteroog (Gengar-vorm)')
zet(34,28,'K','pupil rechteroog (Gengar-vorm)')
zet(35,28,'K','pupil rechteroog (Gengar-vorm)')
# grijns: bovenlip linksboven liep K-a-K-a om en om; Gengar: lip donker, uiteinden zwart -> eind van de lip één
# doorlopende zwarte diagonaal (2:1), tandschaduw aan de punt één tint (H) i.p.v. G/H/h door elkaar.
zet(38,14,'K','bovenlip linkerpunt: doorlopende lijn')
zet(39,16,'K','bovenlip: geen a/K om en om')
zet(40,18,'K','bovenlip: geen a/K om en om (was tandgrijs G)')
zet(39,14,'H','tandschaduw linkerpunt: één tint')
zet(40,16,'H','tandschaduw: één tint')
zet(39,30,'H','tandschaduw rechterpunt: één tint')
# --- manen: buitenlijn. Lichtkant (boven/links) mag grijze selout g houden zoals het model; lichtere grijzen op de
# rand worden g; schaduwkant (onder/rechts) wordt K.
zet(43,2,'g','linkermaan: lichtgrijs op de buitenrand -> selout')
zet(41,7,'g','linkermaan: wit op de buitenrand -> selout')
zet(49,2,'K','linkermaan onderkant: schaduwkant')
for y in (24,25,26): zet(y,62,'K','rechtermaan rechterrand: schaduwkant')
zet(51,50,'g','rechteronder-maan bovenrand: selout'); zet(51,52,'g','idem')
zet(59,41,'K','rechteronder-maan linksonder: schaduwkant')
zet(59,49,'K','rechteronder-maan onderrand tussen de tenen')
for x in (29,30,31): zet(0,x,'g','bovenste maan bovenrand: model donkergrijs (83-86) -> selout g')
zet(1,32,'g','idem'); zet(4,27,'g','bovenste maan linkerrand: selout'); zet(5,25,'g','idem'); zet(8,28,'g','idem onderrand'); zet(9,30,'g','idem')
zet(2,33,'g','bovenste maan: lichtgrijs/glans op de bovenrand -> selout'); zet(2,34,'g','idem'); zet(5,26,'g','glans op de rand -> selout g')
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
open(sys.argv[2]+'.log','w').write('\n'.join(log)+'\n'); print(len(log),'correcties')
