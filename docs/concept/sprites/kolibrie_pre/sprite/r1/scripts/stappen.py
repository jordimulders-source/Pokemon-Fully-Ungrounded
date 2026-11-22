# Stap B (technisch) en C (Gen 3-licht) op stap A. Elke wijziging wordt gelogd per zone en regel.
import numpy as np, json
A=np.load('stapA.npy'); Z=np.load('zone_t.npy'); TH,TW=A.shape
log={}
def zet(y,x,v,regel):
    if out[y,x]!=v:
        log.setdefault(regel,{}).setdefault(Z[y,x],0); log[regel][Z[y,x]]+=1; out[y,x]=v
out=A.copy()
fg=out>0
def nb(y,x,dy,dx): 
    yy,xx=y+dy,x+dx
    return out[yy,xx] if 0<=yy<TH and 0<=xx<TW else 0
# --- B1 spikkels: alleen enkele duidelijke pixels op de modelplekken (sterkste P-dekking, onderling >=2 px uit elkaar)
SC=np.load('spot_c.npy')   # (grootte, y, x): zwaartepunten van de modelspikkels op het natieve raster
keep=[(int(y),int(x)) for n,y,x in SC if n>=3]
for y in range(TH):
  for x in range(TW):
    if Z[y,x]=='P' and (y,x) not in keep: zet(y,x,6 if A[y,x] in (3,4) else A[y,x],'B1 spikkels uitdunnen')
    if Z[y,x]=='W' and (y,x) in keep: Z[y,x]='P'
big={(int(y),int(x)) for n,y,x in SC if n>=5}
for y,x in keep: zet(y,x,3 if (y,x) in big else 4,'B1 spikkel op modelplek')  # spikkel 4 bovenaan, lichter (5) naar beneden toe zoals het model vervaagt
# --- B2 buitenlijn: elke randpixel (grenst aan transparant) wordt lijn; lichtkant (lucht boven/links) gekleurde selout 2, schaduwkant 1
for y in range(TH):
  for x in range(TW):
    if not fg[y,x] or out[y,x] in (1,): continue
    up=nb(y,x,-1,0)==0; lf=nb(y,x,0,-1)==0; dn=nb(y,x,1,0)==0; rt=nb(y,x,0,1)==0
    if not (up or lf or dn or rt): continue
    if Z[y,x] in ('F','S','Y','E'): zet(y,x,1,'B2 buitenlijn'); continue
    licht=(up or lf) and not (dn or rt) and y<26
    zet(y,x,2 if licht else 1,'B2 buitenlijn')
np.save('stapB.npy',out.copy())
json.dump(log,open('log_B.json','w'),indent=1)
# ---------------- stap C: Gen 3-licht (bovenlaag); vorm/silhouet blijven
log={}
T=np.load('tone_t.npy')
spk=set(keep)
def binnen(y,x): return 0<=y<TH and 0<=x<TW
# C1 sikkelschaduw achter op kop en lijf: lila pixel direct links van de rechter (schaduwkant) buitenlijn -> 3
for y in range(0,19):
  for x in range(TW-1):
    if Z[y,x]=='L' and out[y,x] in (4,5) and out[y,x+1]==1 and (x+2>=TW or out[y,x+2]==0): zet(y,x,3,'C1 sikkel achter kop/lijf')
# C2 lichtere dekveren (modelplek met tone>=170 in de vleugelbult) -> 5
for y in range(10,19):
  for x in range(20,30):
    if Z[y,x]=='L' and out[y,x]==4 and T[y,x]>=168: zet(y,x,5,'C2 hooglicht dekveren (model)')
# C3 kinschaduw: eerste buikrij onder de kop -> 5
for y in range(8,11):
  for x in range(10,19):
    if out[y,x]==6 and binnen(y-1,x) and Z[y-1,x] in ('L','K','S','E','Y') : zet(y,x,5,'C3 kinschaduw')
# C5 buik onderrand rechts: 5 direct boven de onderste lijn, kolom>=18 -> 4 (sikkel)
for y in range(20,TH-1):
  for x in range(18,30):
    if Z[y,x]=='W' and out[y,x]==5 and out[y+1,x]==1: zet(y,x,4,'C5 sikkel onder buik')
# C6 vleugel: 8 direct boven/links van de onderste lijn -> 10 (sikkel onderrand) 
for y in range(TH-1):
  for x in range(TW):
    if Z[y,x]=='V' and out[y,x]==8 and (out[y+1,x]==1) : zet(y,x,10,'C6 sikkel onder vleugel')
# C7 gekleurde selout aan de lichtkant: buitenlijnpixels met lucht alleen links/boven, boven rij 22, niet snavel/oog/poot -> 2
for y in range(0,22):
  for x in range(TW):
    if out[y,x]!=1 or Z[y,x] in ('S','E','F','Y') or x<9 or y<8: continue
    up=binnen(y-1,x) and out[y-1,x]==0 or y==0; lf=binnen(y,x-1) and out[y,x-1]==0
    dn=binnen(y+1,x) and out[y+1,x]==0; rt=binnen(y,x+1) and out[y,x+1]==0
    if (up or lf) and not (dn or rt) and x<20: zet(y,x,2,'C7 selout lichtkant')
np.save('stapC.npy',out.copy())
json.dump(log,open('log_C.json','w'),indent=1)
# ---------------- stap D: snavel-selout en ontkorrelen
log={}
# D1 snavel (zone S/K in het snavelvak): bovenrand (lucht erboven) -> selout 2, behalve de punt (kolom 0-1)
for y in range(0,9):
  for x in range(2,13):
    if out[y,x]==1 and Z[y,x] in ('S','K') and binnen(y-1,x) and out[y-1,x]==0 and x<=y*2+2: zet(y,x,2,'D1 snavel bovenrand selout')
# D2 tintklontjes < 3 px nemen de meest voorkomende buurtint uit dezelfde groep aan (spikkels, oog, geel, poten, snavel vrij)
groep={3:'l',4:'l',5:'lw',6:'w',7:'w',8:'v',10:'v',2:'s'}
vrij=set(keep)
for ronde in range(3):
  seen=np.zeros((TH,TW),bool)
  for y in range(TH):
    for x in range(TW):
      v=out[y,x]
      if seen[y,x] or v not in (3,4,5,6,8,10) or Z[y,x] in ('E','Y','F','S','P'): continue
      st=[(y,x)]; pts=[]
      while st:
        a,b=st.pop()
        if binnen(a,b) and not seen[a,b] and out[a,b]==v:
          seen[a,b]=1; pts.append((a,b)); st+=[(a+dy,b+dx) for dy in (-1,0,1) for dx in (-1,0,1)]
      if len(pts)>=3 or any(p in vrij for p in pts): continue
      from collections import Counter
      c=Counter()
      for a,b in pts:
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
          if binnen(a+dy,b+dx) and out[a+dy,b+dx] in (3,4,5,6,8,10) and out[a+dy,b+dx]!=v and (a+dy,b+dx) not in vrij: c[out[a+dy,b+dx]]+=1
      if c:
        nv=c.most_common(1)[0][0]
        for a,b in pts: zet(a,b,nv,'D2 ontkorrelen')
# D3 wang tussen snavelbasis en oog: mengtint 3 uit de reductie (snavel + lila) -> lila 4 zoals het model daar is
for y in range(5,9):
  for x in range(13,19):
    if Z[y,x]=='L' and out[y,x]==3: zet(y,x,4,'D3 wang terug naar modeltint')
np.save('stapD.npy',out.copy())
json.dump(log,open('log_D.json','w'),indent=1)
