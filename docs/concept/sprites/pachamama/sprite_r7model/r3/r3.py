# r3: bouwt vanaf r2/pachamama_r2.npy. Elke wijziging geteld per zone (log). Gebruik: python3 r3/r3.py OOGVARIANT(A/B/C)
import sys; sys.path.insert(0,'r2'); sys.path.insert(0,'r3'); from gemeen import *; from PIL import Image
from clusters import vlakjes
import rompmeet as RM
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
o=np.load('r2/pachamama_r2.npy'); r2=o.copy(); log={}
def zet(c,v,k):
  if o[c]!=v: o[c]=v; log[k]=log.get(k,0)+1
# ---------- palet (punt 3): 2 en 7 delen (90,64,57); index 7 vrij -> roze licht; 9 = roze schaduw ----------
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104)
for c in zip(*np.where(o==7)): zet(c,2,'rood donker 7 -> gedeelde donkere tint 2')
# roze per pixel op modelhelderheid (mediaan 3x3 natief)
a=np.asarray(Image.open('natief_g1.png').convert('RGB')).astype(float); MY,MX=-21,-2
def mmed(y,x):
  b=(slice(max(MY+3*y,0),max(MY+3*y+3,0)),slice(max(MX+3*x,0),MX+3*x+3)); return np.median(a[b].reshape(-1,3),0)
for c in zip(*np.where(r2==9)):
  if lum(mmed(*c))>=133: zet(c,7,'roze -> licht (model)')
for it in range(2):
  for v,comp in vlakjes(o):
    if v not in (7,9): continue
    for p in comp:
      nb=[o[q] for q in ((p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)) if o[q] in (7,9) and o[q]!=v]
      if nb: zet(p,nb[0],'roze vlakje <3 px -> andere roze')
# ---------- gezicht onderste helft (punt 1+2): vlakken uit de modelmediaan (hi-res, zonder lijnpixels), dan lijnen ----------
# kolommen 23..34; L = lijn (tint 2), getal = tint (4 midden, 3 donker, l = 13 licht). Bron: tabel lijnkaart.py (modelmediaan
# per cel, grenzen 88/122/152) met de lijnen op de gemeten modelplek (zie verslag).
F={21:'L44LL344444L4'[:0]}
F={21:[3,4,4,'N','N',4,4,4,4,4,'L',4],
   22:['L',4,4,4,4,4,4,4,4,4,'L',4],
   23:['L',4,4,'M','M','M',4,4,4,'L',3,3],
   24:['L',3,'M','l','l',4,'M',4,4,'L',3,3],
   25:[4,4,'M','l',4,4,4,'M',3,3,3,3],
   26:[3,4,'M',4,4,4,4,3,'M',3,3,3],
   27:[3,3,'M',4,4,3,3,3,'M',3,3,3],
   28:[None,3,4,4,3,3,3,3,3,3,None,None]}
for y,r in F.items():
  for i,v in enumerate(r):
    if v is None: continue
    c=(y,23+i); t={'L':2,'N':2,'M':2,'l':13}.get(v,v)
    k={'L':'wanglijn','N':'neusbasis','M':'mond (∩)','l':'vlak licht'}.get(v,'vlak tint %d'%t)
    zet(c,t,'gezicht: '+k)
# wanglijn R begint bij (20,34) zoals r2; wanglijn L (21,23) sluit aan op de oogkas (r2)
zet((20,34),2,'gezicht: wanglijn')
# tintvlakjes < 3 px die de nieuwe vlakken gaven -> aansluiten op de buurtint
for c,v in {(21,23):4,(24,24):4,(21,34):3,(22,34):3}.items(): zet(c,v,'gezicht: vlakje <3 px -> buurtint')
# ---------- ogen (punt 5 + Jordi "kijken nog wat verveeld"): open, dun gebogen bovenlid, wit aan beide kanten ----------
def oog(var):
  # rechteroog kol 30-33, linkeroog kol 24-26. Rij 16 = deksel boven (boog), wit links/rechts op rij 18-19, onder rij 20.
  lid=1; hoek=1 if var!='C' else 2
  R={(16,30):2,(16,31):lid,(16,32):lid,(16,33):2,(17,30):hoek,(17,33):hoek,
     (18,30):5,(18,33):5,(19,30):5,(19,33):5,(20,30):4,(20,31):5,(20,32):5,(20,33):4}
  Li={(16,24):2,(16,25):lid,(16,26):2,(17,24):hoek,(17,26):hoek,(18,24):5,(18,26):5,(19,24):5,(19,26):5,(20,24):2,(20,25):5,(20,26):13}
  # iris donker (3) met pupil (2), zoals het modeloog: grote donkere iris die tegen het deksel komt
  if var=='A': iR={(17,31):3,(17,32):3,(18,31):2,(18,32):2,(19,31):3,(19,32):3}; iL={(17,25):3,(18,25):2,(19,25):3}
  else:        iR={(17,31):2,(17,32):2,(18,31):2,(18,32):3,(19,31):3,(19,32):3}; iL={(17,25):2,(18,25):2,(19,25):3}
  return {**R,**Li,**iR,**iL}
for c,v in oog(VAR).items(): zet(c,v,'oog variant '+VAR)
# ---------- oker en turquoise (punt 4) ----------
m=o>0; p=np.pad(m,1); rand=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
OK,TQ=(11,12),(14,15)
def groep(c):
  nb=[o[q] for q in ((c[0]+1,c[1]),(c[0]-1,c[1]),(c[0],c[1]+1),(c[0],c[1]-1)) if o[q]>2]
  if nb and all(v in OK+TQ for v in nb):
    return OK if sum(v in OK for v in nb)>=sum(v in TQ for v in nb) else TQ
def plant(c): return 47<=c[0]<=51 and 10<=c[1]<=17
Lf=np.zeros((64,64))
for y in range(33,64):
  for x in range(64):
    if m[y,x]: Lf[y,x]=RM.lijnfr(y,x)
# lijnketens (>=3 cellen met lijnaandeel >=.25, 8-samenhang) = modellijnen
lc=(Lf>=.25)&~rand; lab=np.zeros((64,64),int); n=0; sz={}
for y in range(64):
  for x in range(64):
    if lc[y,x] and not lab[y,x]:
      n+=1; st=[(y,x)]; lab[y,x]=n; k=0
      while st:
        q=st.pop(); k+=1
        for dy in (-1,0,1):
          for dx in (-1,0,1):
            r=(q[0]+dy,q[1]+dx)
            if 0<=r[0]<64 and 0<=r[1]<64 and lc[r] and not lab[r]: lab[r]=n; st.append(r)
      sz[n]=k
islijn=lambda c: lab[c]>0 and sz[lab[c]]>=3
def toon(c,g):
  md=RM.med(*c); return g[int(np.argmin([((md-np.array(PAL[i]))**2).sum() for i in g]))]
o0=o.copy()
for y in range(36,63):
  for x in range(64):
    c=(y,x)
    if rand[c] or plant(c) or y<40 and x>=37: continue
    v=o0[c]
    if v in (1,2):
      g=groep(c)
      if g is None: continue
      if islijn(c): zet(c,g[0],'oker/turq: donker op modellijn -> donkerste eigen tint')
      else: zet(c,toon(c,g),'oker/turq: losse donkere vlek -> modeltint')
    elif v==11 and not islijn(c) and Lf[c]<.1 and toon(c,OK)==12: zet(c,12,'oker: donker blokje zonder modelvorm -> licht')
    elif v==15 and islijn(c) and groep(c)==TQ: zet(c,14,'turq: modellijn -> donkerste turquoise')
    elif v==14 and not islijn(c) and Lf[c]<.1 and toon(c,TQ)==15: zet(c,15,'turq: donker blokje zonder modelvorm -> licht')
# vlakjes < 3 px in oker/turquoise (geen lijnpixels) -> meest voorkomende buurtint van dezelfde groep
for it in range(2):
  for v,comp in vlakjes(o):
    if v not in OK+TQ: continue
    g=OK if v in OK else TQ
    for c in comp:
      if c[0]<33 or islijn(c) or plant(c): continue
      nb=[o[q] for q in ((c[0]+1,c[1]),(c[0]-1,c[1]),(c[0],c[1]+1),(c[0],c[1]-1)) if o[q] in g and o[q]!=v]
      if nb: zet(c,max(set(nb),key=nb.count),'oker/turq: vlakje <3 px -> buurtint')
np.save('r3/pachamama_r3%s.npy'%('' if VAR=='A' else '_'+VAR),o)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL3 for v in c]+[0]*(768-48))
im.save('r3/pachamama_r3%s.png'%('' if VAR=='A' else '_'+VAR),transparency=0)
for k,v in sorted(log.items()): print('%4d  %s'%(v,k))
print('totaal gewijzigd t.o.v. r2:',int((o!=r2).sum()),' kleuren:',len(set(o.ravel())))
