# Pitahaya-draak r6 op af/pitahaya_draak.png. Niets getekend; elke wijziging met modelmeting.
#  1 ARM: gat tussen rechterarm en romp uit het model (natieve pixels van de achtergrondkleur, ingesloten door zwart,
#    in de groep 'wit' van groepen.py) -> transparant bij >= 3/9 zulke px; randpixels eromheen -> lijn
#    (zwart waar het model >= 2 zwarte px heeft, anders donkerste groen); lijnstuk (38,45) uit het model.
#  2 GROEN TOONKAART: binnenpixels van het lijf/armen/poten (groen, geen rand, geen echte lijn) opnieuw uit de
#    gladde toonkaart van het model (sigma S), drempels uit de eigen toonverdeling (zelfde aantal px per tint).
#    'Echte lijn' = blok met >= 3 modelpx lum < 62 (de ribbels/naden), die blijven.
#  3 PALET: groen naar Gen 3-verzadiging (Treecko/Cacnea 0,42-0,86; wij 0,27-0,40), helderheid en tint gelijk.
import sys,numpy as np; from PIL import Image; from collections import Counter
from groepen import laad
S=float(sys.argv[1]) if len(sys.argv)>1 else 2.0; UIT=sys.argv[2] if len(sys.argv)>2 else 'pitahaya_r6.png'
AF=Image.open('af.png'); af=np.asarray(AF).astype(int); pal=AF.getpalette()
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']; a,lum,g=laad()
o=af.copy(); log=[]
def zet(y,x,v,stap):
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
def blok(Y,X):
    ny=OY+3*(Y-y0+ymin); nx=OX+3*(X-x0+xmin); return slice(ny,ny+3),slice(nx,nx+3)
def nz(Y,X): return (g[blok(Y,X)]==1).sum()
# 1 arm
GAT=[]
for Y in range(39,46):
    for X in range(36,42):
        if (g[blok(Y,X)]==6).sum()>=3: GAT.append((Y,X))
for Y,X in GAT: zet(Y,X,0,'1 gat')
m=o>0
for Y,X in GAT:
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        y,x=Y+dy,X+dx
        if m[y,x] and o[y,x] not in (1,8,2): zet(y,x,1 if nz(y,x)>=1 else 8,'1 rand gat')
ZWART=[]
REP=[(45,38,8,'scheiding arm/romp: model heeft daar donkergroene px (lum < 85) tussen (38,44) en (39,46); maakt de lijn doorlopend')]
for y,x,v,r in REP: zet(y,x,v,'1 lijn')
# 2 groene toonkaart
m=o>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
def gauss(x,s):
    r=int(3*s)+1; k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    y=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,x); return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,y)
mg=(g==4).astype(float); TK=gauss(lum*mg,S)/np.maximum(gauss(mg,S),1e-6)
kand=[]
for y,x in zip(*np.where(m)):
    if y<37 or o[y,x] not in (8,9,10,11) or rand[y,x] or (y,x) in [(r[0],r[1]) for r in REP]: continue
    sl=blok(y,x); gm=g[sl]==4
    if not gm.any(): continue
    if ((lum[sl]<62)&(g[sl]!=1)).sum()+(g[sl]==1).sum()>=3: continue    # echte lijn in het model
    kand.append((TK[sl][gm].mean(),y,x))
MODE=sys.argv[3] if len(sys.argv)>3 else 'tint'
if MODE=='kwantiel':
    n=Counter(o[y,x] for _,y,x in kand); kand.sort(); i=0
    for t in (8,9,10,11):
        for _ in range(n.get(t,0)): _,y,x=kand[i]; zet(y,x,t,'2 toonkaart'); i+=1
else:   # dichtstbijzijnde modeltoon (helderheid van de groene modeltonen uit groepen.tonen: 73/98/123/158)
    ML=np.array([73,98,123,158])
    for l,y,x in kand: zet(y,x,(8,9,10,11)[int(np.abs(ML-l).argmin())],'2 toonkaart')
# 3 palet
P=np.array(pal[:48]).reshape(16,3).astype(float)
DOEL={8:0.48,9:0.45,10:0.42,11:0.36}
for i,s in DOEL.items():
    c=P[i]; L=c@[0.299,0.587,0.114]
    for _ in range(40):
        cur=(c.max()-c.min())/c.max(); 
        if abs(cur-s)<0.005: break
        c=L+(c-L)*(1+0.5*(s-cur)/max(cur,0.05)); c=np.clip(c,0,255)
    c=c+(L-c@[0.299,0.587,0.114])
    pal[3*i:3*i+3]=[int(round(v)) for v in np.clip(c,0,255)]
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
def zone(y,x):
    if y<=36: return 'kop'
    if 36<=x<=46 and 37<=y<=48: return 'rechterarm'
    if x<=22: return 'linkerarm'
    if y>=48: return 'poten'
    return 'romp'
cnt=Counter((s,zone(y,x)) for s,y,x,_,_ in log)
for k,v in sorted(cnt.items()): print(k,v)
fz=lambda y,x: 18<=x<=36 and 22<=y<=27
print('S',S,'gewijzigd',len(log),'in ooggebied',sum(fz(y,x) for _,y,x,_,_ in log),'gat',GAT)
for i in DOEL: print(i,pal[3*i:3*i+3])
if UIT=='pitahaya_r6.png': open('afwijkingen_af.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a_}->{b}\t{zone(y,x)}' for s,y,x,a_,b in log)+'\n')
