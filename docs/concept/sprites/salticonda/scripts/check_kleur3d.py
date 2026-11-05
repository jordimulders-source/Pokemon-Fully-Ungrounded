"""Controle 3d: alles behalve de kuif = kleur3 verschoven met DY (0 verschil); rij 0 leeg; open randen."""
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
from PIL import Image
from kop_kleur3d import D, CH, DY, kuifmasker, vast
a=Image.open(D+'kleur3/salticonda.png'); b=Image.open(D+'kleur3d/salticonda.png'); A=a.load(); B=b.load()
vastp=[(x,y) for x in range(64) for y in range(61) if A[x,y]!=0 and not (kuifmasker(x,y) and not vast(x,y))]
diff=[(x,y) for (x,y) in vastp if B[x,y+DY]!=A[x,y]]
lijf=[(x,y) for (x,y) in vastp if y>=20]
print('palet gelijk:',a.getpalette()[:48]==b.getpalette()[:48],'| modus',b.mode,'transparantie',b.info.get('transparency'))
print('niet-kuifpixels van kleur3 (neus, snuit, gezicht, oog, wenkbrauw, wang, halsband, lijf):',len(vastp),'| anders na verschuiving %d px omlaag:'%DY,len(diff))
print('   waarvan halsband+lijf (rij>=20):',len(lijf),'| anders:',sum(1 for p in diff if p[1]>=20))
extra=[(x,y) for x in range(64) for y in range(64) if B[x,y]!=0 and y>=23 and not (y-DY>=0 and A[x,y-DY]!=0)]
print('pixels onder de kuif die niet uit kleur3 komen:',len(extra))
print('rij 0 leeg:',all(B[x,0]==0 for x in range(64)),'| onderste rij:',max(y for x in range(64) for y in range(64) if B[x,y]))
S={(x,y) for x in range(64) for y in range(64) if B[x,y]!=0}
print('open randen:',[(x,y,CH[B[x,y]]) for (x,y) in S if any(q not in S for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]) and CH[B[x,y]] not in 'OKhst'])
