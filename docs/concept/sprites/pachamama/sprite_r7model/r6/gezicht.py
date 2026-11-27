# r6: gezicht opnieuw naar het model (uitsnede x330-640, y130-430), romp en kap = r4 v1. Elke cel benoemd per zone.
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104)
r4=np.load('r4/pachamama_r4.npy'); o=r4.copy(); log={}
def zet(c,v,k):
  if o[c]!=v: o[c]=v; log[k]=log.get(k,0)+1
# gezichtsmasker: binnen de zwarte lijn gezicht-kap (flood fill vanaf het midden, box r12-30 k21-37)
m=np.zeros((64,64),bool); st=[(22,29)]; m[22,29]=1
while st:
  y,x=st.pop()
  for a,b in ((1,0),(-1,0),(0,1),(0,-1)):
    q=(y+a,x+b)
    if 12<=q[0]<=30 and 21<=q[1]<=37 and not m[q] and (r4[q] in (2,3,4,13) or (r4[q]==5 and 17<=q[0]<=20 and 23<=q[1]<=35)): m[q]=1; st.append(q)
for c in [(16,30),(16,31),(16,32),(16,33),(16,34),(17,24),(17,25),(17,26),(17,30),(17,31),(17,32),(17,33),(17,34),(16,25),(16,32),(16,33)]: m[c]=True
rand=np.zeros((64,64),bool)
for y,x in zip(*np.where(m)): rand[y,x]=any(r4[y+a,x+b]==1 and not m[y+a,x+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)))
# 1. basis: bovenste helft licht (13), rand 4; onderste helft (baard) 3
for y,x in zip(*np.where(m)):
  if y<=15: zet((y,x),4 if rand[y,x] else 13,'voorhoofd licht')
  elif y<=22: zet((y,x),4,'wangen/neus basis 4')
  else: zet((y,x),3,'baardvlak 3')
for y,x in zip(*np.where(m)):
  if 16<=y<=26 and (rand[y,x] or x in (22,36,37)): zet((y,x),3,'zijrand schaduw 3')
# 2. oogkas-schaduw direct boven de ogen, neusrug licht, schaduwkant neus, neusonderkant (rij 21 = ±45 % gezichtshoogte)
for c in [(15,24),(15,25),(15,26),(15,30),(15,31),(15,32),(15,33),(15,34)]: zet(c,3,'oogkas-schaduw (direct boven het deksel)')
for y in range(15,21):
  for x in (27,28): zet((y,x),13,'neusrug licht')
  zet((y,29),3,'schaduwkant neus')
for c in [(21,27),(21,28),(21,29)]: zet(c,2,'neusonderkant')
for c in [(19,23),(20,23),(20,24),(20,25),(20,26),(21,24),(21,25)]: zet(c,13,'wang L onder het oog licht')
for c in [(20,30),(20,31),(20,32),(20,33)]: zet(c,13,'wang R onder het oog licht')
# 3. ogen: groot, amandel, overwegend wit, dik zwart bovenlid; iris donker met lichtpunt in de onderhoek
E={(16,30):1,(16,31):1,(16,32):1,(16,33):1,(16,34):1,
   (17,30):5,(17,31):5,(17,32):2,(17,33):2,(17,34):5,
   (18,30):4,(18,31):5,(18,32):13,(18,33):2,(18,34):5,
   (19,30):4,(19,31):5,(19,32):5,(19,33):5,(19,34):4,
   (16,24):1,(16,25):1,(16,26):1,(17,24):5,(17,25):2,(17,26):5,(18,24):5,(18,25):13,(18,26):5,(19,24):4,(19,25):5,(19,26):4,
   (16,23):3,(16,35):3,(17,23):3,(17,35):3,(18,35):3,(19,35):3}
for c,v in E.items(): zet(c,v,'oog')
# 4. snor/baard: brede lage boog van wang tot wang, uiteinden lopen door tot de zijkant van het gezicht (vast aan de omtrek)
SN=[(23,26),(23,27),(23,28),(23,29),(23,30),(23,31),(24,25),(25,24),(26,23),(27,22),(24,32),(25,33),(26,34),(27,35)]
for c in SN: zet(c,2,'snor/baardlijn')
for c in [(24,27),(24,28),(24,29),(24,30),(25,27),(25,28),(25,29)]: zet(c,4,'baard: lichte rotsvlak midden onder de snor')
for c in [(22,26),(22,27),(22,28),(22,29),(22,30),(22,31)]: zet(c,4,'bovenlip 4')
# baard: rotsvlakken uit de modeltinten van r4 (hoofd.py: hi-res modelmediaan); de oude ∩- en wanglijnen van r4 -> 3
OUD={(24,26),(25,26),(26,25),(27,25),(24,30),(25,31),(26,31),(27,31),(25,25),(22,23),(23,24),(24,24),(23,27),(23,28),(23,29)}
for y,x in zip(*np.where(m)):
  if y>=24 and (y,x) not in SN and not (24<=y<=25 and 27<=x<=30):
    v=r4[y,x]
    if (y,x) in OUD: v=3
    if v in (2,3,4): zet((y,x),v,'baard: rotsvlak uit modeltint (r4)')
from clusters import vlakjes
for v,comp in vlakjes(o):
  for c in comp:
    if m[c] and c[0]>=24 and c not in SN and v in (2,4): zet(c,3,'baard: vlakje <3 px -> 3')
np.save('r6/pachamama_r6.npy',o)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL3 for v in c]+[0]*(768-48)); im.save('r6/pachamama_r6.png',transparency=0)
for k,v in sorted(log.items()): print('%4d  %s'%(v,k))
print('gewijzigd t.o.v. r4 v1:',int((o!=r4).sum()),'buiten gezicht:',int(((o!=r4)&~m).sum()),'kleuren',len(set(o.ravel())))
