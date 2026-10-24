"""Stap 1: ruwe opzet per onderdeel op de Galar-Linoone-onderlaag (Linoone-coordinaten).
Levert een eerste tekst-raster dat daarna met de hand wordt afgewerkt (raster_f1.txt).
Alleen een hulpmiddel: het eindresultaat is het handbewerkte raster."""
import sys
H='/home/user/projectgrounded/docs/concept/sprites/olinguito/herbouw_linoone/'
def sp(d): return {y:[tuple(s) for s in v] for y,v in d.items()}
# onderdelen achter -> voor; (naam, ver?, spans)
P=[
('staart',0,{27:[(44,46)],28:[(44,48)],29:[(45,50)],30:[(46,51)],31:[(47,52)],32:[(48,53)],33:[(49,54)],34:[(49,54)],
   35:[(50,55)],36:[(50,55)],37:[(51,56)],38:[(51,56)],39:[(51,56)],40:[(51,56)],41:[(46,48),(51,56)],42:[(45,49),(51,56)],
   43:[(45,49),(51,55)],44:[(45,55)],45:[(46,54)],46:[(47,53)],47:[(48,52)]}),
('achter_ver',1,{38:[(26,32)],39:[(26,33)],40:[(26,32)],41:[(26,32)],42:[(25,31)],43:[(24,31)],44:[(24,30)]}),
('voor_ver',1,{38:[(19,25)],39:[(19,25)],40:[(19,25)],41:[(19,25)],42:[(19,24)],43:[(19,24)],44:[(18,24)],45:[(17,24)],46:[(17,23)]}),
('romp',0,{26:[(29,39)],27:[(24,42)],28:[(23,44)],29:[(22,45)],30:[(22,46)],31:[(22,47)],32:[(22,47)],33:[(22,47)],
   34:[(22,47)],35:[(22,47)],36:[(21,46)],37:[(21,45)],38:[(21,26),(33,44)]}),
('achter_nabij',0,{31:[(37,42)],32:[(35,44)],33:[(34,45)],34:[(34,46)],35:[(34,46)],36:[(34,46)],37:[(34,45)],38:[(34,44)],
   39:[(34,43)],40:[(35,43)],41:[(36,43)],42:[(37,43)],43:[(37,43)],44:[(36,42)],45:[(35,42)],46:[(34,42)],47:[(34,41)]}),
('kop',0,{24:[(11,15)],25:[(6,20)],26:[(5,21)],27:[(4,22)],28:[(3,22)],29:[(2,23)],30:[(1,23)],
   31:[(0,23)],32:[(0,23)],33:[(1,22)],34:[(1,22)],35:[(2,21)],36:[(3,20)],37:[(4,19)],38:[(6,17)]}),
('voor_nabij',0,{37:[(14,21)],38:[(13,21)],39:[(13,21)],40:[(13,20)],41:[(12,19)],42:[(12,18)],43:[(11,18)],44:[(11,17)],
   45:[(10,17)],46:[(9,17)],47:[(9,17)],48:[(10,16)]}),
]
W=64
can=[[0]*W for _ in range(64)]; own=[[None]*W for _ in range(64)]
for name,ver,d in P:
    m=set((x,y) for y,s in d.items() for a,b in s for x in range(a,b+1))
    for (x,y) in m:
        def inm(a,b): return (a,b) in m
        edge_r = not inm(x+1,y) or not inm(x,y+1)
        edge_l = not inm(x-1,y) or not inm(x,y-1)
        if edge_r: c=1
        elif edge_l: c=2
        else:
            # licht linksboven
            tl = (not inm(x-2,y)) or (not inm(x,y-2)) or (not inm(x-1,y-1))
            br = (not inm(x+2,y)) or (not inm(x,y+2)) or (not inm(x+1,y+1))
            c = 5 if tl else (3 if br else 4)
            if ver: c={5:4,4:3,3:3}[c]
        if ver and c==1: c=1
        can[y][x]=c; own[y][x]=name
out=sys.argv[1] if len(sys.argv)>1 else H+'bron/raster_schets.txt'
with open(out,'w') as f:
    for y in range(64): f.write(''.join('.' if v==0 else '0123456789ABCDEF'[v] for v in can[y])+'\n')
print('px',sum(1 for y in range(64) for x in range(64) if can[y][x]))
