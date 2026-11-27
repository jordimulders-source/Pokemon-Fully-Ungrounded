# r4 hoofd: gezicht GELIJK vergroot (1,28 x 1,28; hoofdgroot.py 1.28 1.28 62 16 -> r4/natief_g2.png), dan
# (1) zone = cellen waar natief_g1 en natief_g2 verschillen of die gezicht zijn -> kale reductie r4/basis.npy (kaprand, omlijning)
# (2) gezichtscellen: tint uit de hi-res modelmediaan zonder lijnpixels (r4/lijnkaart.py, zelfde mapping 1,28)
# (3) lijnen en ogen op de gemeten modelplek (zie verslag). Gebruik: python3 r4/hoofd.py VARIANT(1/2) UIT.npy
import sys; sys.path.insert(0,'r2'); sys.path.insert(0,'r4'); from gemeen import *; from PIL import Image
import lijnkaart as LK
VAR=sys.argv[1]; UIT=sys.argv[2]
o=np.load('r3/pachamama_r3.npy'); r3=o.copy(); log={}
def zet(c,v,k):
  if o[c]!=v: o[c]=v; log[k]=log.get(k,0)+1
g1=np.asarray(Image.open('natief_g1.png').convert('RGB')).astype(int); g2=np.asarray(Image.open('r4/natief_g2.png').convert('RGB')).astype(int)
z1=np.load('natief_g1_gez.npy'); z2=np.load('r4/natief_g2_gez.npy'); B=np.load('r4/basis.npy'); MY,MX=-21,-2
def bl(y,x): return (slice(max(MY+3*y,0),max(MY+3*y+3,0)),slice(max(MX+3*x,0),MX+3*x+3))
gez=np.zeros((64,64),bool); zone=np.zeros((64,64),bool)
for y in range(5,40):
  for x in range(10,50):
    b=bl(y,x); gez[y,x]=z2[b].sum()>=5
    zone[y,x]=gez[y,x] or z1[b].sum()>=3 or (g1[b]!=g2[b]).any()
# (1) buiten het gezicht in de zone: kale reductie (r2-palet: 7 -> gedeelde donkere 2; 9 -> roze schaduw)
for y,x in zip(*np.where(zone&~gez)):
  v=B[y,x]; v={7:2}.get(v,v); zet((y,x),v,'zone: kale reductie (kaprand/omlijning)')
# lijn gezicht-kap: elke zonecel buiten het gezicht die (4-buren) aan het gezicht grenst wordt zwart (model: dikke zwarte lijn rondom)
for y,x in zip(*np.where(zone&~gez)):
  if any(gez[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): zet((y,x),1,'lijn gezicht-kap (zwart)')
# (2) gezichtstinten
for y,x in zip(*np.where(gez)):
  b=LK.blok(y,x); v=LK.L[b][~LK.lijn[b]]
  if len(v)<4: continue
  m=np.median(v); t=2 if m<86 else 3 if m<116 else 4 if m<156 else 13
  zet((y,x),t,'gezicht: tint uit model')
# (3) lijnen (tint 2, gemeten in r4/lijnkaart.py op 2x2-subcellen)
L2={'neus R':[(18,28),(19,28),(20,28)],'neusbasis':[(21,27),(21,28)],
    'mond (∩)':[(23,27),(23,28),(23,29),(24,26),(25,26),(26,25),(27,25),(24,30),(25,31),(26,31),(27,31)],
    'wang L':[(22,23),(23,24),(24,24)],'wang R':[(20,34),(21,33),(22,32),(23,32)]}
for k,ps in L2.items():
  for c in ps: zet(c,2,'lijn '+k)
# ogen: rond en open, pupil hoog, lichtpixel; deksel 1 rij hoger dan het model (r16), zoals gevraagd
if VAR=='1':   # wenkbrauw op modelplek (rij 15, tint 3), lichtpixel op de modelplek (linksboven in de iris)
  E={(15,30):3,(15,31):3,(15,32):3,(15,33):3,(15,34):3,(15,35):3,(15,25):3,(15,26):3,
     (16,30):4,(16,31):2,(16,32):1,(16,33):1,(16,34):2,(16,35):3,
     (17,31):1,(17,32):5,(17,33):2,(17,34):1,(18,31):5,(18,32):2,(18,33):2,(18,34):5,(19,31):4,(19,32):5,(19,33):5,(19,34):4,
     (16,24):2,(16,25):1,(16,26):2,(17,24):1,(17,25):5,(17,26):1,(18,24):5,(18,25):2,(18,26):5,(19,24):4,(19,25):5,(19,26):4}
else:          # wenkbrauw hoger (rij 14) met lichte tint 4 ertussen (rij 15); lichtpixel in de onderhoek van de pupil
  E={(14,30):3,(14,31):3,(14,32):3,(14,33):3,(14,34):3,(14,25):3,(14,26):3,
     (15,30):4,(15,31):4,(15,32):4,(15,33):4,(15,34):4,(15,35):3,(15,25):4,(15,26):4,
     (16,30):4,(16,31):2,(16,32):1,(16,33):1,(16,34):2,(16,35):3,
     (17,31):1,(17,32):2,(17,33):2,(17,34):1,(18,31):5,(18,32):2,(18,33):13,(18,34):5,(19,31):4,(19,32):5,(19,33):5,(19,34):4,
     (16,24):2,(16,25):1,(16,26):2,(17,24):1,(17,25):2,(17,26):1,(18,24):5,(18,25):13,(18,26):5,(19,24):4,(19,25):5,(19,26):4}
for c,v in E.items(): zet(c,v,'oog/wenkbrauw variant '+VAR)
zet((20,31),3,'onderooglijn R (model, zacht in tint 3)'); zet((20,32),3,'onderooglijn R (model, zacht in tint 3)')
from clusters import vlakjes
vast=set(E)|{c for ps in L2.values() for c in ps}|{(20,31),(20,32)}
for it in range(2):
  for v,comp in vlakjes(o):
    if v not in (3,4,13): continue
    for c in comp:
      if not gez[c] or c in vast: continue
      nb=[o[q] for q in ((c[0]+1,c[1]),(c[0]-1,c[1]),(c[0],c[1]+1),(c[0],c[1]-1)) if gez[q] and q not in vast and o[q] in (3,4,13) and o[q]!=v]
      if nb: zet(c,max(set(nb),key=nb.count),'gezicht: vlakje <3 px -> buurtint')
np.save(UIT,o); np.save('r4/hoofdzone.npy',zone|gez)
for k,v in sorted(log.items()): print('%4d  %s'%(v,k))
print('hoofd: gewijzigd t.o.v. r3',int((o!=r3).sum()))
