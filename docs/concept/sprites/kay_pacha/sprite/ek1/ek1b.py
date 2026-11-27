# ek1b: stap 2 na ek1.py (stap1.npy). Kop/hals per pixel naar het model, volume (Gen 3 zoals Raikou-poten) op de groene delen,
# mantelschaduw waar het model donker is, paars. Run vanuit docs/concept/sprites/kay_pacha: python3 sprite/ek1/ek1b.py
import sys, json, numpy as np; from PIL import Image
sys.path.insert(0,'sprite/ek1'); import ek1
from ek1 import S, B, FG, log, zet, PAL, save, D
G0=15
# ---- 3. kop/hals: lijnen 1 px, wie ervoor ligt bepaalt de lijnkleur (masker 9 > hals G0 boven de mantel; mantel 5 voor de hals eronder) ----
HAND=[ # (x,y,waarde,reden)
 (20,12,1,'groen stukje achter de kop: bovenrand zwart (anders om-en-om met (19,11)/(20,13); model zwart)'),
 (17,13,11,'maskerlijn 1 px: binnenste pixel wordt maskerschaduw'),(19,13,3,'groen stukje achter de kop (model)'),(20,13,1,'groen stukje: schaduwkant buitenlijn'),
 (17,14,3,'groen stukje (model)'),(19,14,G0,'lijn hals->mantel (hals ervoor)'),(20,14,6,'mantel in schaduw van de kop'),
 (18,15,2,'groen stukje, schaduwkant'),(19,15,G0,'lijn hals->mantel (hals ervoor)'),
 (17,16,2,'groen stukje onder de kop (model)'),(18,16,G0,'lijn hals->mantel (hals ervoor)'),(19,16,6,'mantel in schaduw van de kop'),
 (17,17,6,'mantel in schaduw van de kop (lijn 1 px)'),
 (16,19,G0,'lijn hals->mantel loopt door tot het masker'),
 (16,20,G0,'lijn hals->mantel (hals ervoor)'),(17,21,G0,'lijn hals->mantel'),(17,22,G0,'lijn hals->mantel'),(18,22,6,'lijn 1 px: mantel schaduw'),
 (18,23,6,'lijn 1 px: mantel schaduw'),(17,24,G0,'lijn hals->mantel'),(18,24,6,'lijn 1 px: mantel schaduw'),
 # kaak: groene onderkaak onder het masker (model), lijn 1 px
 (5,23,G0,'onderkaak: punt, outline base groen'),(7,23,2,'onderkaak (model groen)'),(8,23,G0,'onderkaak/mondhoek: lijn groen i.p.v. creme'),
 (10,23,2,'lijn 1 px: maskerrand staat erboven (10-11,22); hier hals in schaduw'),(11,23,2,'idem'),(10,24,1,'onderrand kaak/hals: schaduwkant'),
]
for x,y,v,r in HAND: zet(x,y,v,'kop/hals: '+r)
# ---- 4. volume groen (Gen 3, zoals Raikou-poten: smal licht aan de lichtkant, schaduwsikkel ±35% aan de schaduwkant) ----
F=np.isin(S,[2,3,4,13])
def ray(x,y,dx,dy):
    n=0
    while True:
        x+=dx; y+=dy
        if not(0<=x<64 and 0<=y<64) or not F[y,x]: return n
        n+=1
VOL=S.copy()
for y in range(55):
    for x in range(64):
        t=S[y,x]
        if t not in (3,4): continue
        hl,hr=ray(x,y,-1,0),ray(x,y,1,0); vu,vd=ray(x,y,0,-1),ray(x,y,0,1)
        kand=[(w,a,b) for (w,a,b) in ((hl+hr+1,hl,hr),(vu+vd+1,vu,vd)) if 4<=w<=10]
        if not kand: continue
        w,a,b=min(kand)
        sw=max(1,min(3,round(0.35*w)))
        if b<sw: VOL[y,x]=t-1
        elif a==0 and t==3 and w>=5: VOL[y,x]=4
# geen nieuwe tintvlekjes: een gewijzigde pixel die met zijn nieuwe tint een groepje < 3 px vormt -> terug
from collections import deque
def groepje(A,x,y):
    t=A[y,x]; q=deque([(x,y)]); z={(x,y)}
    while q and len(z)<3:
        a,b=q.popleft()
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            u,v=a+dx,b+dy
            if 0<=u<64 and 0<=v<64 and A[v,u]==t and (u,v) not in z: z.add((u,v)); q.append((u,v))
    return len(z)
for it in range(3):
    for y in range(64):
        for x in range(64):
            if VOL[y,x]!=S[y,x] and groepje(VOL,x,y)<3: VOL[y,x]=S[y,x]
for y in range(64):
    for x in range(64):
        if VOL[y,x]!=S[y,x]: zet(x,y,VOL[y,x],'volume groen: '+('schaduwsikkel' if VOL[y,x]<S[y,x] else 'licht aan de lichtkant'))
# ---- 5. mantel: waar het model duidelijk donkerder is (L<=128) dan de basis -> schaduwtint 6 ----
M=np.load(D+'modelL.npy')
for y in range(64):
    for x in range(64):
        if S[y,x] in (7,8) and M[y,x]<=128: zet(x,y,6,'mantel: schaduw waar het model donker is')
# ---- 6. paars: gedeeld oog/strepen tussen oogpaars (150,88,155) en streeppaars model (124,72,137) ----
PAL[13]=(138,80,148)
PAL[2]=(56,106,62); PAL[3]=(84,146,78); PAL[4]=(122,184,96); PAL[15]=(32,68,42)   # groen: stappen ±28 (Taillow 30-40), hue naar blauw in de schaduw
PAL[8]=(242,208,88)                                                                  # goudlicht iets minder fel
save(S,'kay_pacha_ek1.png'); np.save(D+'kay_pacha_ek1.npy',S)
assert ((S>0)==FG).all(),'silhouet gewijzigd'
assert S[18,9]==14 and S[18,11]==14 and S[17,11]==14 and S[18,10]==13
assert len(np.unique(S))<=16
tot=0
for k,v in log.items(): print(f'{len(v):4d} px  {k}'); tot+=len(v)
print('totaal',tot,'px gewijzigd t.o.v. r1 B (figuur',int(FG.sum()),'px); kleuren',len(np.unique(S)))
diff=(S!=B)&~((B==15)&(S==13)); print('pixels anders dan r1 B:',int(diff.sum()))
json.dump(log,open(D+'ek1_log.json','w'),default=int)
