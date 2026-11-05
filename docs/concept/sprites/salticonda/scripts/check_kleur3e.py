"""Controle 3e: alpha-diff 0 met kleur3, alleen kuifinterieur gewijzigd, omlijning/neus/oog/wenkbrauw/wang/halsband/lijf gelijk."""
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
from PIL import Image
from kop3e import D, CH, kuifmasker, vast
a=Image.open(D+'kleur3/salticonda.png'); b=Image.open(D+'kleur3e/salticonda.png'); A=a.load(); B=b.load()
alpha=sum(1 for x in range(64) for y in range(64) if (A[x,y]!=0)!=(B[x,y]!=0))
ch=[(x,y) for x in range(64) for y in range(64) if A[x,y]!=B[x,y]]
buiten=[p for p in ch if not (kuifmasker(*p) and not vast(*p))]
oml=[p for p in ch if CH[A[p]] in 'hKO']
print('palet gelijk:',a.getpalette()[:48]==b.getpalette()[:48],'| modus',b.mode,'transparantie',b.info.get('transparency'))
print('alpha-diff met kleur3:',alpha,'| gewijzigd:',len(ch),'| buiten het kuifinterieur:',len(buiten),'| omlijningspixels gewijzigd:',len(oml))
