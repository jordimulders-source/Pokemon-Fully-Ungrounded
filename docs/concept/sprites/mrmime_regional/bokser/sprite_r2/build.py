# Bokser r2: r1 (../sprite_r1/r1.npy) + alleen de benoemde reparaties van Claude (snor, ogen, benen, vuisten, V-variant).
# Varianten via omgevingsvariabelen: OOG=A|B|C  VUIST=D|L  V=vlak|lijn  UIT=bestandsnaam
import numpy as np, json, os
from PIL import Image
from palet import PAL
r1=np.load('../sprite_r1/r1.npy'); b=r1.copy(); H,W=b.shape
OOG=os.environ.get('OOG','B'); VUIST=os.environ.get('VUIST','D'); V=os.environ.get('V','vlak'); UIT=os.environ.get('UIT','bokser')
zones={}
def put(z,y,x,v): zones.setdefault(z,set()).add((y,x)); b[y,x]=v
def rows(z,y0,x0,lines):
    for dy,s in enumerate(lines):
        for dx,c in enumerate(s.replace(' ','')):
            if c!='.': put(z,y0+dy,x0+dx,int(c))

# 1. SNOR uit het model: natief rij 19 kol 32-35 (boven), rij 20 kol 31-32 + 34-37 (krullen omlaag aan de uiteinden)
#    -> sprite rij 13 kol 23-25, rij 14 kol 22-26 (uiteinden zwart, midden donkergrijs: modelgat op natief kol 33)
rows('snor',13,23,["1 1 1"])
rows('snor',14,22,["1 2 2 2 1"])

# 2. OGEN: Gen 3 Mr. Mime-oog (pupil 3 boven 1, oogwit rechts), zonder de rand (b) rechts die als bril leest
for x in (24,28):
    for y in (9,10,11,12): put('ogen',y,x,8)
if OOG=='A':      # MM 1-op-1 zonder rand: lichtgrijze puntjes (MM '1') boven en onder het oogwit
    rows('ogen',9,22,["8 7"]); rows('ogen',12,22,["8 7"]); rows('ogen',9,26,["8 7"]); rows('ogen',12,26,["8 7"])
elif OOG=='B':    # zoals het model: alleen zwarte pupil + oogwit, geen grijs eromheen
    rows('ogen',9,22,["8 8"]); rows('ogen',12,22,["8 8"]); rows('ogen',9,26,["8 8"]); rows('ogen',12,26,["8 8"])
elif OOG=='C':    # pupil + oogwit, alleen een onderlid-schaduw (6) onder het oogwit
    rows('ogen',9,22,["8 8"]); rows('ogen',12,22,["8 6"]); rows('ogen',9,26,["8 8"]); rows('ogen',12,26,["8 6"])

# 3. BENEN: schone omlijning (1), vlakke lichtgrijze huid 7, schaduwkant rechts 6; knieplekken alleen beenhuid
rows('benen',43,22,["1 7 7 6 1"]); rows('benen',44,22,["1 7 7 6 1"])
rows('benen',45,23,["1 7 6 1"]);   rows('benen',46,23,["1 7 6 1"])
rows('benen',47,23,["1 7 7 6 1"]); rows('benen',48,23,["1 7 7 6 1"])
rows('benen',49,24,["1 7 7 6 1"]); rows('benen',50,25,["1 7 6 1"])
rows('benen',51,25,["1 7 7 6 1"])
for y in (52,53,54): rows('benen',y,26,["1 7 6 1"])
rows('benen',55,27,["1 6 1"])
for y in (43,44,45): rows('benen',y,29,["1 7 7 6 1"])
for y in range(46,51): rows('benen',y,30,["1 7 6 1"])
rows('benen',51,30,["7 7 6 1"]); rows('benen',52,30,["7 7 6 1"])
for y in (53,54,55): rows('benen',y,30,["1 7 6 1"])

# 4. VUISTEN: verticale vingerscheidingen + knokkelrij bovenaan + duim dwars onderlangs; silhouet = r1/model
NAB=[". . 1 1 1 1 1",
     ". 1 8 8 5 8 8 1",          # knokkelrij
     "1 7 8 7 5 8 7 1",
     "1 7 8 7 5 8 7 6 1",
     "1 6 7 6 5 7 6 6 1",
     "1 1 5 5 5 5 6 6 6 1",      # duimrand
     ". . 1 4 8 7 7 6 6 1",      # duim
     ". . . . 1 1 1 1 1 8"]
VER=[(19,28,". . . 1 1 1"),
     (20,28,"1 8 8 5 8 8 1"),
     (21,28,"1 7 8 5 8 7 1"),
     (22,27,"1 7 8 7 5 8 7 1"),
     (23,27,"1 6 7 6 5 7 6 1"),
     (24,28,"1 5 5 5 5 6 6 1"),
     (25,29,"1 7 8 7 6 6 1"),
     (26,30,"1 1 1 1 1 1")]
if VUIST=='D':   # model-donkergrijs met lichte tape: 8->5 7->4 6->3 vingerscheiding 5->2, tapeband rij 2 licht (6)
    m={'8':'5','7':'4','6':'3','5':'2'}
    conv=lambda s:''.join(m.get(c,c) for c in s)
    NAB=[conv(s) for s in NAB]; VER=[(y,x,conv(s)) for y,x,s in VER]
    NAB[3]="1 6 6 6 2 6 6 3 1"; VER[3]=(22,27,"1 6 6 6 2 6 6 1")      # lichte tapeband over de vingers
    NAB[6]=". . 1 3 7 6 6 3 3 1"; NAB[7]=". . . . 1 1 1 1 1 8"; VER[6]=(25,29,"1 6 7 6 3 3 1")       # tape om de duim
rows('vuist_nabij',9,0,NAB)
for y,x,s in VER: rows('vuist_ver',y,x,[s])

# 5. V-patroon: standaard de gevulde V van r1; variant 'lijn' = V als lijn van 2 px
if V=='lijn':
    rows('v_lijn',18,21,["8 8 8 8 8 7 7 7"])
    rows('v_lijn',19,21,["8 8 8 8 8 8 8 7 7 7"])
    rows('v_lijn',20,21,["8 8 8 8 8 8 8"]); rows('v_lijn',21,21,["8 8 8 8 8 8 8"])
    rows('v_lijn',22,21,["8 8 8 8 8 8"]);   rows('v_lijn',23,21,["8 8 8 8 8 8"])
    for y,x in [(19,22),(19,23),(20,23),(20,24),(21,24),(21,25),(22,25),(22,26),(23,26),
                (19,29),(19,30),(20,27),(21,27)]:   # rechterbeen grotendeels achter de vuist
        put('v_lijn',y,x,3)

np.save(UIT+'.npy',b)
json.dump({k:sorted([int(a),int(c)] for a,c in v) for k,v in zones.items()},open(UIT+'_zones.json','w'))
full=np.zeros((64,64),'uint8'); full[0:H,10:10+W]=b
p=Image.fromarray(full,'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal)))
p.save(UIT+'.png',transparency=0)
d=(b!=r1); print(UIT,'afwijkend van r1:',int(d.sum()))
for k,v in zones.items(): print('  %-12s %d'%(k,sum(1 for y,x in v if d[y,x])))
