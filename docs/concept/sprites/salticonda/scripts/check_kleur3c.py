"""Controle kleurronde 3c t.o.v. kleur3b: alleen kuif en snuitfront gewijzigd; oog, wenkbrauw, wang, halsband en lijf 0 pixels anders."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
a=Image.open(D+'kleur3b/salticonda.png'); b=Image.open(D+'kleur3c/salticonda.png'); A=a.load(); B=b.load()
oud={y:max(x for x in range(48) if A[x,y]!=0) for y in range(1,20)}; oud[13]=44
def kuif(x,y): return (1<=y<=5 and x>=13) or (y==6 and 13<=x<=14) or (2<=y<=19 and x>=oud[y]-1)
def snuit(x,y): return 4<=x<=14 and 5<=y<=10
def bevroren(x,y):  # zoals in kop3b: oog, wenkbrauw, wang/gezichtslijn, halsband+lijf
    return (y>=20) or (20<=x<=33 and 10<=y<=14) or (23<=x<=30 and y==15) or (21<=x<=33 and 7<=y<=9) or (23<=x<=30 and y==6) or (25<=x<=27 and y==5) or (33<=x<=36 and 9<=y<=19)
ch=[(x,y) for x in range(64) for y in range(64) if A[x,y]!=B[x,y]]
buiten=[p for p in ch if not (kuif(*p) or snuit(*p))]
bev=[p for p in ch if bevroren(*p)]
print('palet gelijk:',a.getpalette()[:48]==b.getpalette()[:48],'| modus',b.mode,'transparantie',b.info.get('transparency'))
print('gewijzigd:',len(ch),'| buiten kuif+snuitfront:',len(buiten),buiten[:10],'| in bevroren zones (oog, wenkbrauw, wang, halsband, lijf):',len(bev))
print('kuifpixels gewijzigd:',sum(1 for p in ch if kuif(*p)),'| snuitfront:',sum(1 for p in ch if snuit(*p)))
print('rij 0 leeg:',all(B[x,0]==0 for x in range(64)))
S={(x,y) for x in range(64) for y in range(64) if B[x,y]!=0}
print('open randen kop:',[(x,y,CH[B[x,y]]) for (x,y) in S if y<26 and any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]) and CH[B[x,y]] not in 'OKhst'])
