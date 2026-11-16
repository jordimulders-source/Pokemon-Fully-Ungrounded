# Pitahaya-draak r2: alleen de benoemde reparaties op r1 (coordinator ronde 2). Niets getekend.
#  1 VULLING: toonkaart van het model (luminantie per kleurgroep gladgestreken met een gauss, sigma S natieve px,
#    genormaliseerd binnen de groep), gemiddeld per 3x3-blok en gekwantiseerd naar de modeltinten van die groep.
#    Alleen vulpixels; bevroren: silhouet, buitenlijn (randpixels), lijnen (zwart), binnenlijnen (regel 4: mondlijn,
#    schubnaden, ribbels), amber, wit, mauve, gezichtsgebied x 18-34 / y 22-34.
#  2 SCHUBRANDEN rechts (x 39-45, y 8-30): zwarte binnenpixels (geen randpixel) waar het model een dunne lijn heeft
#    (<= 3 zwarte modelpx in het blok = hooguit 1 modelrij) -> donkerste tint van de omringende groep (roze 2 / groen 8).
#  3 PALET: groene tinten alleen in waarde (0 px), stappen naar 30-40 helderheid, kleuraard gelijk.
import sys,numpy as np; from PIL import Image, ImageFilter; from collections import Counter
from groepen import laad
S=float(sys.argv[1]) if len(sys.argv)>1 else 3.5; SR=float(sys.argv[3]) if len(sys.argv)>3 else S; UIT=sys.argv[2] if len(sys.argv)>2 else 'pitahaya_r2.png'
R1=Image.open('pitahaya_r1.png'); r1=np.asarray(R1).astype(int); pal=R1.getpalette()
info=np.load('kaal_info.npz'); regel=info['regel']; nzw=info['nzw']; OY,OX,ymin,xmin,y0,x0=info['geo']
a,lum,g=laad(); o=r1.copy(); log=[]
def zet(y,x,v,stap):
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
def blok(Y,X):
    ny=OY+3*(Y-y0+ymin); nx=OX+3*(X-x0+xmin); return slice(ny,ny+3),slice(nx,nx+3)
GRP={**{i:2 for i in (2,3,4,5)},6:3,7:3,**{i:4 for i in (8,9,10,11)}}
P=np.array(pal[:48]).reshape(16,3); L=P@[0.299,0.587,0.114]
TONEN={2:[3,4,5],4:[8,9,10,11]}
# toonkaart per groep (genormaliseerde convolutie binnen de groep)
def gauss(x,S):
    r=int(3*S)+1; k=np.exp(-0.5*(np.arange(-r,r+1)/S)**2); k/=k.sum()
    y=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,x); return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,y)
TK={}
for k in (2,4):
    m=(g==k).astype(float); s_=SR if k==2 else S; TK[k]=gauss(lum*m,s_)/np.maximum(gauss(m,s_),1e-6)
m=r1>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
def gezicht(y,x): return 18<=x<=34 and 22<=y<=34
# 1
KAND={}
for y,x in zip(*np.where(m)):
    v=r1[y,x]
    if rand[y,x] or gezicht(y,x) or v not in GRP or GRP[v]==3 or regel[y,x]==4: continue
    k=GRP[v]; sl=blok(y,x); gm=g[sl]==k
    if not gm.any(): continue
    KAND.setdefault(k,[]).append((TK[k][sl][gm].mean(),y,x))
# kwantiseren: drempels uit de eigen toonverdeling van r1 (zelfde aantal px per tint als de kale reductie gaf,
#   dus evenveel licht en schaduw = volume blijft), plaatsing volgt de gladde toonkaart van het model
for k,lst in KAND.items():
    t=TONEN[k]; n=Counter(r1[y,x] for _,y,x in lst); lst.sort()
    i=0
    for tt in t:
        for _ in range(n.get(tt,0)): _,y,x=lst[i]; zet(y,x,tt,'1'); i+=1
# 1b losse toonpixels die de toonkaart achterlaat (4-verbonden cluster van 1 vulpixel, niet in het gezicht/op de rand)
#    -> meest voorkomende 4-buur uit dezelfde kleurgroep (alleen tinten 3-5 / 9-11)
if '--zonder-1b' not in sys.argv:
    VUL={3,4,5,9,10,11}
    for y,x in zip(*np.where(m)):
        v=o[y,x]
        if v not in VUL or rand[y,x] or gezicht(y,x): continue
        nb4=[o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
        if v in nb4: continue
        c=Counter(b for b in nb4 if b in VUL and GRP[b]==GRP[v])
        if c: zet(y,x,c.most_common(1)[0][0],'1b')
# 2
for y in range(8,31):
    for x in range(39,46):
        if o[y,x]!=1 or rand[y,x] or nzw[y,x]>3: continue
        nb=Counter(GRP[o[y+dy,x+dx]] for dy in (-1,0,1) for dx in (-1,0,1) if o[y+dy,x+dx] in GRP)
        if not nb: continue
        k=nb.most_common(1)[0][0]; zet(y,x,2 if k in (2,3) else 8,'2')
# 3 palet (waarden alleen)
NIEUW={8:(48,80,52),10:(115,147,101),11:(155,183,134)}
for i,c in NIEUW.items(): pal[3*i:3*i+3]=list(c)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
def zone(y,x,v):
    if y<=36: return 'schubpunten' if GRP.get(v)==4 else 'hoofd/gezicht'
    if y>=48 and 19<=x<=44: return 'poten'
    if x<=22 or x>=39: return 'armen'
    return 'lijf'
cnt=Counter((s,zone(y,x,a_)) for s,y,x,a_,b in log)
for k,v in sorted(cnt.items()): print(k,v)
print('S groen',S,'roze',SR,'gewijzigd',len(log),'silhouet-diff',((o>0)!=(r1>0)).sum(),'gezicht-diff',sum(1 for _,y,x,_a,_b in log if gezicht(y,x)))
if UIT=='pitahaya_r2.png': open('afwijkingen_r1.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a_}->{b}\t{zone(y,x,a_)}' for s,y,x,a_,b in log)+'\n')
