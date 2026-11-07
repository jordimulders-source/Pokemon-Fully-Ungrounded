"""Controle kleurronde 3: diff met kleur1-E buiten/binnen de kopzone, open randen, losse pixels, palet."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
ZONE=(0,0,47,25)   # x0,y0,x1,y1 inclusief: kop + halsband
a=Image.open(D+'kleur1/salticonda_E.png'); b=Image.open(D+'kleur3/salticonda.png'); A=a.load(); B=b.load()
inz=lambda x,y: ZONE[0]<=x<=ZONE[2] and ZONE[1]<=y<=ZONE[3]
out=[(x,y) for x in range(64) for y in range(64) if not inz(x,y) and A[x,y]!=B[x,y]]
inn=[(x,y) for x in range(64) for y in range(64) if inz(x,y) and A[x,y]!=B[x,y]]
body=[(x,y) for (x,y) in inn if y>=21 and A[x,y]!=0 and not (16<=x<=34 and y<=23)]
print('palet gelijk:',a.getpalette()[:48]==b.getpalette()[:48],'| modus',b.mode,'transparantie',b.info.get('transparency'))
print('gewijzigd buiten kopzone',ZONE,':',len(out))
print('gewijzigd binnen kopzone:',len(inn),'| waarvan E-lijfpixels (rij>=21, buiten oude halsband) bedekt door de nieuwe halsband:',len(body), 'rijen',sorted({y for x,y in body}))
S={(x,y) for x in range(64) for y in range(64) if B[x,y]!=0}
openr=[(x,y,CH[B[x,y]]) for (x,y) in S if inz(x,y) and any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]) and CH[B[x,y]] not in 'OKhst']
print('open randen in kopzone:',openr)
lone=[]
for (x,y) in S:
    if not inz(x,y): continue
    c=B[x,y]; n=[B[q] for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if q in S]
    if n and all(v!=c for v in n) and CH[c] not in 'OKhqrst': lone.append((x,y,CH[c]))
print('losse pixels in kopzone:',len(lone),lone)
def bbox(P,xr,yr):
    pts=[(x,y) for x in xr for y in yr if P[x,y]!=0]; xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; return min(xs),max(xs),min(ys),max(ys)
