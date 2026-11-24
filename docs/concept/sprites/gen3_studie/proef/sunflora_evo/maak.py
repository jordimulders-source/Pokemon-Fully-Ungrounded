from PIL import Image
SRC='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/sunflora_evo/af/sunflora_evo.png'
im=Image.open(SRC); px=im.load()
# gezicht: ogen, mond, wenkbrauwen, AA-pixels aan de gezichtslijnen
face=set()
for y in range(25,28):
    for x in range(19,36):
        if px[x,y] in (1,8,9): face.add((x,y))
for y in range(31,36):
    for x in range(22,32):
        if px[x,y] in (6,10,4): face.add((x,y))
brows=[(20,25),(21,24),(21,23),(22,23),(23,23),(24,24),(25,25),(27,25),(28,24),(29,23),(30,23),(31,23),(32,23),(33,24),(34,25)]
aa=[(20,27),(19,28),(24,28),(29,28),(34,28),(23,25),(30,25),(31,30),(30,34)]
face|=set(brows)|set(aa)
C={}  # (x,y): nieuwe index
def s(pts,c):
    for p in pts: C[p]=c
L,Y,O,S,B=4,3,None,3,6
# lichtkant: buitenlijn in donker goud (4)
s([(28,18),(29,18),(30,18),(25,19),(31,19),(22,20),(23,20),(24,20),(21,21),(20,22),(19,23),(18,24),(18,26),(18,31)],4)
# ringen binnen de lichtkant -> grondtint creme (2)
s([(22,21),(22,22),(33,21),(34,22),(34,23),(34,24),(19,24),(19,26),(20,28),(19,29),(20,29),(19,30),(20,30),(19,31),(20,31),(20,32),(34,29),(34,30)],2)
# schaduwsikkel rechts + kinzone onder: 3
s([(35,22),(35,23),(36,23),(35,24),(36,24),(36,25),(36,26),(37,26),(38,26),(38,27),(38,28),(38,29),(35,28),(35,29),(35,30),(38,30),
   (34,32),(34,33),(33,34),(36,34),(31,34),(32,35),(33,35),(35,35),(32,36),(34,36),(31,37),(32,37),(25,38),(30,38),
   (20,33),(20,34),(20,35),(21,35),(21,36)],3)
# schaduwkant: buitenlijn bruin (6)
s([(36,21),(37,22),(37,23),(37,24),(39,26),(39,27),(39,28),(39,29),(39,30)],6)
hit=[p for p in C if p in face]
print('in gezicht (worden overgeslagen):',hit)
out=im.copy(); op=out.load()
for p,c in C.items():
    if p in face: continue
    op[p]=c
out.save('na.png')
# bewijzen
a=Image.open(SRC); b=Image.open('na.png'); pa=a.load(); pb=b.load()
mask=sum((pa[x,y]==0)!=(pb[x,y]==0) for x in range(64) for y in range(64))
fd=sum(pa[p]!=pb[p] for p in face)
ch=[(x,y) for x in range(64) for y in range(64) if pa[x,y]!=pb[x,y]]
print('silhouet diff',mask,'gezicht diff',fd,'(',len(face),'px bevroren)','gewijzigd',len(ch))
from collections import Counter
print(Counter((pa[p],pb[p]) for p in ch))
print('kleuren', len(set(b.getdata())-{0}), b.mode, b.size)
