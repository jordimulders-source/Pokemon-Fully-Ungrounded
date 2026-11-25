# r15: hoed rechts los van het hoofd (Jordi bij r14). Twee varianten zonder tekenen.
# A: Mr. Rime's zijhaar (front.png y16-23 x38-45: de strook langs de achterkant van de kop, incl. aanzet onder de rand) op de hoedverschuiving (DX=+7, DY=-3, zelfde als de Rime-hoed in r14),
#    omgekleurd, alleen op transparante pixels (achter de kopomtrek, niets over het gezicht).
# B: hoed + beide vleugels als geheel 1 px omlaag (B1) of 1 px links + 1 omlaag (B2).
import numpy as np; from PIL import Image
PAL=[(16,16,24),(40,40,54),(66,70,92),(100,106,132),(128,124,146),(164,162,178),(200,200,212),(224,224,234),(248,248,248)]
src=Image.open('../sprite_r14/mr_prime.png'); A0=np.asarray(src.convert('RGBA'))
K14=np.full((64,64),-1)
for i,c in enumerate(PAL): K14[(A0[...,3]>0)&np.all(A0[...,:3]==c,axis=-1)]=i
R=np.asarray(Image.open('../../../../../graphics/pokemon/mr_rime/front.png')).astype(int)
MAP={3:0,1:0,4:1,2:2}   # Rime zwart/donker -> 16, 56,48,88 -> 40, 80,80,128 -> 66 (hoedtinten r14)
DX,DY=7,-3
def save(K,naam):
    pal=src.getpalette(); P=np.zeros((64,64),'uint8')
    ent=[tuple(pal[k*3:k*3+3]) for k in range(16)]
    for i,c in enumerate(PAL): P[K==i]=ent.index(c)
    o=Image.fromarray(P,'P'); o.putpalette(pal); o.save(naam,transparency=0)
# --- A ---
KA=K14.copy(); nA=0
for y in range(16,24):
    for x in range(38,46):
        v=R[y,x]
        if v in MAP:
            yy,xx=y+DY,x+DX
            if KA[yy,xx]==-1: KA[yy,xx]=MAP[v]; nA+=1
save(KA,'variant_A.png'); print('A: Rime-zijhaar pixels geplaatst',nA)
# --- B ---
laag=np.zeros((64,64),bool)
laag[0:13,:]=K14[0:13,:]>=0                  # hoed, rand, rechtervleugel, bovenkant linkervleugel
laag[13:18,10:26]=K14[13:18,10:26]>=0        # staart linkervleugel
for naam,(dx,dy) in {'B1':(0,1),'B2':(-1,1)}.items():
    KB=K14.copy(); KB[laag]=-1
    # wat onder de laag lag: alleen de kop (rij 13+), die blijft; vrijgekomen pixels erboven worden transparant
    KB[13:,:]=np.where(laag[13:,:],-1,K14[13:,:])
    ys,xs=np.where(laag)
    for y,x in zip(ys,xs): KB[y+dy,x+dx]=K14[y,x]
    save(KB,'variant_%s.png'%naam)
