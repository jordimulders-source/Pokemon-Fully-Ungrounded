# r9 afwerking: meting (gezicht.py A=2 B=7) + per-pixel reparaties naar het model (natgrid r10, zie verslag).
# Gebruik: python3 r9/afwerking.py METING.npy UIT_PREFIX
import sys, numpy as np
from PIL import Image
D='docs/concept/sprites/pachamama/sprite_r7model/'
o=np.load(sys.argv[1]).copy(); meet=o.copy()
r4=np.array(Image.open(D+'r4/pachamama_r4.png')); m=np.load(D+'r9/masker.npy')
d,a=13,10
E={}
def z(y,x,v,k): E[(y,x)]=(v,k)
# 1. modelomlijning/haar valt op randcellen van het masker (r4 heeft daar al zijn eigen ring): vlaktint ernaast
for c in [(14,34),(15,35),(16,35),(18,36),(19,36),(23,36),(24,36),(26,35),(27,35)]: z(*c,3,'rand rechts: modellijn -> schaduw 3 (r4-ring is de lijn)')
z(17,36,3,'rand rechts: modelhaar -> 3')
for c in [(20,22),(21,22),(22,22)]: z(*c,d,'rand links: modellijn -> wangvlak d (r4-ring is de lijn)')
z(23,22,4,'rand links: gemengd 2/3/4/d -> 4'); z(24,22,4,'rand links: modellijn -> 4'); z(27,23,4,'rand links: modellijn -> 4'); z(28,23,4,'rand links: modellijn -> 4')
# linkerrand grenst aan de crème kaprand (geen zwarte r4-ring): gezichtslijn in 2 zoals het model (en r4)
for c in [(22,21),(23,21),(24,21),(27,22)]: z(*c,2,'gezichtslijn 2 tegen crème kaprand (model: lijn in 2)')
# kin: onderste rij = schaduw boven de r4-onderlijn
for c in [(31,24),(31,25),(31,27)]: z(*c,3,'kin: modelrij 100 = 3, lijn zelf is de r4-ring')
z(12,32,4,'buiten modelgezicht (kap): voorhoofdtint')
# 2. wenkbrauwen + neuslijn links als een doorlopende lijn (model)
z(17,25,2,'linkerwenkbrauw loopt door naar de neuslijn (model i66-75)')
z(18,26,2,'neuslijn links (model i77, L~55)'); z(20,26,2,'neuslijn links loopt tot onder het oog (model i76 j66-69)')
z(17,33,2,'rechterwenkbrauw: boog-einde (model)')
# 3. ogen (model: wit | iris/pupil | wit, donker bovenlid)
z(18,25,1,'bovenlid links over het hele oog (model i68-73)')
z(18,30,1,'bovenlid rechts (model i89-96)')
z(19,25,a,'wit rechts van de iris (model i74 W)')
z(20,32,2,'iris 2x2 (model iris i94-95; meting gaf wit)')
z(19,33,a,'wit rechts (model i96-98 W; meting telde de ooghoeklijn)')
# 4. neus onderkant: lijn links omlaag en onder (model i73-85 j76-83)
z(23,25,2,'neus: linkeronderrand (model i74 j77-81)'); z(24,25,2,'neus: linkeronderrand')
z(25,26,2,'neus: onderlijn (model j82)')
# 5. kaaklijn rechts doorlopend (model)
z(24,34,2,'kaaklijn rechts doorlopend (model i100 j79-80)'); z(29,31,2,'kaaklijn doorlopend tussen (28,32) en (30,30)')
z(25,22,4,'losse 3 aan de linkerrand (modellijn) -> 4 zoals (26,22)')
for (y,x),(v,k) in E.items():
  assert m[y,x], (y,x)
  o[y,x]=v
np.save(sys.argv[2]+'.npy',o)
af=[(y,x,'%x'%meet[y,x],'%x'%o[y,x],E.get((y,x),('',''))[1]) for y,x in zip(*np.where(m)) if meet[y,x]!=o[y,x]]
print('afwijkend van de meting:',len(af))
for t in af: print(t)
