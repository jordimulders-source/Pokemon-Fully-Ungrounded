"""Kuifoppervlak (zelfde masker voor elke versie): rij 0-5 vanaf x 13, rij 6-9 vanaf x 21 (boven/achter het oog), rij 10-19 vanaf x 34 (achter de gezichtslijn)."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
def kuif(f):
    P=Image.open(D+f).load()
    pts=[(x,y) for x in range(64) for y in range(20) if P[x,y]!=0 and ((y<=5 and x>=13) or (6<=y<=9 and x>=21) or (y>=10 and x>=34))]
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return len(pts), max(xs)-min(xs)+1, max(ys)-min(ys)+1, min(xs),max(xs),min(ys)
r={}
for k in ['kleur3','kleur3b','kleur3c']:
    r[k]=kuif(k+'/salticonda.png'); print(k,'oppervlak',r[k][0],'px | breedte',r[k][1],'(x %d-%d)'%(r[k][3],r[k][4]),'| hoogte',r[k][2],'(vanaf rij %d)'%r[k][5])
print('3c t.o.v. kleur3: %+.0f%%, t.o.v. 3b: %+.0f%%'%((r['kleur3c'][0]/r['kleur3'][0]-1)*100,(r['kleur3c'][0]/r['kleur3b'][0]-1)*100))
