# meting r3 punt 3: welke paletkleur kan het best vrij voor een tweede roze tint? Fout = som over pixels van de afstand
# modelmediaan (3x3 natief) -> toegewezen paletkleur, alleen voor de pixels van de betrokken groep.
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('natief_g1.png').convert('RGB')).astype(float); MY,MX=-21,-2
o=np.load('r2/pachamama_r2.npy')
M=np.zeros((64,64,3))
for y in range(64):
  for x in range(64):
    b=(slice(max(MY+3*y,0),max(MY+3*y+3,0)),slice(max(MX+3*x,0),MX+3*x+3))
    if o[y,x]>1 and a[b].size: M[y,x]=np.median(a[b].reshape(-1,3),0)
def fout(groep,pal):
  m=np.isin(o,groep); v=M[m]; Q=np.array(pal,float); d=np.sqrt(((v[:,None]-Q[None])**2).sum(-1)); return d.min(1).sum(),m.sum()
PALr=dict(enumerate(PAL))
pl=(164,101,105); pd_=(190,128,130)
print('roze nu (1 tint):            %.0f'%fout([9],[PAL[9]])[0])
print('roze met 2 tinten:           %.0f'%fout([9],[pl,pd_])[0])
cases={
 'A rood donker 7 -> bruin 2 (rood)':([7,8],[PAL[2],PAL[8]],[7,8],[PAL[7],PAL[8]]),
 'D oker donker 11 -> bruin 2 (oker)':([11,12],[PAL[2],PAL[12]],[11,12],[PAL[11],PAL[12]]),
 'E rood donker 7 = roze schaduw (rood+roze)':([7,8,9],[PAL[8],pd_,(150,86,88)],[7,8,9],[PAL[7],PAL[8],pl,pd_]),
 'G rood midden 8 = roze licht (rood+roze)':([7,8,9],[PAL[7],pl,(186,112,106)],[7,8,9],[PAL[7],PAL[8],pl,pd_]),
 'H turq donker 14 -> 2 (turq)':([14,15],[PAL[2],PAL[15]],[14,15],[PAL[14],PAL[15]]),
 'I gezicht licht 13 -> 4/5 (gezicht+kap)':([2,3,4,13,5],[PAL[2],PAL[3],PAL[4],PAL[5]],[2,3,4,13,5],[PAL[2],PAL[3],PAL[4],PAL[13],PAL[5]]),
 'J blauwgrijs 6 -> 13/10 (sneeuw)':([6,10,13,5],[PAL[10],PAL[13],PAL[5]],[6,10,13,5],[PAL[6],PAL[10],PAL[13],PAL[5]]),
}
for k,(g,p,g0,p0) in cases.items():
  f,n=fout(g,p); f0,_=fout(g0,p0); print('%-45s extra fout %6.0f over %d px (%.1f/px)'%(k,f-f0,n,(f-f0)/n))
print('--- rood+roze absoluut (alle pixels 7,8,9; rest van het palet ongewijzigd) ---')
G=[7,8,9]
opties={
 'nu: 7,8,9 (roze 1 tint)':[PAL[7],PAL[8],PAL[9]],
 'ideaal 4 kleuren':[PAL[7],PAL[8],pl,pd_],
 'G: 8 = roze licht gedeeld':[PAL[7],pl,(186,112,106)],
 'E: 7 = roze schaduw gedeeld':[(150,86,88),PAL[8],pd_],
}
for k,p in opties.items(): print('%-35s %.0f'%(k,fout(G,p)[0]))
# A: 7 weg, rood donker -> 2 (bruin) of 1, roze 2 tinten
print('%-35s %.0f'%('A: 7 -> bruin 2, roze 2 tinten',fout(G,[PAL[2],PAL[8],pl,pd_])[0]))
print('--- alle paren samenvoegen tot 1 kleur (optimale gedeelde kleur = gewogen gemiddelde; extra modelfout) ---')
res=[]
FACE={2,3,4,13}; VAST={5,6,10}
for i in range(1,16):
  for j in range(i+1,16):
    if i in VAST or j in VAST: continue
    if i in FACE and j in FACE: continue
    if 9 in (i,j): continue
    m=np.isin(o,[i,j]); v=M[m]
    if i==1 or j==1: continue
    c=v.mean(0)
    for _ in range(5):   # geometrische mediaan
      d=np.sqrt(((v-c)**2).sum(1))+1e-6; c=(v/d[:,None]).sum(0)/(1/d).sum()
    f1=np.sqrt(((v-c)**2).sum(1)).sum(); f0=fout([i,j],[PAL[i],PAL[j]])[0]
    res.append((f1-f0,i,j,tuple(int(t) for t in c),m.sum()))
for r in sorted(res)[:8]: print('%2d+%2d -> %s  extra %.0f over %d px'%(r[1],r[2],r[3],r[0],r[4]))
print('--- index i vrijmaken: pixels naar dichtstbijzijnde overgebleven kleur (Lab-afstand, incl. de 2 nieuwe roze) ---')
def lab(c):
  c=np.asarray(c,float)/255; c=np.where(c>.04045,((c+.055)/1.055)**2.4,c/12.92)
  X=c@np.array([.4124,.2126,.0193]); Y=c@np.array([.3576,.7152,.1192]); Z=c@np.array([.1805,.0722,.9505])
  f=lambda t: np.where(t>.008856,np.cbrt(t),7.787*t+16/116); fx,fy,fz=f(X/.9505),f(Y),f(Z/1.089)
  return np.stack([116*fy-16,500*(fx-fy),200*(fy-fz)],-1)
for i in (7,8,11,12,14,15,3,13):
  rest=[PAL[j] for j in range(1,16) if j not in (i,9)]+[pl,pd_]
  d=np.sqrt(((lab(PAL[i])-lab(rest))**2).sum(-1)); j=d.argmin(); n=(o==i).sum()
  # ook: modelfout van die pixels voor/na
  m=o==i; v=M[m]; e0=np.sqrt(((lab(v)-lab(PAL[i]))**2).sum(-1)).mean(); e1=np.sqrt(((lab(v)-lab(rest[j]))**2).sum(-1)).mean()
  print('%2d %s n=%3d -> %s dE %.1f | modelfout per px %.1f -> %.1f | totaal extra %.0f'%(i,PAL[i],n,rest[j],d[j],e0,e1,(e1-e0)*n))
print('--- 2 en 7 delen een kleur: extra Lab-modelfout over alle 2- en 7-pixels (gezichtslijnen, donkerbruin romp, rode schaduw) ---')
m=np.isin(o,[2,7]); v=lab(M[m]); e0=np.where(o[m]==2,np.sqrt(((v-lab(PAL[2]))**2).sum(-1)),np.sqrt(((v-lab(PAL[7]))**2).sum(-1))).sum()
for c in [PAL[2],(88,64,56),(96,64,58),(104,66,60),(110,74,68)]:
  print('  gedeeld %s: extra %.0f over %d px'%(c,np.sqrt(((v-lab(c))**2).sum(-1)).sum()-e0,m.sum()))
