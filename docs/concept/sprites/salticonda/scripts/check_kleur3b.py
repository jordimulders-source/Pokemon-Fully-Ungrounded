"""Controle kleurronde 3b: bevroren zones gelijk aan kleur3, open randen, losse pixels, bovenrand."""
import sys
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
from PIL import Image
from kop3b import frozen, D, CH
a=Image.open(D+'kleur3/salticonda.png'); b=Image.open(D+'kleur3b/salticonda.png'); A=a.load(); B=b.load()
fr=[(x,y) for x in range(64) for y in range(64) if frozen(x,y) and A[x,y]!=B[x,y]]
ch=[(x,y) for x in range(64) for y in range(64) if A[x,y]!=B[x,y]]
print('palet gelijk:',a.getpalette()[:48]==b.getpalette()[:48],'| modus',b.mode,'transparantie',b.info.get('transparency'))
print('bevroren zones (oog, wenkbrauw, wang/gezichtslijn, halsband+lijf rij>=20, alles buiten x0-47 y0-25) gewijzigd:',len(fr))
xs=[x for x,y in ch]; ys=[y for x,y in ch]
print('gewijzigd totaal:',len(ch),'| binnen x',min(xs),'-',max(xs),'y',min(ys),'-',max(ys))
print('rij 0 leeg:',all(B[x,0]==0 for x in range(64)),'| bovenste kop-rij:',min(y for x in range(64) for y in range(64) if B[x,y]!=0))
S={(x,y) for x in range(64) for y in range(64) if B[x,y]!=0}
openr=[(x,y,CH[B[x,y]]) for (x,y) in S if y<26 and any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]) and CH[B[x,y]] not in 'OKhst']
print('open randen kop:',openr)
lone=[(x,y,CH[B[x,y]]) for (x,y) in S if y<26 and CH[B[x,y]] not in 'OKhqrst' and all(B[q]!=B[x,y] for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if q in S)]
print('losse pixels kop:',len(lone),lone)
