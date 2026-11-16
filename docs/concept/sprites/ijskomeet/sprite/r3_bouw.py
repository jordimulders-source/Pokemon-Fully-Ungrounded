# r3: lijf terug naar schotsen (model-naden), ogen rond, spiraalaanzet + sterren. Basis r2.txt.
from gio import from_txt, to_txt, CH
import numpy as np
o=from_txt('r2.txt')
L=[''.join('.' if v<0 else CH[v] for v in r) for r in o]
def put(y,s,x0=0):
    global L
    r=L[y]; L[y]=r[:x0]+s+r[x0+len(s):]
def setp(x,y,c):
    put(y,c,x)
# --- lijf, rijen x0..33 (rest blijft r2) ---
rows={
38:".SWWLLgLLLLLLggLLLLLM",
39:".SWLLLLLLLLLLLLLLLLLLMSKKKKKKK",
40:".SWLLLLLLLLLLLLLLLLMMSWWWWWWWK",
41:".SWLLLLLLLLLLLLLLLMMSWWWWWWWLK",
42:".SSSSMMMMLLLLLLLLMSSWWWWLLLLLKKWWK",
43:".SWWWSSSSMMMMMMSSSLLLLLLLLLLMKWLLK",
44:".SWLLLLLMSSSSSSMMMLLLLLLLLMMSWLLLK",
45:".SWLLLLMSLMMSWWSSSMMMMDDDDSSWLLLMK",
46:"..SWLLLLMSMSWWWWWWSSSSSSSSWWLLLLMK",
47:"..KWLLLLMSSWLLLLLLWWWWWWSWLLLLLMMK",
48:"..KWLLLLMSWLLLLLLLLLLLLLSWLLLLMMDK",
49:"...KWLLLMSWLLLLLLLLLLLLLMSWLLMMMDK",
50:"...KWLLMMSLLLLLLLLLLLMMMMSLMMMDDK",
51:"...KWLLMSLSLLLLLLLMMMMMMMMSMMDDK",
52:"....KLMMSLSSLLLMMMMMMMMMDDDSMDDK",
53:".....KSSLLLLSDDDMMMMMMMMDDDSDDK",
54:".......KLMMMMSSSDDDDDDMMMMMDSSSSK",
55:".......KLMMMMSLLSSSSSSDDDDDSLLLLMK",
56:"........KMMMDSMMLLLLLLSSSSSLMMMDK",
57:".........KMMDSMMMMMMMMMSLLLMMDK",
58:"..........KKKSMMMMDDDDDDSDDKK",
}
for y,s in rows.items(): put(y,s,0)
# --- kop: dubbele buitenlijn links (M-lijn naast S) laten eindigen ---
setp(7,30,'W'); setp(7,31,'W')
# --- ogen: donkere rand rondom, kern kleiner ---
for (x,y) in [(8,33),(11,33),(16,33),(4,36),(8,36),(11,36),(16,36)]: setp(x,y,'r')
setp(6,35,'c'); setp(14,35,'c')
# ogen afronden: hoeken van de kern dicht (rechts 6x6, links 5x6)
for (x,y) in [(12,33),(15,33),(12,36),(15,36),(5,36),(7,36)]: setp(x,y,'r')
# --- kern: spiraalaanzet (boog v rond de vlek, gescheiden door n) ---
for (x,y) in [(26,32),(27,32),(28,33),(29,34),(29,35),(28,36)]: setp(x,y,'v')
# opschonen losse tintpixels
for (x,y,c) in [(9,45,'M'),(26,50,'W'),(31,56,'M'),(29,57,'M'),(14,56,'L'),(15,56,'L'),(18,37,'L'),(19,37,'M')]: setp(x,y,c)
# --- sterpixels in de staart ---
for (x,y) in [(29,21),(42,25),(40,38)]: setp(x,y,'w')
o2=np.array([[-1 if c=='.' else CH.index(c) for c in r] for r in L])
to_txt(o2,'r3.txt')
m=np.load('mask_r1.npy'); print('alpha-diff',int(((o2>=0)!=m).sum()))
for y in range(30,62): print('%2d '%y+L[y][:40])
