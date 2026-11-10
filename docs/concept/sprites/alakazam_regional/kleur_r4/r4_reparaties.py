# ronde 4: snor als dunne Alakazam-snorhaar (1 px, uit de zijkant van de snuit), stompje, hals; draait op raster van r3
R=[list(l.ljust(64,'.')) for l in open('../kleur_r3/raster.txt').read().split('\n')[:64]]
def put(y,x,s):
    for i,ch in enumerate(s):
        if ch!='_': R[y][x+i]=ch
# 1. snor: band weg, snuitgrijs terug (licht linksboven)
put(21,31,"bbbbccccccd")      # x31-41 (was snorband n/k)
put(22,31,"ooooocccccc")      # linker snorhaar 1 px op y22 x31-35 (model y22-22.5); x36-41 snuit
put(23,35,"coo")              # snorhaar komt onder de snuit vandaan: (36,23),(37,23) (model y23 x36-37.5)
# rechter snorhaar: uit de snuitpunt (42,22) naar de krul: blijft (r22 x42-45, krul ongewijzigd)
# 2. stompje onder de hals = begin van de zwarte arm (bovenrand n, midden m)
put(34,37,"nnn"); put(35,38,"mm")
# 3. hals: schaduw onder de kaak, links licht, rechts schaduw (sluit aan op kin)
put(27,37,"cccd")
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
