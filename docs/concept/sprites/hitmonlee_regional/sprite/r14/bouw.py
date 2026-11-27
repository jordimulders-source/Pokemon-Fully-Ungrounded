# r14: alleen de rechte lijnen repareren op ek2 (Jordi 27 nov). Elke gewijzigde pixel -> log.txt.
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonlee_regional/'
src=Image.open(D+'eindkeuring/ek2.png'); e=np.array(src); r=e.copy()
LOG=[]
def zet(y,x,v,why):
    if r[y,x]!=v: LOG.append((y,x,int(r[y,x]),int(v),why)); r[y,x]=v

# ---- A. koepel bovenop: top-run 10 -> 8, rechterschouder 10,2,3 -> 8,3,2,1,1 (model-subpixel <= 0,5 px) ----
zet(21,17,0,'koepel: topschouder links afronden (model rand 21,50)')
zet(21,26,0,'koepel: topschouder rechts afronden (model rand 21,33)')
zet(22,17,2,'koepel: nieuwe bovenrand -> selout')
zet(22,26,2,'koepel: nieuwe bovenrand -> selout')
zet(23,31,0,'koepel: rechterflank, model rand 23,75 (dekking 0,25)')

# ---- C. nabije arm: taps zoals het model (rechterrand 16,15,15,14,14,14,13,13 i.p.v. 16,15,15,15,15,14,14,14) ----
for (y,x) in [(46,15),(47,15),(49,14),(50,14)]:
    zet(y,x,0,'arm: rechterrand naar model (dekking < 0,5)'); zet(y,x-1,1,'arm: nieuwe rechterrand zwart (schaduwkant)')

# ---- D/E. ringen als bogen (model: ringlijnen hangen in het midden 1 rij lager, uiteinden hoger) ----
# Bandtinten per ring (licht linksboven, zoals de Gen 3-Hitmonlee: licht -> midden -> donker naar de schaduwkant),
# tinten = de ringtinten die het model per band meet (bleek/zalm links, oranje -> oranjerood rechts).
def ringen(rows,cmin,cmax,mids,naam,full,T1,T2):
    for y in rows:
        xs=[x for x in range(cmin,cmax+1) if r[y,x]!=0]
        L,R=min(xs)+1,max(xs)-1
        w=R-L+1; c0=(L+R)/2
        for x in range(L,R+1):
            outer = abs(x-c0) > (w-1)/2-1+1e-9
            off = -1 if (outer and mids) else 0
            if y in full or (y-off) in mids:
                v=3 if (x==L and y not in full) else 2
                zet(y,x,v,naam+': ringlijn als boog (uiteinden 1 rij hoger, lichtkant 3)'); continue
            # positie in de band
            prev=max([m for m in list(mids)+[f+off for f in full] if m<y-off]+[-99])
            pos=(y-off)-prev
            T=T1 if pos<=1 else T2
            j=round((x-L)*(len(T[w])-1)/max(w-1,1)) if w not in T1 else x-L
            zet(y,x,T[w][x-L] if w in T1 else T[max(T)][j],naam+': bandtint rij %d van de ring'%pos)
K1={5:[15,7,6,5,5],6:[15,7,6,6,5,5],4:[7,6,5,5]}
K2={5:[7,6,5,5,4],6:[7,6,6,5,5,4],4:[6,5,5,4]}
# trapbeen rechterrand (10 rijen recht op kolom 48): inkeping op de lijnrijen 13, 15, 18, waar de modeldekking van
# kolom 48 het laagst is (0,67 / 0,78 / 0,44); ribbels zoals de Gen 3-Hitmonlee.
for y in (13,15,18):
    zet(y,48,0,'trapbeen: inkeping rechterrand bij ringlijn (modeldekking < 0,8)'); zet(y,47,1,'trapbeen: rechterrand zwart')
ringen(range(12,22),40,47 if False else 48,[14,16,19,21],'trapbeen',[11,22],K1,K2)
# standbeen: linkerrand naar het model (kolom 51 heeft daar dekking >= 0,5) met inkepingen op de lijnrijen
# 46, 48, 51 (ribbels; model 48 = inkeping, 46/51 dekking ~0,5).
for y in (45,47,49,50,52):
    if r[y,51]==0: zet(y,51,2,'standbeen: linkerrand naar model (selout, lichtkant)')
for y in (46,48,51):
    if r[y,51]!=0: zet(y,51,0,'standbeen: inkeping bij ringlijn')
    zet(y,52,2,'standbeen: linkerrand selout')
S1={4:[7,6,5,4],3:[7,5,4],5:[7,6,5,5,4]}
S2={4:[6,5,5,4],3:[6,5,4],5:[6,6,5,4,4]}
ringen(range(44,54),50,58,[],'standbeen',[44,46,48,51,53],S1,S2)

np.save(D+'sprite/r14/idx.npy',r)
im=Image.fromarray(r.astype('uint8'),'P'); im.putpalette(src.getpalette()); im.info['transparency']=0
im.save(D+'sprite/r14/r14.png',transparency=0)
im.convert('RGBA').resize((512,512),0).save(D+'sprite/r14/r14_8x.png')
with open(D+'sprite/r14/log.txt','w') as f:
    for t in LOG: f.write('(%d,%d) %d -> %d  %s\n'%(t[1],t[0],t[2],t[3],t[4]))
print(len(LOG),'pixels gewijzigd')
