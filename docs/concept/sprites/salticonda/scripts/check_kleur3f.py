"""Controle 3f t.o.v. 3e: alpha-diff 0, pixels per zone, niets buiten kop/overgang, vorm kuif (naden g, omlijning) en neus/oog gelijk."""
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
from PIL import Image
from kop3f import D, CH, kuifmasker, vast
a=Image.open(D+'kleur3e/salticonda.png'); b=Image.open(D+'kleur3f/salticonda.png'); A=a.load(); B=b.load()
alpha=sum(1 for x in range(64) for y in range(64) if (A[x,y]!=0)!=(B[x,y]!=0))
ch=[(x,y) for x in range(64) for y in range(64) if A[x,y]!=B[x,y]]
kop=[p for p in ch if kuifmasker(*p) and not vast(*p)]; overgang=[p for p in ch if p[1]==26 and 15<=p[0]<=30]
rest=[p for p in ch if p not in kop and p not in overgang]
print('palet gelijk:',a.getpalette()[:48]==b.getpalette()[:48],'| modus',b.mode,'transparantie',b.info.get('transparency'))
print('alpha-diff met 3e:',alpha,'| gewijzigd:',len(ch),'| kop (schaduwkant kuif):',len(kop),'| overgang (slagschaduw winding):',len(overgang),'| elders:',len(rest))
print('naden (g) of omlijning (hKO) gewijzigd:',sum(1 for p in ch if CH[A[p]] in 'ghKO'),'| neus/gezicht/oog/wenkbrauw/wang/halsband gewijzigd:',sum(1 for p in ch if vast(*p) or not (kuifmasker(*p) or p in overgang)))
