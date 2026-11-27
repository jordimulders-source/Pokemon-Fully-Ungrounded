# r16: Jordi: "daar zijn de benen gewoon een normale vorm alsof ze getaped zijn, dus alleen binnen de lijnen zie je die golven".
# Basis r15 (koepel + arm blijven). Benen: gladde cilinderomtrek uit het model (uniform gefit), ringen alleen binnenin:
# gebogen binnenlijn (uiteinden raken de omtrek, midden 1 rij lager) + per ring licht->donker dwars over het been.
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonlee_regional/'
ek=Image.open(D+'eindkeuring/ek2.png'); e=np.array(ek)
r=np.array(Image.open(D+'sprite/r15/r15.png')).copy()
ZONE={}
def zet(y,x,v,why): r[y,x]=v; ZONE[(y,x)]=why

def been(naam,omtrek,arcs,P1,P2,extra_mid=()):
    # omtrek: y -> (L,R) buitenlijn; arcs: rijen s (uiteinden), middenlijn op s+1
    for y,(L,R) in omtrek.items():
        # oude beenpixels in deze rij wissen (venster rond het been)
        for x in range(L-3,R+4):
            if r[y,x]!=0 and abs(x-(L+R)/2)<=(R-L)/2+3: zet(y,x,0,naam)
        zet(y,L,2,naam+': gladde omtrek, selout lichtkant'); zet(y,R,1,naam+': gladde omtrek, zwart schaduwkant')
        cols=list(range(L+1,R))
        w=len(cols)
        for i,x in enumerate(cols):
            eind = i==0 or i==w-1
            lijnrijen=[s for s in arcs] if eind else [s+1 for s in arcs]
            if y in lijnrijen:
                zet(y,x,3 if i==0 else 2,naam+': binnenlijn (boog)'); continue
            vorige=max([t for t in lijnrijen if t<y]+[-9])
            p=y-vorige
            T=P1 if p<=1 else P2
            zet(y,x,T[w][i],naam+': ringverloop licht->donker (rij %d van de ring)'%p)
    for (y,x) in extra_mid: zet(y,x,2,naam+': laatste boog loopt door in het doorschijnende deel')

# trapbeen: model (uniform, schaal 0,424): kol 42-48 t/m rij 19, 41-47 rij 20-21, 40-46 rij 22-23
KB={y:(42,48) for y in range(12,20)}
KB.update({20:(41,47),21:(41,47),22:(40,46)})
P1={5:[15,8,8,7,6]}; P2={5:[8,7,6,6,5]}
been('trapbeen',KB,[13,16,19,22],P1,P2,extra_mid=[(23,42),(23,43),(23,44)])
# rij 22: middenlijn hoort op rij 23 (s=22 -> 23), dus rij 22 midden = band; rij 23 midden = lijn (extra_mid)

# standbeen: kol 51-56 (breedte en plek van de ek2-lijnrijen, model kol 51-56/57), rij 44-53
SB={y:(51,56) for y in range(44,54)}
S1={4:[15,8,7,6]}; S2={4:[8,7,6,5]}
been('standbeen',SB,[45,48,51],S1,S2)

np.save(D+'sprite/r16/idx.npy',r)
im=Image.fromarray(r.astype('uint8'),'P'); im.putpalette(ek.getpalette())
im.save(D+'sprite/r16/r16.png',transparency=0)
im.convert('RGBA').resize((512,512),0).save(D+'sprite/r16/r16_8x.png')
prev={}
for l in open(D+'sprite/r15/log.txt'):
    xy=l.split(')')[0][1:]; x,y=map(int,xy.split(',')); prev[(y,x)]=l.split('  ',1)[1].strip()
with open(D+'sprite/r16/log.txt','w') as f:
    n=0
    for y,x in zip(*np.where(r!=e)):
        f.write('(%d,%d) %d -> %d  %s\n'%(x,y,e[y,x],r[y,x],ZONE.get((y,x)) or prev.get((y,x),'?'))); n+=1
print(n,'px t.o.v. ek2; silhouet',((r>0)!=(e>0)).sum(),'kleuren',len(set(r.ravel())-{0}))
