"""Kuifoppervlak (zelfde masker voor elke versie): rij 0-5 vanaf x 12, rij 6-9 vanaf x 21 (boven/achter het oog), rij 10-19 vanaf x 34 (achter de gezichtslijn)."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
def kuif(f,dy=0):
    P=Image.open(D+f).load()
    pts=[(x,y) for x in range(64) for y in range(20+dy) if P[x,y]!=0 and ((y-dy<=5 and x>=12) or (6<=y-dy<=9 and x>=21) or (y-dy>=10 and x>=34))]
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return len(pts), max(xs)-min(xs)+1, max(ys)-min(ys)+1, min(xs),max(xs),min(ys)
r={}
for k,dy in [('kleur3',0),('kleur3b',0),('kleur3c',0),('kleur3e',0),('kleur3d',3)]:
    r[k]=kuif(k+'/salticonda.png',dy); print(k,'oppervlak',r[k][0],'px | breedte',r[k][1],'(x %d-%d)'%(r[k][3],r[k][4]),'| hoogte',r[k][2],'(vanaf rij %d)'%r[k][5])
print('3c/kleur3 %.2fx | 3d/kleur3: oppervlak %.2fx, breedte %.2fx, hoogte %.2fx'%(r['kleur3c'][0]/r['kleur3'][0],r['kleur3d'][0]/r['kleur3'][0],r['kleur3d'][1]/r['kleur3'][1],r['kleur3d'][2]/r['kleur3'][2]))
