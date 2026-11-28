# K1 afwerking: meting (meet.py masker_k1 kap_k1 3.3 83.7 101.5) + ogen/wenkbrauwen/neus/mond zoals r9 (per pixel naar het model)
import sys, numpy as np
R='docs/concept/sprites/pachamama/sprite_r7model/'
o=np.load(sys.argv[1]).copy(); meet=o.copy(); m=np.load(R+'r10/masker_k1.npy')
d,a=13,10; E={}
def z(y,x,v,k): E[(y,x)]=(v,k)
# linkeronderkant: kapopening is daar breder dan het r10-gezicht -> gezichtslijn (2, modeltint) op de maskerrand, huid erbinnen
for c in [(21,22),(22,22),(23,22),(24,22),(25,22),(26,22),(27,23),(28,23)]: z(*c,2,'gezichtslijn links op de rand van de kapopening (r10 smaller)')
for c in [(21,23),(22,23)]: z(*c,d,'modellijn 1 px naar buiten verplaatst -> wangvlak')
for c in [(23,23),(24,23),(25,23),(26,23),(28,24),(26,24),(27,24)]: z(*c,4,'modellijn naar buiten verplaatst / opvulling -> 4')
# wenkbrauwen (model j56-58): links doorlopend naar de neuslijn, rechts een boog
z(17,25,2,'linkerwenkbrauw'); z(17,26,2,'linkerwenkbrauw -> neuslijn')
for x in (30,31,32): z(16,x,2,'rechterwenkbrauw (boog)')
# ogen zoals r9: bovenlid, wit | iris/pupil | wit, 2 rijen
z(18,26,1,'bovenlid links'); z(18,30,1,'bovenlid rechts')
z(20,25,2,'iris links (r9)'); z(20,26,a,'wit links (r9)')
z(19,32,2,'iris rechts (r9)'); z(20,30,a,'wit (r9)'); z(20,31,2,'iris (r9)'); z(20,32,2,'iris (r9)'); z(20,33,a,'wit (r9)')
# neus zoals r9: lijn | licht | lijn tussen de ogen, onderaan breder
for y in (18,19,20): z(y,27,2,'neuslijn links'); z(y,28,5,'neus licht')
for y in (21,22,23): z(y,28,5,'neus licht (onderaan breder)')
# mond (model j88: kort streepje) valt bij deze schaal onder 1/3 van de cel
for x in (27,28,29): z(26,x,2,'mondstreepje (model i76-85, j88)')
for (y,x),(v,k) in E.items():
  assert m[y,x],(y,x); o[y,x]=v
np.save(sys.argv[2],o)
af=[(int(y),int(x),'%x'%meet[y,x],'%x'%o[y,x],E[(y,x)][1]) for y,x in zip(*np.where(m)) if meet[y,x]!=o[y,x]]
print('afwijkend van de meting:',len(af)); [print(t) for t in af]
print('nul in masker:',int((m&(o==0)).sum()))
