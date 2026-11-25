# r14: drie vormreparaties op r13 (verre arm, achterbeen, rokpanden). Kleuren = palet r13.
# Index = helderheidsvolgorde van het r13-palet: 0=16 1=40 2=66 3=100 4=128 5=164 6=200 7=224 8=248
import numpy as np; from PIL import Image
PAL=[(16,16,24),(40,40,54),(66,70,92),(100,106,132),(128,124,146),(164,162,178),(200,200,212),(224,224,234),(248,248,248)]
r13=Image.open('../sprite_r13/mr_prime.png'); A=np.asarray(r13.convert('RGBA'))
K=np.full((64,64),-1)
for i,c in enumerate(PAL): K[(A[...,3]>0)&np.all(A[...,:3]==c,axis=-1)]=i
assert (K[A[...,3]>0]>=0).all()
R13=K.copy()
def put(y,x0,s):
    for i,ch in enumerate(s):
        if ch==' ': continue
        K[y,x0+i]=-1 if ch=='.' else int(ch)

# ---------- 1. verre arm (vorm = kale modelreductie, r13-omlijning blijft) ----------
# bovenarm als eigen deel vanaf de schouder (x47), lijn tussen romp en arm (x46), elleboog, plooi uit het model
put(29,46,'144')
put(30,46,'13444')
put(31,46,'133344')
put(32,46,'13333333')
put(33,47,'0022223' '2')  # plooi (model x47-48) + onderkant bovenarm
put(34,49,'0002' '3' '22')  # plooi, elleboog-hooglicht (model), schaduw
put(35,50,'000' '222')     # plooi + onderarm

# ---------- 2. achterbeen ----------
# schoen = r13-schoen als geheel 3 rijen omlaag (rij 52-58 -> 55-61), x gelijk (raakt x63 al)
shoe=np.zeros((64,64),bool)
for y,(a,b) in {52:(59,61),53:(57,62),54:(53,63),55:(54,63),56:(54,63),57:(55,63),58:(56,62)}.items(): shoe[y,a:b+1]=True
S=np.where(shoe,R13,-1)
# oud onderbeen/schoen weg (rechts van de nieuwe beenlijn)
for y in range(46,59):
    for x in range(49,64):
        if K[y,x]>=0 and not (y==45): K[y,x]=-1
for y in range(52,59):
    for x in range(44,64): K[y,x]=-1 if x>=44 else K[y,x]
ys,xs=np.where(S>=0)
for y,x in zip(ys,xs): K[y+3,x]=S[y,x]
# dij + scheen, vorm = afschuiving van het model (beenshear k=3): bovenlijn 1 px/rij, onderlijn 2 px/rij
put(45,48,'2200000')   # dij tot x49, zoomlijn van de jas x50-53
K[45,54]=-1            # jashoek recht op x53 (r13-jaskant)
put(46,45,'44333' '0')
put(47,43,'4444333' '0')
put(48,42,'223333333' '0')
put(49,42,'0023333333' '0')
put(50,41,'0000223333330')
put(51,44,'000222233' '30')
put(52,46,'000222233' '0')
put(53,48,'0022223' '30')
put(54,50,'00222' '33' '0')
put(55,52,'00223' '00')
put(56,54,'000')
# ---------- 3. rokpanden: één donkere vorm met de band erboven (model), punt B achter het achterbeen ----------
put(51,37,'12220')     # punt A: vulling in de bandtint (was licht 100 -> los tandje)
put(52,38,'120')
put(53,39,'00')
# punt B (model x44-49, y51-54) valt nu helemaal achter de onderlijn van het achterbeen
np.save('K14.npy',K)
# opslaan als r13: geïndexeerd, zelfde palet en volgorde, index 0 = transparant
pal=r13.getpalette()[:48]; P=np.zeros((64,64),'uint8')
for i,c in enumerate(PAL):
    j=[tuple(pal[k*3:k*3+3]) for k in range(16)].index(c); P[K==i]=j
out=Image.fromarray(P,'P'); out.putpalette(r13.getpalette()); out.info['transparency']=0
out.save('mr_prime.png',transparency=0)
