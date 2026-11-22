# wijzig_r3.py: r3 = r2 + gezicht (ogen, leden, mond) -> raster_r3.txt ; elke pixel met reden in wijzigingen_r3.txt
R=[list(r.rstrip('\n')) for r in open('raster_r2.txt')]
E={}
def zet(x,y,c,reden):
    if R[y][x]!=c: E[(x,y)]=(R[y][x],c,reden); R[y][x]=c
def blok(x0,rijen,reden):
    for y,r in rijen.items():
        for i,c in enumerate(r): zet(x0+i,y,c,reden)
# LINKER (verre) oog x15..19: dik schuin lid omlaag naar de neus (rechts), wit als halvemaan links, pupil 2x2 rechts in het wit
blok(15,{30:"#mmmm",
         31:"####m",
         32:"#WW##",
         33:"#W##m",
         34:"#W##m"},'linkeroog: Haunter-techniek, lid 2 dik schuin naar de neus, pupil 2x2 rechts in het wit (model: pupil kol 35-36 rechts)')
# RECHTER (nabij) oog x23..29: dik schuin lid omlaag naar de neus (links), wit halvemaan, pupil 2x2 aan de binnenkant
blok(23,{28:"mmmmmmm",
         29:"mmmm##m",
         30:"m#####m",
         31:"m##WWWm",
         32:"m###WWm",
         33:"mm##WWm",
         34:"mmddddm"},'rechteroog: Haunter-techniek, lid 2 dik schuin naar de neus, pupil 2x2 binnenkant in het wit (model: pupil kol 50-53)')
# MOND x17..27, y35..39 op modelmaat (natief: mondhoek links sx18 y36, rechts sx26 y35, tong sx21-25 y38-39,
# hoektand sx24 y36-37, tandje sx20 y37); '?' = laten staan
def blokq(x0,rijen,reden):
    for y,r in rijen.items():
        for i,c in enumerate(r):
            if c!='?': zet(x0+i,y,c,reden)
blokq(17,{35:"?????????#?",
          36:"?######W##?",
          37:"??#WrrrWr#?",
          38:"???#rpppp#?",
          39:"????#ppp#??"},'mond: open lachende mond op modelmaat, mondhoeken omhoog (18,36) en (26,35), zwarte rand, binnenkant rood i.p.v. donkerbruin zodat hij leest')
zet(26,27,'d','lijn onder de rechterhoorn: werd een losse zwarte pixel na het weghalen van de wenkbrauwpixel (26,28); donkere vlaktint (model ##)')
open('raster_r3.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
with open('wijzigingen_r3.txt','w') as f:
    for (x,y),(a,b,r) in sorted(E.items(),key=lambda t:(t[0][1],t[0][0])): f.write('(%d,%d) %s->%s  %s\n'%(x,y,a,b,r))
print(len(E),'pixels gewijzigd t.o.v. r2')
