# ek2: reparatie rechte lijnen (Jordi's krabbel_ek1) + wachtvuist los van de schouder. Alleen tint, silhouet gelijk, oogzone niet aangeraakt.
import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/hitmonchan_regional/'; O=D+'eindkeuring/'
src=Image.open(O+'ek1.png'); K=np.array(src); pal=src.getpalette()[:24]; T=K.copy()
W=[ # (x,y,oud,nieuw,reden)
 # lijn 2: binnenrand opgeheven onderarm. Model (rijen 1-op-1): kol 16 r24-25, kol 17 r26-27, kol 18 r28-32, kol 19 r33-37 = trap 2/2/5/5.
 # ek1 had x24 r18-19, x25 r20-26 (7 recht: kol 17 en 18 vielen samen). Nu x24 r18-21, x25 r22-26, x26 r27-30 = 4/5/4.
 (24,20,4,1,'lijn 2: trap; model kol 17 r26 navy, M_donker=1'),
 (24,21,4,1,'lijn 2: trap; model kol 17 r27 navy, M_donker=1'),
 (25,20,1,2,'lijn 2: rechts van de lijn; model kol 18 r26 = 2, M_gem=2'),
 (25,21,1,2,'lijn 2: rechts van de lijn; model kol 18 r27 = 2, M_gem=2'),
 # lijn 6: riem bovenrand. Model r46 kol 21-24 = 3,4,3,2 (lichte inkeping), navy pas weer kol 25-29. ek1 had 10 navy op rij 37.
 (28,37,1,3,'riem bovenrand: inkeping model r46 kol 21-22 (3/4)'),
 (29,37,1,3,'riem bovenrand: inkeping model r46 kol 23 (3), M_gem=3'),
 (30,37,1,2,'riem bovenrand: inkeping model r46 kol 24 (2), M_licht=2'),
 # extra punt Jordi: wachtvuist bovenkant los van de schouder. Model r33 kol 38-41 = 6,6,7,6 (bovenvlak kubus), M_gem=6,6,6; r5 had (43,27)=6, ontkorreld in r6.
 (43,27,5,6,'wachtkubus bovenvlak onder de naad met de schouder (model 6, M_gem 6, kale reductie 6)'),
 (44,27,5,6,'idem (model r33 6/7, M_gem 6)'),
 (45,27,5,6,'idem (model r33 7/6, M_gem 6)'),
]
log=[]
for x,y,o,n,r in W:
    assert T[y,x]==o,(x,y,T[y,x],o); T[y,x]=n; log.append(f'({x},{y}) {o}->{n}  {r}')
assert ((T>0)==(K>0)).all()                      # silhouet gelijk
assert (T[18:27,33:44]==K[18:27,33:44]).all()   # oogzone niet aangeraakt
assert set(np.unique(T))<=set(np.unique(K))     # geen nieuwe kleuren
im=Image.fromarray(T.astype('uint8'),'P'); im.putpalette(pal+[0]*(768-24)); im.save(O+'ek2.png',transparency=0)
open(O+'ek2_log.txt','w').write('\n'.join(log)+'\n')
# beelden
TMP='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f28540c1-eb25-5a6c-8e41-5cf2205926c1/scratchpad/ek/'
def rgba(p):
    Image.open(p).save(TMP+'_t.png',transparency=0); return Image.open(TMP+'_t.png').convert('RGBA')
def on(im,c):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
LB=(235,235,235,255); DB=(40,44,52,255)
e1=rgba(O+'ek1.png'); e2=rgba(O+'ek2.png')
e18=on(e1,LB).resize((512,512),Image.NEAREST); e28=on(e2,LB).resize((512,512),Image.NEAREST); e28.save(O+'ek2_8x.png')
m=Image.open(D+'gemini/r3.png').convert('RGB'); a=np.asarray(m).min(2)<235; ys,xs=np.where(a)
crop=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); h=512; w=int(crop.width*h/crop.height)
m8=Image.new('RGB',(512,512),(235,235,235)); m8.paste(crop.resize((w,h),Image.LANCZOS),((512-w)//2,0))
dm=(np.array(on(e2,LB))*0.35+165).astype('uint8')
for y,x in zip(*np.where(K!=T)): dm[y,x]=(230,0,0)
d8=Image.fromarray(dm).resize((256,256),Image.NEAREST)
Wd=3*512+4*16; H=40+512+24+128+16
v=Image.new('RGB',(Wd,H),(255,255,255)); dr=ImageDraw.Draw(v)
for i,(im,l) in enumerate(zip([e18,e28,m8],['ek1 8x','ek2 8x','model r3 (zelfde hoogte)'])):
    x=16+i*528; v.paste(im,(x,40)); dr.text((x,22),l,fill=(0,0,0))
y=40+512+24; x=16
for im in [e1,e2]:
    for c in [LB,DB]:
        b=on(im,c); v.paste(b,(x,y)); v.paste(b.resize((128,128),Image.NEAREST),(x+72,y)); x+=72+128+16
dr.text((16,y-16),'1x / 2x licht en donker: ek1, ek2',fill=(0,0,0))
dr.text((x+10,y-16),f'diff ek1->ek2 (rood, {len(W)} px)',fill=(0,0,0)); v.paste(d8.crop((0,0,256,128)) if False else d8.resize((128,128)),(x+10,y))
v.save(O+'vel2.png'); print('\n'.join(log))
