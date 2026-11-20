# maak.py: harpij_r4.txt -> harpij_r4.png (64x64, index 0 transparant), _8x.png, vel.png
import numpy as np; from PIL import Image, ImageDraw; from pal import *
g=lees('harpij_r4.txt'); OY,OX=3,13
a=np.zeros((64,64),'uint8')
for y in range(61):
  for x in range(38): a[OY+y,OX+x]=L[g[y,x]]
im=Image.fromarray(a,'P'); im.putpalette([v for _,c in PAL for v in c]+[0]*(768-3*len(PAL))); im.save('harpij_r4.png',transparency=0)
def plat(rgb64,s,bg=(232,232,232)): return Image.fromarray(rgb64).resize((64*s,64*s),Image.NEAREST)
def to64(rgb38,mask):
  o=np.full((64,64,3),232,'uint8'); o[OY:OY+61,OX:OX+38][mask]=rgb38[mask]; return o
R4=to64(rgb(g),g!='.')
plat(R4,8).save('harpij_r4_8x.png')
C=np.load('pal18.npy'); l=np.load('lijn.npy'); kr=np.zeros((61,38,3),'uint8'); kr[l>0]=C[l[l>0]-1].astype('uint8'); KAAL=to64(kr,l>0)
r3=lees('../sprite_r3/harpij_r3.txt'); R3=to64(rgb(r3),r3!='.')
avg=np.load('avg.npy'); cov=np.load('cov.npy'); MOD=to64(avg.clip(0,255).astype('uint8'),cov>=.5)
# modelomtrek: natief masker op 8x-schaal (factor 0,66*8 per natief px), rand in rood
o=np.load('model_idx_r4.npy')[3:95,24:82]>0
def met_omtrek(rgb64,S):
  # natief masker (58x92) bilineair op de 38x61-box (= factor 0,66, bodem rij 63, gecentreerd), rand 1 px in rood
  P=np.asarray(plat(rgb64,S)).copy()
  b=np.asarray(Image.fromarray((o*255).astype('uint8')).resize((38*S,61*S),Image.BILINEAR))>127
  e=b&~(np.roll(b,1,0)&np.roll(b,-1,0)&np.roll(b,1,1)&np.roll(b,-1,1))
  P[OY*S:OY*S+61*S,OX*S:OX*S+38*S][e]=(230,30,30); return Image.fromarray(P)
S=8; G=16; T=18
pan=[('r4 + modelomtrek (rood)',met_omtrek(R4,S)),('kale reductie x0,66',plat(KAAL,S)),('r3',plat(R3,S)),('model x0,66 (gemiddelde)',plat(MOD,S))]
zones=[('kop + kuif',(13,3,43,28)),('poten',(17,46,48,64)),('vleugelrand rechts',(36,24,51,58))]
Z=12
zh=sum((b[3]-b[1])*Z+T+G for _,b in zones)
Wd=4*(512+G)+G; V=Image.new('RGB',(Wd,T+512+G+zh+G),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,p) in enumerate(pan): V.paste(p,(G+i*(512+G),T)); d.text((G+i*(512+G),3),t+' (8x)',fill=(0,0,0))
y=T+512+G
for t,b in zones:
  d.text((G,y),t+' 12x: r4 (+rood) | kale reductie | r3 | model',fill=(0,0,0)); y+=T; x=G
  for k,src in enumerate((R4,KAAL,R3,MOD)):
    p=met_omtrek(src,Z) if k==0 else plat(src,Z)
    c=p.crop((b[0]*Z,b[1]*Z,b[2]*Z,b[3]*Z)); V.paste(c,(x,y)); x+=c.size[0]+G
  y+=(b[3]-b[1])*Z+G
V.save('vel.png'); print(V.size)
