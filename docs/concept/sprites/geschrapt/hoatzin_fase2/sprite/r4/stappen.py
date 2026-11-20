# Hoatzin r1: stap A (zones/tonen -> palet), B (technisch: buitenlijn, losse lijnpixels, ontkorrelen), C (oog)
# Elke wijziging t.o.v. stap A wordt per zone geteld. Niets met de hand getekend: alleen regels op gemeten modelzones.
import json, numpy as np; from PIL import Image
Z=np.load('zone_t.npy'); C=np.load('col_t.npy'); L=C.mean(2); FK=np.load('fk_t.npy'); FW=np.load('fw_t.npy')
TH,TW=Z.shape; X0=(64-TW)//2; Y0=64-TH
PAL=[(152,208,160),(30,18,32),
     (50,30,48),(90,62,82),(128,98,118),(178,148,170),     # 2-5 mauve lijf/vleugel/staart
     (100,52,32),(152,82,44),                              # 6-7 kuif bruin
     (52,62,144),(98,116,214),                             # 8-9 blauw gezicht
     (208,52,76),                                          # 10 oog rood
     (122,82,112),(142,98,128),(165,122,152),              # 11-13 buik #7A5270 #8E6280 #A57A98
     (88,84,106),(134,130,152)]                            # 14-15 grijs snavel/poten
def toon(z,l):
    if z=='K': return 1
    if z=='W': return 5
    if z=='D': return 2 if l<42 else 3
    if z=='M': return 2 if l<64 else 3 if l<92 else 4 if l<122 else 5
    if z=='C': return 6 if l<62 else 7
    if z=='F': return 8 if l<90 else 9
    if z=='E': return 10
    if z=='P': return 11 if l<95 else 12 if l<124 else 13
    if z in 'TS': return 14 if l<88 else 15
    return 0
A=np.zeros((TH,TW),int)
for y in range(TH):
  for x in range(TW): A[y,x]=toon(Z[y,x],L[y,x])
# vleugelstrepen: alleen de kernen (>= 55 % streep in de cel) in de lichtste tint, de rest een tint lager (opdracht 6: geen zebra/vlekken)
WK=float(__import__('os').environ.get('WK',0.6))
A[(Z=='W')&(FW<WK)]=4
np.save('stapA.npy',A)
GRP={1:'K',2:'M',3:'M',4:'M',5:'M',6:'C',7:'C',8:'F',9:'F',10:'E',11:'P',12:'P',13:'P',14:'T',15:'T'}
DONKER={'W':3,'M':2,'D':2,'C':6,'F':8,'E':10,'P':11,'T':14,'S':14}
S=A.copy(); log={}
def zet(y,x,v,regel):
    if S[y,x]!=v:
        log.setdefault(regel,{}); z=Z[y,x]; log[regel][z]=log[regel].get(z,0)+1; S[y,x]=v
fg=A>0
N4=((-1,0),(1,0),(0,-1),(0,1))
def nb(y,x,d=N4):
    for dy,dx in d:
        if 0<=y+dy<TH and 0<=x+dx<TW: yield y+dy,x+dx,S[y+dy,x+dx]
        else: yield y+dy,x+dx,0
# B1: binnenlijn alleen waar het model echt zwart is (>=55 % zwart in de cel); anders donkerste tint van de buurzone
for y in range(TH):
  for x in range(TW):
    if A[y,x]==1 and all(v>0 for _,_,v in nb(y,x)) and FK[y,x]<0.55:
        zs=[Z[a,b] for a,b,v in nb(y,x,[(i,j) for i in (-1,0,1) for j in (-1,0,1) if i or j]) if v>1]
        zz=max(set(zs),key=zs.count) if zs else 'M'
        zet(y,x,DONKER.get(zz,2),'B1 binnenlijn->donkere tint (model <55% zwart)')
# B2: losse zwarte binnenpixel zonder zwarte 8-buur -> donkere tint
for y in range(TH):
  for x in range(TW):
    if S[y,x]==1 and all(v>0 for _,_,v in nb(y,x)):
        n8=[v for _,_,v in nb(y,x,[(i,j) for i in (-1,0,1) for j in (-1,0,1) if i or j])]
        if n8.count(1)==0: zet(y,x,DONKER.get(Z[y,x] if Z[y,x]!='K' else 'M',2),'B2 losse zwarte pixel')
# B3: ontkorrelen: vulpixel zonder enige 4-buur van dezelfde tint en met >=3 buren van één andere tint in dezelfde groep -> die tint
for _ in range(2):
  for y in range(TH):
    for x in range(TW):
      v=S[y,x]
      if v<=1 or v==10: continue
      ns=[w for _,_,w in nb(y,x)]
      if v in ns: continue
      same=[w for w in ns if w>1 and GRP.get(w)==GRP.get(v)]
      if same:
          w=max(set(same),key=same.count)
          if same.count(w)>=3: zet(y,x,w,'B3 ontkorrelen')
# B5: clusterfilter (Krassault): vulclusters < 3 px (4-verbonden, zelfde tint) nemen de meest voorkomende buurtint van dezelfde kleurgroep aan; kuifstrengen en oog uitgezonderd
MINC=int(__import__('os').environ.get('MINC',3))
def clusters():
    seen=np.zeros_like(S,bool); out=[]
    for y in range(TH):
      for x in range(TW):
        v=S[y,x]
        if v>1 and not seen[y,x]:
          st=[(y,x)];c=[];seen[y,x]=1
          while st:
            a,b=st.pop();c.append((a,b))
            for d,e in N4:
              p,q=a+d,b+e
              if 0<=p<TH and 0<=q<TW and S[p,q]==v and not seen[p,q]: seen[p,q]=1;st.append((p,q))
          out.append((v,c))
    return out
for _ in range(3):
  for v,c in clusters():
    if len(c)>=MINC or GRP.get(v) in ('C','E','F'): continue
    buur=[]
    for a,b in c:
        for p,q,w in nb(a,b):
            if w>1 and w!=v and GRP.get(w)==GRP.get(v): buur.append(w)
    if buur:
        w=max(set(buur),key=buur.count)
        for a,b in c: zet(a,b,w,'B5 clusterfilter <3 px')
# B4: buitenlijn (1 px, binnen het silhouet): lichtkant (achtergrond boven/links) gekleurde selout, schaduwkant zwart; kuif altijd donkerbruin
for y in range(TH):
  for x in range(TW):
    if not fg[y,x]: continue
    bgd=[(dy,dx) for dy,dx in N4 if not (0<=y+dy<TH and 0<=x+dx<TW and fg[y+dy,x+dx])]
    if not bgd: continue
    z=Z[y,x]
    if z=='C': zet(y,x,6,'B4 buitenlijn'); continue
    if z=='W': z='M'
    if z=='E': continue
    licht=sum(-dy-dx for dy,dx in bgd)>0 and x<TW*0.62 and y<TH*0.75
    if licht and z!='K': zet(y,x,DONKER.get(z,2) if z not in 'MD' else 3,'B4 buitenlijn')
    else: zet(y,x,1,'B4 buitenlijn')
# B6: rand zonder om-en-om: randpixel waarvan de randburen (8-buren op de rand) in meerderheid de andere randsoort zijn, neemt die over
rand=np.zeros((TH,TW),bool)
for y in range(TH):
  for x in range(TW):
    if fg[y,x] and any(not (0<=y+dy<TH and 0<=x+dx<TW and fg[y+dy,x+dx]) for dy,dx in N4): rand[y,x]=True
SEL={3,8,11,14}
for _ in range(2):
  for y in range(TH):
    for x in range(TW):
      if not rand[y,x] or Z[y,x] in 'CE': continue
      v=S[y,x]
      if v!=1 and v not in SEL: continue
      rb=[S[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<TH and 0<=x+dx<TW and rand[y+dy,x+dx] and Z[y+dy,x+dx] not in 'CE']
      zw=sum(1 for w in rb if w==1); se=[w for w in rb if w in SEL]
      if v in SEL and zw>=2 and len(se)==0: zet(y,x,1,'B6 rand: losse selout tussen zwart -> zwart')
      elif v==1 and len(se)>=2 and zw==0: zet(y,x,max(set(se),key=se.count),'B6 rand: los zwart tussen selout -> selout')
# C: oog = rood (model: roze ring, donkere kern); donkerste oogpixel wordt het zwarte puntje
ey,ex=np.where(Z=='E'); i=np.argmin(L[ey,ex]); zet(ey[i],ex[i],1,'C oog pupil (donkerste modelpixel)')
# C2: oog rond maken naar het model (modeloog: midden op x 6,4 / y 20,6, ringrand tot y 21,8): 3x3 rond de pupil, ringpixels buiten het oog -> blauw
import os
py,px=ey[i],ex[i]
for y,x in zip(ey,ex):
    if abs(y-py)>1 or abs(x-px)>1: zet(y,x,9 if L[y,x]>=90 else 8,'C2 oog: modelringrand buiten 3x3 -> blauw')
for dy in (-1,0,1):
  for dx in (-1,0,1):
    if dy or dx:
        hoek=dy and dx
        v=10
        if os.environ.get('OOG','A')=='B' and hoek and dy>0: v=8
        zet(py+dy,px+dx,v,'C2 oog 3x3 rond de pupil (model)')
np.save('stapS.npy',S)
im=np.zeros((64,64),'uint8'); im[Y0:Y0+TH,X0:X0+TW]=S
p=Image.fromarray(im,'P'); p.putpalette([c for t in PAL for c in t]); p.save('hoatzin.png',transparency=0)
open('normal.pal','w').write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%c for c in PAL))
json.dump(log,open('log.json','w'),indent=1,ensure_ascii=False)
for r,d in log.items(): print(r,d,sum(d.values()))
print('afwijkend van stap A:',int((S!=A).sum()),'silhouet-diff:',int(((S>0)!=(A>0)).sum()),'kleuren',len(set(S.ravel())))
for y in range(TH): print('%2d '%y+''.join('.' if v==0 else '0123456789abcdef'[v] for v in S[y]))
