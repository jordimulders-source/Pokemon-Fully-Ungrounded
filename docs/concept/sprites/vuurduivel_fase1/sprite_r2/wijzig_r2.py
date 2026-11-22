# wijzig_r2.py: r2 = r1 + benoemde reparaties (ogen, mond, hoorns) -> raster_r2.txt ; elke pixel met reden
R=[list(r.rstrip('\n')) for r in open('raster_r1.txt')]
E={}
def zet(x,y,c,reden):
    if R[y][x]!=c: E[(x,y)]=(R[y][x],c,reden); R[y][x]=c
# ---- OGEN volgens de Haunter-techniek (Gen 3 anim_front_gba): oogwit als wig onder een schuin zwart lid dat naar het
# midden van het gezicht zakt (= wenkbrauw-V), pupil klein in de binnenste onderhoek van het wit, geen zwarte onderrand.
# Plek, maat en blik uit het model: ver oog wit kol 33-36 / rij 65-68 (sx16-18, sy32-34), pupil rechts;
# nabij oog wit kol 49-57 / rij 63-66 (sx24-28, sy31-33), pupil linksonder; wenkbrauwen schuin naar het midden.
VER={ # x15..19
30:"#m#mm",
31:"###mm",
32:"#W##m",
33:"#WWW#",
34:"#WW#m",
}
for y,r in VER.items():
    for i,c in enumerate(r): zet(15+i,y,c,'ver (linker) oog: Haunter-wig op de modelplek (lid schuin omlaag naar rechts, pupil rechtsonder)')
NAB={ # x23..29
28:"mmm#mmm",
29:"mm#mmmm",
30:"m#mm##m",
31:"mm##WWm",
32:"m#W#WWm",
33:"mm##WWm",
34:"mmddddm",
}
for y,r in NAB.items():
    for i,c in enumerate(r): zet(23+i,y,c,'nabij (rechter) oog: Haunter-wig op de modelplek (lid schuin omlaag naar links, pupil linksonder)')
# ---- MOND: hoektand 2 px wit (model kol 49-50, rij 72-74), donkere rand rondom
zet(24,36,'W','hoektand: wit (model #W/bW)'); zet(24,37,'W','hoektand: punt, 2 px zodat hij leest (model Md, punt rij 74)')
zet(25,36,'#','mondrand boven rechts naast de tand (model Wm/kB -> rand)')
zet(26,38,'#','mondrand rechts (model #m)')
# ---- HOORNS: donkere omlijning tussen hoorn en haar (model: rechterhoorn # rechts, R/b links)
for c,(x,y) in (('#',(26,21)),('#',(25,22)),('p',(26,22)),('#',(27,22)),('#',(24,23)),('p',(25,23)),('r',(26,23)),('#',(27,23)),
                ('#',(24,24)),('p',(25,24)),('r',(26,24)),('#',(27,24)),('R',(25,25)),('r',(26,25)),('R',(27,25))):
    zet(x,y,c,'rechterhoorn: los rood hoorntje, zwarte rand tegen het haar, lichtstreep links (model)')
for c,(x,y) in (('R',(15,22)),('R',(14,23)),('p',(15,23)),('#',(16,23)),('R',(14,24)),('p',(15,24)),('r',(16,24)),('#',(17,24)),
                ('R',(15,25)),('r',(16,25)),('#',(17,25))):
    zet(x,y,c,'linkerhoorn: los rood hoorntje, zwarte rand tegen het haar (model ## rechts van de hoorn)')
open('raster_r2.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
with open('wijzigingen_r2.txt','w') as f:
    for (x,y),(a,b,r) in sorted(E.items(),key=lambda t:(t[0][1],t[0][0])): f.write('(%d,%d) %s->%s  %s\n'%(x,y,a,b,r))
print(len(E),'pixels gewijzigd t.o.v. r1')
