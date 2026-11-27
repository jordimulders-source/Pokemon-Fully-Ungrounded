# ek3: linkeroog (oog links in beeld, het verre oog) zoals in het model: puntje rechts + navy pupil.
# Model (natief_q, cellen): linkeroog = kol 23-26 x rij 26-28:
#   r26: 4 7 1 6   r27: 2 7 2 2   r28: 2 6 2 5   (kol 26 r27 = het puntje rechts)
# In ek2 staan kol 23,24,25 al als sprite x29,30,31 (rij 26-28 -> sprite rij 20-22), maar kol 26 viel weg
# in de verkleining (x32 = vooral kol 27). Met kol 23-26 1-op-1 op x29-32 komen er 2 pixels bij.
import numpy as np
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; D=R+'docs/concept/sprites/hitmonchan_regional/'; O=D+'eindkeuring/'
TMP='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f28540c1-eb25-5a6c-8e41-5cf2205926c1/scratchpad/oog/'
src=Image.open(O+'ek2.png'); K=np.array(src); pal=src.getpalette()[:24]; T=K.copy()
q=np.load(D+'sprite/natief_q.npy')
W=[ # (x,y,oud,nieuw,modelcel (rij,kol),reden)
 (32,21,5,2,(27,26),'puntje rechts van het linkeroog (model kol 26 r27 = 2)'),
 (31,20,2,1,(26,25),'pupil linkeroog bovenaan navy (model kol 25 r26 = 1)'),
]
log=[]
for x,y,o,n,(mr,mc),r in W:
    assert T[y,x]==o,(x,y,T[y,x],o); assert q[mr,mc]==n,(mr,mc,q[mr,mc]); T[y,x]=n
    log.append(f'({x},{y}) {o}->{n}  model r{mr} k{mc}={q[mr,mc]}  {r}')
# controle: linkeroog x29-32 rij 20-22 == model kol 23-26 rij 26-28
assert (T[20:23,29:33]==q[26:29,23:27]).all(), (T[20:23,29:33], q[26:29,23:27])
assert ((T>0)==(K>0)).all()                      # silhouet gelijk
assert (T[18:27,33:44]==K[18:27,33:44]).all()   # rechteroog / gezichtszone niet aangeraakt
assert set(np.unique(T))<=set(np.unique(K))     # geen nieuwe kleuren
im=Image.fromarray(T.astype('uint8'),'P'); im.putpalette(pal+[0]*(768-24)); im.save(O+'ek3.png',transparency=0)
open(O+'ek3_log.txt','w').write('\n'.join(log)+'\n')
# beelden
def rgba(p):
    Image.open(p).save(TMP+'_t.png',transparency=0); return Image.open(TMP+'_t.png').convert('RGBA')
def on(im,c):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
LB=(235,235,235,255); DB=(40,44,52,255)
e2=rgba(O+'ek2.png'); e3=rgba(O+'ek3.png')
e28=on(e2,LB).resize((512,512),Image.NEAREST); e38=on(e3,LB).resize((512,512),Image.NEAREST); e38.save(O+'ek3_8x.png')
m=Image.open(D+'gemini/r3.png').convert('RGB'); a=np.asarray(m).min(2)<235; ys,xs=np.where(a)
crop=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); h=512; w=int(crop.width*h/crop.height)
m8=Image.new('RGB',(512,512),(235,235,235)); m8.paste(crop.resize((w,h),Image.LANCZOS),((512-w)//2,0))
# close-up beide ogen: sprite x27-41 rij 17-25 op 16x; model natief kol 21-37 rij 23-31 op 16x (per cel)
nat=Image.open(D+'test/natief.png').convert('RGB')
def mark(img,s,cells,ox,oy):
    d=ImageDraw.Draw(img)
    for (x,y) in cells: d.rectangle([(x-ox)*s,(y-oy)*s,(x-ox+1)*s-1,(y-oy+1)*s-1],outline=(230,0,0),width=2)
    return img
c2=on(e2,LB).crop((27,17,42,26)).resize((15*16,9*16),Image.NEAREST)
c3=mark(on(e3,LB).crop((27,17,42,26)).resize((15*16,9*16),Image.NEAREST),16,[(x,y) for x,y,*_ in W],27,17)
cm=mark(nat.crop((21,23,38,32)).resize((17*16,9*16),Image.NEAREST),16,[(26,27),(25,26)],21,23)
Wd=3*512+4*16; H=40+512+40+144+40+128+16
v=Image.new('RGB',(Wd,H),(255,255,255)); dr=ImageDraw.Draw(v)
for i,(im,l) in enumerate(zip([e28,e38,m8],['ek2 8x','ek3 8x','model r3 (zelfde hoogte)'])):
    x=16+i*528; v.paste(im,(x,40)); dr.text((x,22),l,fill=(0,0,0))
y=40+512+40
for x,im,l in [(16,c2,'ek2 ogen 16x (x27-41, rij 17-25)'),(16+528,c3,'ek3 ogen 16x (rood = gezet)'),(16+2*528,cm,'model natief 16x (kol 21-37, rij 23-31; rood = bron)')]:
    v.paste(im,(x,y)); dr.text((x,y-16),l,fill=(0,0,0))
y=y+144+40; x=16
for im in [e2,e3]:
    for c in [LB,DB]:
        b=on(im,c); v.paste(b,(x,y)); v.paste(b.resize((128,128),Image.NEAREST),(x+72,y)); x+=72+128+16
dr.text((16,y-16),'1x / 2x licht en donker: ek2, ek3',fill=(0,0,0))
v.save(O+'vel3.png'); print('\n'.join(log))
