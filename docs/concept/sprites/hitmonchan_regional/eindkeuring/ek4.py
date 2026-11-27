# ek4: duidelijker onderscheid schouder / wachtarm met kubus (krabbel_ek3, groene ^ rechts in beeld).
# Krabbel = ek3 op 6,2x (offset x -15, y +1). De ^ loopt in spritecoordinaten (42,30)-(43,29)-(44,28)-top rij 27 x45-47-(48,28)-(49,29)-(50,30).
# Model (natief_q, rij/kol): de ^ staat er als donkere binnenlijn om het lichte bovenvlak van de kubus:
#   linkerbeen 3: (40,35) (39,36) (38,37) -> 2 (37,38);  top: band rij 34 kol 42-44 = 4 4 4 (+ (41,35)=4);  rechterbeen 3: (45,35) (46,36), 4 (47,37).
# In ek3 waren rechterbeen (48,28)=3, (49,29)=3, (45,28)=4 en (46,27)=4 er al; het linkerbeen en de rechterhelft van de top vielen weg
# in de verkleining (sprite rij 27 = vooral model rij 33, licht). Alleen die worden teruggezet.
import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/hitmonchan_regional/'; O=D+'eindkeuring/'
TMP='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f28540c1-eb25-5a6c-8e41-5cf2205926c1/scratchpad/schouder/'
src=Image.open(O+'ek3.png'); K=np.array(src); pal=src.getpalette()[:24]; T=K.copy()
q=np.load(D+'sprite/natief_q.npy')
W=[ # (x,y,oud,nieuw,modelcel (rij,kol),reden)
 (47,27,6,4,(34,43),'top van de ^: band onder de schouder (model rij 34 kol 42-44 = 4)'),
 (44,28,5,3,(35,40),'linkerbeen ^ (model kol 40 r35 = 3)'),
 (43,29,5,3,(36,39),'linkerbeen ^ (model kol 39 r36 = 3)'),
 (42,30,5,3,(37,38),'linkerbeen ^ (model kol 38 r37 = 3), sluit aan op de 2-lijn (42,31)'),
]
log=[]
for x,y,o,n,(mr,mc),r in W:
    assert T[y,x]==o,(x,y,T[y,x],o); assert q[mr,mc]==n,(mr,mc,q[mr,mc]); T[y,x]=n
    log.append(f'({x},{y}) {o}->{n}  model r{mr} k{mc}={q[mr,mc]}  {r}')
assert ((T>0)==(K>0)).all()                      # silhouet gelijk
assert (T[18:27,28:44]==K[18:27,28:44]).all()   # beide ogen / gezicht niet aangeraakt
assert set(np.unique(T))<=set(np.unique(K))     # geen nieuwe kleuren
assert (T!=K).sum()==len(W)
im=Image.fromarray(T.astype('uint8'),'P'); im.putpalette(pal+[0]*(768-24)); im.save(O+'ek4.png',transparency=0)
open(O+'ek4_log.txt','w').write('\n'.join(log)+'\n')
def rgba(p):
    Image.open(p).save(TMP+'_t.png',transparency=0); return Image.open(TMP+'_t.png').convert('RGBA')
def on(im,c):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
LB=(235,235,235,255); DB=(40,44,52,255)
e3=rgba(O+'ek3.png'); e4=rgba(O+'ek4.png')
e38=on(e3,LB).resize((512,512),Image.NEAREST); e48=on(e4,LB).resize((512,512),Image.NEAREST); e48.save(O+'ek4_8x.png')
m=Image.open(D+'gemini/r3.png').convert('RGB'); a=np.asarray(m).min(2)<235; ys,xs=np.where(a)
crop=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); h=512; w=int(crop.width*h/crop.height)
m8=Image.new('RGB',(512,512),(235,235,235)); m8.paste(crop.resize((w,h),Image.LANCZOS),((512-w)//2,0))
nat=Image.open(D+'test/natief.png').convert('RGB')
def mark(img,s,cells,ox,oy):
    d=ImageDraw.Draw(img)
    for (x,y) in cells: d.rectangle([(x-ox)*s,(y-oy)*s,(x-ox+1)*s-1,(y-oy+1)*s-1],outline=(230,0,0),width=2)
    return img
# close-up schouder: sprite x38-52 rij 23-33 op 16x; model natief kol 34-49 rij 29-41 op 16x
c3=on(e3,LB).crop((38,23,53,34)).resize((15*16,11*16),Image.NEAREST)
c4=mark(on(e4,LB).crop((38,23,53,34)).resize((15*16,11*16),Image.NEAREST),16,[(x,y) for x,y,*_ in W],38,23)
cm=mark(nat.crop((34,29,50,42)).resize((16*16,13*16),Image.NEAREST),16,[(c,r) for *_,(r,c),_ in W],34,29)
Wd=3*512+4*16; H=40+512+40+208+40+128+16
v=Image.new('RGB',(Wd,H),(255,255,255)); dr=ImageDraw.Draw(v)
for i,(im,l) in enumerate(zip([e38,e48,m8],['ek3 8x','ek4 8x','model r3 (zelfde hoogte)'])):
    x=16+i*528; v.paste(im,(x,40)); dr.text((x,22),l,fill=(0,0,0))
y=40+512+40
for x,im,l in [(16,c3,'ek3 schouder 16x (x38-52, rij 23-33)'),(16+528,c4,'ek4 schouder 16x (rood = gezet)'),(16+2*528,cm,'model natief 16x (kol 34-49, rij 29-41; rood = bron)')]:
    v.paste(im,(x,y)); dr.text((x,y-16),l,fill=(0,0,0))
y=y+208+40; x=16
for im in [e3,e4]:
    for c in [LB,DB]:
        b=on(im,c); v.paste(b,(x,y)); v.paste(b.resize((128,128),Image.NEAREST),(x+72,y)); x+=72+128+16
dr.text((16,y-16),'1x / 2x licht en donker: ek3, ek4',fill=(0,0,0))
v.save(O+'vel4.png'); print('\n'.join(log))
