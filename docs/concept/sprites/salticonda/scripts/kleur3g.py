"""Kleur3g: reparaties R1-R4 uit keuring/KEURING.md + Electric-hint, met de hand per pixel op het raster van 3f.
Alle bewerkingen in 3f-coordinaten; daarna de hele sprite 2 px omlaag (R1)."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH={'.':0,'O':1,'K':2,'h':3,'e':4,'d':5,'c':6,'b':7,'a':8,'f':9,'g':10,'q':11,'r':12,'s':13,'t':14,'v':15}
V=(252,232,96)   # index 15: warm lichtgeel 'geladen' glans (geen ijsblauw)
r=[list(l) for l in open(D+'kleur3f/salticonda_raster.txt').read().split('\n')[:64]]
o=[row[:] for row in r]
Z={1:set(),2:set(),3:set(),5:set()}
def put(x,y,c,z):
    if r[y][x]!=c: r[y][x]=c
    Z[z].add((x,y))
def sag(x,y0,y1,z=1):
    """band in kolom x (rijen y0..y1) 1 px omlaag; bovenste pixel krijgt de kleur erboven (onderkant bovenste winding)"""
    col=[o[y][x] for y in range(y0,y1+1)]
    put(x,y0,o[y0-1][x],z)
    for i,c in enumerate(col): put(x,y0+1+i,c,z)
# --- R2/punt 1: ringen als ellips ---
for x in range(20,28): sag(x,47,49)            # ring 3: 45(3) 46(6) 47(6) 48(8) 47(7) 46(6) 45(4) 44(3) 43(4)
for x in (18,19,31,32): sag(x,32,34)            # ring 2: 31(3) 32(5) 33(4) 34(7) 33(4) 32(4) 31(4) 30

for x in range(22,29): sag(x,33,35)
for x in (29,30): pass                           # blijven op 33
# halsband: onderste twee rijen in het midden 1 px omlaag (rij 23 herhaald), onderrand zakt naar 26
for x in range(19,27):
    put(x,24,o[23][x],1); put(x,25,o[24][x],1); put(x,26,'s',1)
# halsband: runs <= 8 (rij 22 q x22-30 -> r op x30; rij 23 r x26-35 -> s op x34-35)
put(30,22,'r',1); put(37,24,'t',1); put(38,24,'t',1); put(39,24,'t',1); put(34,23,'s',1); put(35,23,'s',1)
# --- punt 2: onderrand en rechtsonder naar donkerste omlijning ---
for y in range(55,61):
    for x in range(0,64):
        if o[y][x]=='K': put(x,y,'O',2)
# schaduwkant rechts (halsband t/m ring 2): K -> O
for y in range(21,39):
    for x in range(40,64):
        if o[y][x]=='K': put(x,y,'O',2)
# --- R4/punt 3: staart 4-5 px dik, taps, eindigend in een zoutkegeltje (rijen in 3f-coordinaten, x 55..62) ---
STAART={  # x 55..63 in 3f-coordinaten; '-' = laten staan
 42:"....K....",
 43:"...haO...",
 44:"..habdO..",
 45:".habgdeO.",
 46:".KcgcdeO.",
 47:".OrsttOO.",
 48:"-.KcdeO..",
 49:"-OKcdeeO.",
 50:"-edcdeeO.",
 51:"-eedeeO..",
 52:"-eedeO...",
 53:"--eeO....",
 54:"---O.....",
}
import sys

KEEP=set()
for y,row in STAART.items():
    for i,c in enumerate(row):
        x=55+i
        if c!='-': put(x,y,c,3)
        else: KEEP.add((x,y))
for y in range(41,55):            # oude staartpixels buiten de nieuwe staart wissen
    for x in range(56,64):
        if (x,y) not in Z[3] and (x,y) not in KEEP and o[y][x]!='.' and x>=57: put(x,y,'.',3)
# --- punt 5: Electric-hint: 'geladen' glans (index 15) op de lichte kant van de ringen ---
GLANS=[(18,22),(19,22),(20,22),(21,22),(32,21)] if '--glans' not in sys.argv else eval(sys.argv[sys.argv.index('--glans')+1])
for x,y in GLANS: put(x,y,'v',5)
# --- R1/punt 4: alles 2 px omlaag ---
S=2
n=[['.']*64 for _ in range(S)]+r[:64-S]
assert all(c=='.' for c in ''.join(''.join(l) for l in r[64-S:]))
out=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else D+'kleur3g/salticonda'
im=Image.open(D+'kleur3f/salticonda.png'); pal=im.getpalette()[:48]; pal[45:48]=list(V)
g=Image.new('P',(64,64)); g.putpalette(pal+[0]*(768-48))
g.putdata([CH[c] for l in n for c in l]); g.save(out+'.png',transparency=0)
open(out+'_raster.txt','w').write('\n'.join(''.join(l) for l in n)+'\n')
