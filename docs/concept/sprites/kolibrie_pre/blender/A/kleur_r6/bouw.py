"""r6: kleur_r5/raster.txt + rijen_r6.txt -> raster_basis.txt; daarna drie oogmaten (S/M/L) -> raster_{S,M,L}.txt en kolibrie_pre_{S,M,L}.png.
kolibrie_pre.png = M (het Starly-oog). Snavelzone (x<=20) wordt niet aangeraakt."""
import sys, shutil
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
D=A+'kleur_r6/'
g=[list(l.rstrip('\n')) for l in open(A+'kleur_r5/raster.txt')][:64]
for l in open(D+'rijen_r6.txt'):
    if l.startswith('#') or not l.strip(): continue
    y,x0,*p=l.split(); p=''.join(p)
    for i,c in enumerate(p): g[int(y)][int(x0)+i]=c
# oogvak leeg naar gezicht (zoals rond het M-oog in r5): wordt per maat overschreven
GEZICHT={16:'55555',17:'55544',18:'55544',19:'54444',20:'44444',21:'44433'}   # x21-25
for y,s in GEZICHT.items():
    for i,c in enumerate(s): g[y][21+i]=c
g[17][26]=g[18][26]=g[20][26]='4'; g[19][26]='4'
def blok(rows):
    d={}
    for y,x0,s in rows:
        for i,c in enumerate(s):
            if c!=' ': d[(x0+i,y)]=c
    return d
OOG={
 # M = Starly-oog uit maker/kleur_r10 (x21-25 y14-18), pixel voor pixel, 3 omlaag
 'M':blok([(17,22,'111'),(18,21,'21712'),(19,21,'21712'),(20,21,'21512'),(21,22,'111')]),
 # S = zelfde opbouw, één glansrij minder (5x4)
 'S':blok([(18,22,'111'),(19,21,'21712'),(20,21,'21512'),(21,22,'111')]),
 # L = zelfde opbouw, groter en ronder (6x6, hoeken weg): glans 3 px linksboven, onderglans 1 px
 'L':blok([(19,27,'3'),(16,22,'2112'),(17,21,'217712'),(18,21,'117111'),(19,21,'111111'),(20,21,'211512'),(21,22,'2112')]),
}

sys.path.insert(0,D); import palet
open(D+'raster_basis.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
for m,eye in OOG.items():
    h=[r[:] for r in g]
    for (x,y),c in eye.items(): h[y][x]=c
    open(D+f'raster_{m}.txt','w').write('\n'.join(''.join(r) for r in h)+'\n')
    palet.build(D+f'raster_{m}.txt',D+f'kolibrie_pre_{m}.png')
shutil.copy(D+'raster_M.txt',D+'raster.txt'); shutil.copy(D+'kolibrie_pre_M.png',D+'kolibrie_pre.png')
