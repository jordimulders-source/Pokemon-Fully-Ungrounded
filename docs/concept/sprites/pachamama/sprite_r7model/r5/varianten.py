# r5: 4 hoofdvarianten vanaf r4 v1 (romp ongewijzigd). Alleen gezicht. Gebruik: python3 r5/varianten.py
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104)
r4=np.load('r4/pachamama_r4.npy')
def buur(o,c,weg):
  nb=[o[c[0]+a,c[1]+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if o[c[0]+a,c[1]+b] in (3,4,13) and (c[0]+a,c[1]+b) not in weg]
  return max(set(nb),key=nb.count) if nb else 3
def A(o):  # pupillen recht vooruit, midden van het oog: iris boven (3, lichtpixel 13 linksboven), pupil midden, wit onder
  for c,v in {(17,32):13,(17,33):3,(18,32):2,(18,33):2,(19,32):5,(19,33):5,(17,25):3,(18,25):2,(19,25):5}.items(): o[c]=v
def B(o):  # poten recht omlaag, schouders korter (bovenlijn blijft (23,27-29))
  weg=[(25,25),(26,25),(27,25),(25,31),(26,31),(27,31)]
  for c in [(24,26),(25,26),(26,26),(27,26),(24,30),(25,30),(26,30),(27,30)]: o[c]=2
  for c in weg: o[c]=buur(o,c,weg)
def C(o):  # bovenlijn van de ∩ in tint 3 (baardplooi), poten blijven 2
  for c in [(23,27),(23,28),(23,29)]: o[c]=3
def D(o):  # wenkbrauw neutraal: vlak, alleen boven het oog, geen schuine donkere deksel-uiteinden
  for c in [(15,30),(15,35)]: o[c]=buur(o,c,[])
  for c in [(15,31),(15,32),(15,33),(15,34),(15,25),(15,26)]: o[c]=3
  for c in [(16,31),(16,34),(16,24),(16,26)]: o[c]=3
  o[(16,30)]=4; o[(16,35)]=buur(o,(16,35),[])
V={'A':[A],'B':[A,B],'C':[A,C],'D':[A,B,D]}
for k,fs in V.items():
  o=r4.copy()
  for f in fs: f(o)
  np.save('r5/pachamama_r5_%s.npy'%k,o)
  im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL3 for v in c]+[0]*(768-48)); im.save('r5/pachamama_r5_%s.png'%k,transparency=0)
  print(k,'gewijzigd t.o.v. r4 v1:',int((o!=r4).sum()),'kleuren',len(set(o.ravel())))
