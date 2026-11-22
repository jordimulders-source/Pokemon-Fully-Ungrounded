# wijzig_r5.py [OOGVARIANT]: r5 = r3 + glimpje (Jordi) + keurder-MOET 1-6 -> raster_r5.txt ; elke pixel met reden in wijzigingen_r5.txt
import sys
V=sys.argv[1] if len(sys.argv)>1 else 'A'
R=[list(r.rstrip('\n')) for r in open('raster_r3.txt')]
E={}
def zet(x,y,c,reden):
    if R[y][x]!=c: E[(x,y)]=(R[y][x],c,reden); R[y][x]=c
def blok(x0,rijen,reden):
    for y,r in rijen.items():
        for i,c in enumerate(r):
            if c!='?': zet(x0+i,y,c,reden)

# ---- MOET 1 + Jordi: ogen ----
if V=='A':
    # linkeroog x15..19: lid 2 dik schuin omlaag naar de neus (model-wenkbrauw (16,29.5)->(19,32)), oogwit-amandel 3 px
    # onder het lid aan de buitenkant, pupil 2x2 aan de neuskant, glimpje rechtsonder (18,34) (Jordi)
    blok(15,{30:"##mmm",
             31:"####m",
             32:"#WW##",
             33:"#W##m",
             34:"#d#Wm"},'linkeroog: V-lid + amandel (model), glimpje onderhoek')
    # rechteroog x23..29: lid = model-wenkbrauw (26,28)->(23,31) + lidlijn boven het wit (model rij 31.0), wit-amandel
    # (26-28,32)+(27,33) (model), pupil aan de neuskant met glimpje linksonder (24,33) (= plek van het glimpje in het model)
    blok(23,{28:"mmmmmmm",
             29:"mm##mmm",
             30:"m##mmmm",
             31:"#####mm",
             32:"m##WWWm",
             33:"mW##WWm",
             34:"mdddddm"},'rechteroog: V-lid + amandel (model), glimpje onderhoek')
if V=='B':
    blok(23,{28:"mmm#mmm",
             29:"mm##mmm",
             30:"m##mmmm",
             31:"#####mm",
             32:"m##WWWm",
             33:"m#W#Wmm",
             34:"mdddddm"},'rechteroog: V-lid + amandel (model), glimpje binnen de pupil')
    blok(15,{30:"##mmm",
             31:"####m",
             32:"#WW##",
             33:"#W##m",
             34:"#d#Wm"},'linkeroog')

# glimpjes ingesloten: pupil 1 px groter in donkere vlaktint d, zodat het wit als glimpje IN de pupil leest (Jordi: "het moet een oog zijn")
zet(23,33,'d','rechteroog: pupil 1 px groter (d) links van het glimpje; model heeft daar zwart op 33.0 x24a')
zet(19,34,'d','linkeroog: pupil 1 px groter (d) rechts van het glimpje; model heeft zwart op 33.1 x19a en 34.1 x18b')
# ---- MOET 2: mond. Bovenrand, D-vorm met U-onderkant staan al op modelmaat (gemeten: rij 37 6 breed, 38 5, 39 3,
# zijkanten diagonaal zoals het model). Linker mondhoek omhoog: het lachkuiltje van het model (35.0, x19b) ----
zet(19,35,'#','mond: lachkuiltje/linker mondhoek omhoog (model: zwart op 35.0 x19b)')
zet(20,35,'m','KAN: losse l-pixel op de wang weg (model: dat lichte pixel hoort bij het kuiltje, op 1x ruis)')
# ---- MOET 3: tanden. Gemeten in het model: grote tand RECHTS (x24b-25a, y36-37, ±11x9 modelpx), klein tandje links
# (x19b-20a, y37, ±8x8 modelpx). r3 volgt het model al: (24,36-37) groot, (20,37) klein. Model wint van de keurder. ----
zet(25,37,'R','mond: mondinterieur rechts naast de tand donkerrood zoals het model (37.x x25: R) i.p.v. losse r')
# ---- MOET 4: hoorns, eigen hoornrood H + hoornlicht h (modelkleuren bb2d2e / e8645f), zwart aan de haarkant
# (schaduwkant), donkerrood R aan de lichtkant (model), punt omhoog ----
blok(14,{22:".R",
         23:"Rh#",
         24:"RhH#",
         25:"?RhH#",
         26:"?#HH#",
         27:"??##d"},'linkerhoorn: model-kegel, punt (15,22), hoornrood/hoornlicht, zwart aan de haarkant')
blok(24,{21:"??#",
         22:"?Rh#",
         23:"RhH#",
         24:"#hHH#",
         25:"#HHH#",
         26:"#HHH#",
         27:"m###m"},'rechterhoorn: model-kegel 3 breed aan de voet, punt (26,21) boven de haarrand, hoornrood/hoornlicht, zwarte rand rechts en onder, R links')
# ---- MOET 5: haar ----
zet(20,19,'R','haarrand: zwart tussen donkerrood -> donkerrood')
zet(34,27,'O','haar rechts: vlamtong 2 loopt door naar linksonder zoals het model (34-35,26.5-27.5)')
zet(35,27,'O','haar rechts: vlamtong 2 samenhangend (model)')
zet(36,27,'r','haar rechts: rode schaduw tussen tong 2 en 3 (model), geen O-r-O-dambord')
# ---- MOET 6: staartpunt onderkant: twee lobben met schone donkerrode onderrand, stam komt aan in de inkeping (46,45) ----
blok(42,{43:"RrOrrrrrR",
         44:".RrrRrrR.",
         45:"..RR#RR..",
         46:"...##....",
         47:"..##.....",},'staartpunt: schone R-onderrand van beide lobben, inkeping (46,44-45), stam erin')
open('raster_r5.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
with open('wijzigingen_r5.txt','w') as f:
    for (x,y),(a,b,r) in sorted(E.items(),key=lambda t:(t[0][1],t[0][0])): f.write('(%d,%d) %s->%s  %s\n'%(x,y,a,b,r))
print(len(E),'pixels gewijzigd t.o.v. r3')
