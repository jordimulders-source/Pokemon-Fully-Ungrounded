# Eindpalet (Gen 3: kleur mag afwijken van het model), A.png/B.png, vel.png en het diffbewijs.
import numpy as np; from PIL import Image, ImageDraw
from npy2png import save
PAL=[(152,208,160),(16,14,18),(42,40,44),(66,64,66),(104,100,98),(252,228,148),(206,162,88),
     (248,192,96),(210,134,52),(156,92,36),(96,52,20),(248,116,96),(204,44,48)]
PAL+= [(0,0,0)]*(16-len(PAL))
kaal=np.load('kaal.npy'); basis=np.load('basis.npy'); A=np.load('A_ruw.npy'); B=np.load('B_ruw.npy')
save(A,'A.png',PAL); save(B,'B.png',PAL)
# --- bewijs: buiten de plaatzone (plaatpixels van de basis) zijn A, B en de basis gelijk
zone=np.isin(basis,[7,8,9,10])
print('A vs B buiten plaatzone:',int(((A!=B)&~zone).sum()),'| A vs basis buiten zone:',int(((A!=basis)&~zone).sum()),'| B vs basis buiten zone:',int(((B!=basis)&~zone).sum()))
print('A vs B binnen plaatzone:',int(((A!=B)&zone).sum()))
# --- afwijking van de kale reductie per zone
cx,cy=31.1,34.0; J,I=np.mgrid[0:64,0:64]; r=np.hypot(I+0.5-cx,J+0.5-cy)
pz=np.zeros((64,64),bool); pz[22:46,14:36]=True; pz&=r<17
Z={'plaat+ogen':pz,'kern':(r<17.5)&~pz,'ring (straal 17.5-21)':(r>=17.5)&(r<=21)&np.isin(basis,[0,5,6])&np.isin(kaal,[0,5,6]),}
Z['stenen+brokjes']=~(Z['plaat+ogen']|Z['kern']|Z['ring (straal 17.5-21)'])
for k,m in Z.items():
    print(f'{k:24s} basis≠kaal: {int(((basis!=kaal)&m).sum()):4d}   A≠kaal: {int(((A!=kaal)&m).sum()):4d}   B≠kaal: {int(((B!=kaal)&m).sum()):4d}')
print('kleuren A',len(np.unique(A)),'B',len(np.unique(B)))
# --- vel
def rgba(o,bg):
    im=Image.new('RGBA',(64,64),bg); px=im.load()
    for j in range(64):
        for i in range(64):
            if o[j,i]: px[i,j]=PAL[o[j,i]]+(255,)
    return im
LICHT=(232,236,224,255); DONKER=(40,44,64,255)
m=Image.open('../referenties/model.png').convert('RGBA')
S=11.87; X0=138-0.5*S; Y0=107-1.2*S
mod=m.crop((int(X0),int(Y0),int(X0+64*S),int(Y0+64*S))).resize((64,64),Image.LANCZOS)
z=8; W=64*z; pad=16
vel=Image.new('RGBA',(3*W+4*pad, W+2*pad+40+64*2+pad*2),(255,255,255,255)); d=ImageDraw.Draw(vel)
for k,(im,t) in enumerate([(rgba(A,LICHT),'A: linkeroog op de plaat'),(rgba(B,LICHT),'B: rechteroog op de plaat'),(mod,'model verkleind (64x64, Lanczos)')]):
    vel.paste(im.resize((W,W),Image.NEAREST),(pad+k*(W+pad),pad+20)); d.text((pad+k*(W+pad),4),t,fill=(0,0,0))
y=pad+20+W+pad; x=pad
for o,t in [(A,'A'),(B,'B')]:
    for bg in (LICHT,DONKER,(255,255,255,255)):
        vel.paste(rgba(o,bg),(x,y+12)); x+=64+8
    d.text((x-3*(64+8),y),t+' 1x (licht/donker/wit)',fill=(0,0,0)); x+=24
for o,t in [(A,'A 2x'),(B,'B 2x')]:
    vel.paste(rgba(o,LICHT).resize((128,128),Image.NEAREST),(x,y+12)); d.text((x,y),t,fill=(0,0,0)); x+=136
vel.save('vel.png'); print('vel',vel.size)
