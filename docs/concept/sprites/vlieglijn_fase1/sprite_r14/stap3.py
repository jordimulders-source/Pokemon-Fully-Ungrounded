import sys; sys.path.insert(0,'sprite_r14')
from lib import *
im=Image.open('sprite_r14/_stap1.png'); b=im.load()
# punt 3: onderrand / aansluiting poten
b[22,39]=1                      # lijfrand onder de kop sluiten (vrijgekomen door verschuiving)
b[25,40]=9; b[26,40]=7          # voorpoot B komt onder A vandaan, zonder dwarsstreep
for x in (28,29,30,31,32): b[x,39]=2   # middenpoot komt direct uit het borststuk, onderrand zakt naar achter
b[36,41]=2; b[37,41]=2          # dwarsstreep achterlijf weg: kapjes van nieuwe en achterpoot schuin
# punt 4: zwart vak boven rechter oog -> kopgrijs zoals buren (x17, x22 op rij 27)
for x in range(18,22): b[x,27]=5
im.save('sprite_r14/_stap3.png',transparency=0)
