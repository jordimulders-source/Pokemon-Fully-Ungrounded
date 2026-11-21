# r6: poten uit r9 (natief = r5 B op kleurruis na, zie natief.py/vergelijk), verre middenpoot vervangen
# door een KOPIE van de nabije middenpoot (poot 3) in schaduwtint, verschoven naar rechtsboven,
# alleen op lege pixels en niet naast de koperklauwtjes van de nabije poot.
# python3 bouw6.py NAAM dx dy
import numpy as np, sys; from PIL import Image
PAL=[(255,0,255),(16,16,20),(32,32,36),(60,60,66),(104,104,110),(156,156,160),(188,188,192),
     (50,60,74),(86,100,118),(132,148,162),(234,248,252),(208,232,240),(116,146,162),(160,72,214),(224,116,52),(146,64,34)]
naam=sys.argv[1]; dx,dy=int(sys.argv[2]),int(sys.argv[3])
r5=np.loadtxt('../sprite_r5/vlieg_r5_B.txt',dtype=int)
basis=np.loadtxt('../sprite_r5/r5_basis_vol.txt',dtype=int)   # r5 zonder verre kopieen
f=r5.copy()
# oude verre middenpoot (r5-kopie links van poot 3, x<=35) weg; die van r9 (donkere schuine poot) zat niet in r5
oud=[(x,y) for y,x in zip(*np.where(r5!=basis)) if x<=35]
for x,y in oud: f[y,x]=basis[y,x]
# achtervoet (rechtsonder, dambord in r9 en r5): vorm houden, schoon als twee klauwen met de twee koperkleuren
VOET={(47,57):1,(48,57):14,(46,57):0}
for (x,y),v in VOET.items(): f[y,x]=v
base=f.copy()
POOT={7,8,9,10,11,12,14,15}; S={7:7,8:7,9:8,10:11,11:12,12:12,14:15,15:15,1:1}
def masker(x0,x1,y0,y1):
    m=np.zeros_like(f,bool)
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            v=basis[y,x]
            if v in POOT: m[y,x]=True
            elif v==1 and any(basis[y+a,x+b] in POOT for a,b in((1,0),(-1,0),(0,1),(0,-1))): m[y,x]=True
    return m
m=masker(26,39,41,61); nieuw=[]
for y,x in zip(*np.where(m)):
    Y,X=y+dy,x+dx
    if not(0<=Y<64 and 0<=X<64) or base[Y,X]!=0 or f[Y,X]!=0: continue
    buur=[base[Y+a,X+b] for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=Y+a<64 and 0<=X+b<64]
    if (14 in buur or 15 in buur) and basis[y,x]!=1: continue   # geen koper tegen koper (dambord)
    f[Y,X]=S[basis[y,x]]; nieuw.append((X,Y))
# opschonen: buitenlijnpixels van de kopie die geen kopiekleur raken weg; open randen dicht met 1 px lijn
N=((1,0),(-1,0),(0,1),(0,-1)); ns=set(nieuw)
for X,Y in list(ns):
    if f[Y,X]==1 and not any((X+b,Y+a) in ns and f[Y+a,X+b]!=1 for a,b in N): f[Y,X]=0; ns.discard((X,Y))
dicht=0
for X,Y in list(ns):
    if f[Y,X]==1: continue
    for a,b in N:
        if f[Y+a,X+b]==0: f[Y+a,X+b]=1; ns.add((X+b,Y+a)); dicht+=1
nieuw=sorted(ns)
# koperklauwtjes van alle poten: lichte kleur nooit op de buitenrand -> 1 px lijn erboven/ernaast
for y in range(41,63):
    for x in range(1,63):
        if f[y,x] in (14,15):
            for a,b in N:
                if f[y+a,x+b]==0: f[y+a,x+b]=1; dicht+=1
print('lijn gesloten',dicht)
np.savetxt(f'vlieg_r6_{naam}.txt',f,fmt='%2d')
im=Image.fromarray(f.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48))
im.save(f'vlieg_r6_{naam}.png',transparency=0)
Image.fromarray(np.array(PAL)[f].astype('uint8')).resize((512,512),Image.NEAREST).save(f'vlieg_r6_{naam}_8x.png')
ys,xs=np.where(f>0)
print(naam,(dx,dy),'oude verre weg',len(oud),'nieuwe verre px',len(nieuw),'breed',xs.max()-xs.min()+1,'kleuren',len(set(f.ravel()))-1)
