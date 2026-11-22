# Levert sunflora_evo_r1.png, _8x.png, vel.png en telt afwijkingen per zone t.o.v. de kale reductie.
import numpy as np; from PIL import Image, ImageDraw; from pal import PAL
C=np.load('r1_schoon.npy'); P=[v for c in PAL for v in c]
im=Image.fromarray(C,'P'); im.putpalette(P); im.save('sunflora_evo_r1.png',transparency=0)
S=Image.open('sunflora_evo_r1.png').convert('RGBA'); S.resize((512,512),Image.NEAREST).save('sunflora_evo_r1_8x.png')
# kale referentie op 64x64: kop_kaal (zonder lijn) + lijfboven_kaal + voeten_kaal op dezelfde plek
kop=np.load('kop_kaal.npy'); lb=np.load('lijfboven_kaal.npy'); vt=np.load('voeten_kaal.npy')
K=np.zeros((64,64),'uint8'); lx,ly=22,50
L=np.zeros((14,23),'uint8'); L[:lb.shape[0],:]=np.where(lb>0,lb,0); L[8:8+5,7:16]=np.where(vt[:5,:9]>0,vt[:5,:9],L[8:13,7:16])
K[ly:ly+14,lx:lx+23]=L; K[1:1+kop.shape[0],4:4+kop.shape[1]]=np.where(kop>0,kop,K[1:1+kop.shape[0],4:4+kop.shape[1]])
face=np.zeros((64,64),bool); face[19:40,15:39]=True
head=np.zeros((64,64),bool); head[1:1+kop.shape[0],4:4+kop.shape[1]]=kop>0
lijn=(C>0)&(K==0)&~(np.isin(C,[11,12,13,14,1])&(np.arange(64)[:,None]>=50))
d=C!=K
print('gezicht  afwijkend',(d&face&head).sum(),'van',(face&head).sum())
print('kop rest afwijkend',(d&head&~face).sum(),'van',(head&~face).sum())
print('kop buitenlijn erbij (buiten modelsilhouet)',(lijn&~head).sum())
body=(C>0)&~head&~lijn
print('lijf afwijkend',(d&body).sum(),'van',body.sum())
# vel
f=8
M=Image.open('model26_64.png').convert('RGB')
sun=Image.open('sunflora_f1.png').convert('RGBA')
W=64*f*3+40; H=64*f+40+140
v=Image.new('RGB',(W,H),(255,255,255)); dr=ImageDraw.Draw(v)
v.paste(S.resize((512,512),Image.NEAREST),(0,20),S.resize((512,512),Image.NEAREST))
v.paste(M.resize((512,512),Image.NEAREST),(512+20,20))
sb=sun.resize((512,512),Image.NEAREST); v.paste(sb,(1024+40,20),sb)
dr.text((4,4),'r1 (8x)',fill='black'); dr.text((532,4),'model r5 kop 2,6x, zelfde schaal (8x)',fill='black'); dr.text((1068,4),'Sunflora Gen 3 (8x)',fill='black')
y=512+40
for i,bg in enumerate([(248,248,248),(232,232,200),(40,40,48),(16,24,64)]):
    t=Image.new('RGB',(64,64),bg); t.paste(S,(0,0),S); v.paste(t,(i*84,y)); v.paste(t.resize((128,128),Image.NEAREST),(400+i*148,y))
v.save('vel.png'); print('vel',v.size)
