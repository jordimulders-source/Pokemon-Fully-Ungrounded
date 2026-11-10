# ronde 2: alleen de benoemde reparaties (1 gezicht, 2 snor, 3 tinten zwarte massa links); draait op raster.txt van r1
R=[list(l.ljust(64,'.')) for l in open('../kleur_r1/raster.txt').read().split('\n')[:64]]
def put(y,x,s):
    for i,ch in enumerate(s):
        if ch!='_': R[y][x+i]=ch
# 1. nabij oog: hoge gebogen bovenrand (boog r13-15), wit vlak, pupil op de modelplek (34,17), zwaar lid rechts
put(13,31,"bdddb")          # x31-35
put(14,31,"d___d")          # zijkanten boog
put(15,32,"oocccd")         # bovenrand links hoog, x37 = d
put(16,32,"owwood")         # wit + lid naar rechts omlaag
put(17,32,"dwowwo")        # wit | pupil | wit wit | ooghoek
put(18,32,"bccccd")
# verre oog: zwaar lid (2 px zwart), pupil + wit eronder, half dicht
put(15,38,"bdc"); put(16,38,"doo"); put(17,38,"cow"); put(18,38,"cdd")
# 2. snor: linkerkrul met grijs binnenin, dunne band (links 2 px, rechts 1 px) die naar rechts oploopt
put(18,30,"oo")
put(19,28,"cobo"); put(19,32,"bbbccdcc")      # (38,19) d = lijn langs de snuit
put(20,29,"bob"); put(20,32,"bbbcccdcc"); put(20,41,"co")
put(21,29,"obnnnnccckkkko")                   # x29-42
put(22,29,"oommmmmmmcccc"); put(22,42,"oooo")  # x29-41 + staart 42-45
# mond: scheve glimlach onder de snor, omlaag naar rechts, eind omhoog; kin eronder
put(23,30,"occccod"); put(23,37,"ccbbcdo")    # x30-36, 37-43
put(24,36,"ooooodo")                          # x36-42 ; (41,24) d = mondhoek omhoog
put(23,41,"d")
put(25,36,"occddo")                           # x36-41
# 3. zwarte massa links: plaat lichtst, bovenarm middel, rug/zijkant donker
put(19,17,"npnn")
put(20,15,"npppnnn")
put(21,14,"npppnnnnnm")
put(22,14,"nppnnnnnmm")
put(23,13,"mnnnnnnnnmm")
put(24,13,"mnnnnnnmmmk")
put(25,13,"mmnnnnmmmkk")
put(26,14,"kmmmmmmkk")
for y in range(21,39):
    for x in range(10,29):
        inplaat=((x-18.5)/6.3)**2+((y-23)/5.1)**2<=1.0 and y<=26
        inarm=12<=x<=19 and 28<=y<=33
        if not inplaat and not inarm and R[y][x] in 'mn': R[y][x]='k'
# lichte rand (m) aan de lichtkant van rug en zijkant
put(34,12,"mmmmm"); put(35,12,"m"); put(36,13,"m")
put(31,20,"m"); put(28,21,"m"); put(29,21,"m"); put(30,20,"m")
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
