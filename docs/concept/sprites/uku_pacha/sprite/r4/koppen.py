# Uku Pacha r2: beide koppen per pixel naar het model (puntmonster punt.py + zoom.py naast het model).
# Overschrijft alleen pixels binnen het bestaande silhouet (alpha blijft gelijk; script controleert).
import sys
R=[list(l.rstrip('\n')) for l in open('raster_auto.txt')][:64]
def zet(x0,y0,rows):
    for dy,row in enumerate(rows):
        for dx,c in enumerate(row):
            if c==' ': continue
            y,x=y0+dy,x0+dx
            if (R[y][x]=='.')!=(c=='.'): sys.exit(f'alpha wijkt af op {x},{y}: {R[y][x]}->{c}')
            R[y][x]=c
# linkerkop: open bek, tong, tanden, oog (cols 0-22, rij 9-27)
zet(0,9,[
"..............DDDDDD...",
".......DDDDDDDDBhhBBDDD",
"......DBhhhhBBBBssBBBBB",
".....DhhhhBBBBBDBBBBnss",
"....DhhhhshBBBBBBBBBBns",
"...DhBhhBhBBBsBBBBBBBns",
"..DBhhhsbBKKsBBBBBBsnns",
"..DBhhBhBKWKshhBBmsndds",
"..DBBBnBKpWshBBmmmnbbbn",
"DDBBBhhnsbhhBBDmmmnbbnb",
"KhhhhhmmmmmmKKmmmnbbnnb",
"KKhBKmmmsKKKPKmmKKKKKbb",
".KKKmmKKKPPPPmmK.....Kb",
".KpKKKKWKPPPKmK......KK",
"..K..KKWPPPsmK........K",
".....KPPKsKmK.........K",
"....KPKKKKKK..........K",
"...PKP................K",
"....KP...............Kb",
])
# rechterkop: dichte bek; oog r3 = model 1-op-1 verkleind (geel (40-41,5),(39-40,6), donkere hoek (41,6), zwarte rand (38-39,5), wenkbrauw (40-41,4)) (rij 2-15), per rij vanaf de eerste silhouetpixel
for x,y,row in [(36,2,"DDDDDDD"),(34,3,"DDhhhhmmBDDD"),(32,4,"DDmmshhbKKsBBBK"),(31,5,"DhhhbmsKKYYKssBKK"),
 (30,6,"DhhhhnbbsYYnhhhsBBK"),(29,7,"DhhhnbbbbbbhbbbbbsBK"),(29,8,"Dhnn"+"b"*14+"sK"),
 (29,9,"Dmhhsnnnnnm"+"b"*7+"ddK"),(30,10,"KhhhhsbbbnnnnKbbsddK"),(31,11,"Kbbbss"+"b"*7+"sbnddK"),
 (32,12,"KKssssnnsbbbbndddK"),(34,13,"KKKssssnnnnndddK"),(37,14,"KssssssbndddK"),(38,15,"KsssbbbndddK")]:
    zet(x,y,[row])
# vleugels per pixel naar het model (punt.py): arm licht bovenaan, vlies D, vingers n
for x,y,row in [(15,28,"D"),(12,29,"DDhBK"),(11,30,"DDhBBK"),(9,31,"DBnDDBnn"),(8,32,"DBnDDnBDDn"),
 (7,33,"DKBBBBnDDDDn"),(11,34,"KBnDDDDn"),(11,35,"KDKDnDDD"),
 (43,30,"DDDDDDDD"),(42,31,"DhhnBBBBnBBK"),(41,32,"DBBnDDDDDD"),(40,33,"DBnnDnBBBBK"),
 (38,34,"nDBnnDDBnBBK"),(39,35,"nDDnDDDnDBK"),(37,36,"DDDDDnDBDDBK"),(38,37,"DDDnDBBKKKKK"),
 (41,38,"nBBK")]:
    zet(x,y,[row])
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
