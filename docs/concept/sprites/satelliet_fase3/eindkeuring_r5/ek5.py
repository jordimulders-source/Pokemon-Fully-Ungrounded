# Eindkeuring r5 (Dragonfly Cave): alleen indexwissels per pixel op sprite/r5/sprite.png.
# Draaien vanuit de repo-root of deze map; schrijft sprite.png, sprite_8x.png, vel.png.
import os, numpy as np
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..'))
G=os.path.normpath(os.path.join(R,'..','..','..','..'))
FIX=[ # (x,y,oud,nieuw,reden)
 (1,38,1,2,'zwart aan de lichtkant (punt paneel PD) -> outline base navy'),
 (38,28,1,3,'mastvoetring: 8/1/8-dambord, holte in donkerste eigen tint (model L58)'),
 (33,40,1,12,'zwart cluster 2 rijen onder de hub; model hier licht (L181) = buis'),
 (34,40,1,2,'zwart cluster onder de hub -> bovenkant mast in eigen navy (model L78)'),
 (35,40,1,2,'idem (model L66)'),
 (13,43,5,2,'bovenrand grote oogbol (lichtkant): lila paneellijn -> outline base navy'),
 (14,43,5,15,'binnen de omlijning van de oogbol; model wit (L227)'),
 (14,42,15,2,'losse witte pixel boven de omlijning -> outline base navy (1 px rand)'),
 (15,42,1,2,'zwart op de lichtkant (bovenkant oogbol) -> navy'),
 (16,42,1,2,'idem'),
 (17,42,5,2,'lila paneellijn op de bolrand -> navy'),
 (21,45,1,12,'binnenlijn 2 px dik; model hier bol (L179)'),
 (22,45,1,3,'binnenlijn bol/kraag: zwart/3/zwart om en om -> 3 (model L52)'),
 (22,47,1,3,'idem (model L54)'),
 (22,48,1,3,'idem'),
 (24,46,1,3,'binnenlijn kraag/buis niet zwart (model L94)'),
 (12,50,5,6,'oogring: lila 5 (andere tint, lichter dan 6) -> ringpaars 6 (model 111,72,127)'),
 (13,51,5,6,'idem'),
 (14,52,5,6,'idem; 5/6/5 om en om'),
 (16,51,5,6,'idem'),
 (16,52,5,12,'model hier bol (L185) -> c'),
 (41,32,1,3,'zwart tussen twee kragen (6 boven en onder) -> binnenlijn 3 (model L75)'),
 (42,33,1,2,'bovenrand rechterarm = lichtkant, cluster 2 rijen zwart -> navy'),
 (43,33,1,2,'idem'),
 (44,33,1,2,'idem (sluit aan op navy (45,34))'),
 (38,35,1,6,'losse zwarte pixel tussen hub en kraag -> kraagpaars (model 126,86,143)'),
 (46,28,1,12,'zwart in de buis; model licht (L162)'),
 (47,28,1,3,'binnenlijn buis/module niet zwart (model L59)'),
]
src=Image.open(os.path.join(R,'sprite','r5','sprite.png'))
a=np.array(src); pal=src.getpalette()
b=a.copy()
for x,y,o,n,r in FIX:
    assert a[y,x]==o,(x,y,a[y,x],o); b[y,x]=n
out=Image.fromarray(b,'P'); out.putpalette(pal)
out.save(os.path.join(H,'sprite.png'),transparency=0)
assert ((a>0)!=(b>0)).sum()==0
print('gewijzigd',int((a!=b).sum()),'silhouet gelijk; kleuren',len(np.unique(b)))
def rgb(arr,bg):
    o=np.zeros(arr.shape+(3,),np.uint8)+np.array(bg,np.uint8)
    for i in range(1,16): o[arr==i]=pal[3*i:3*i+3]
    return Image.fromarray(o)
def rgba(arr):
    o=np.zeros(arr.shape+(4,),np.uint8)
    for i in range(1,16): o[arr==i]=pal[3*i:3*i+3]+[255]
    return Image.fromarray(o)
rgba(b).resize((512,512),Image.NEAREST).save(os.path.join(H,'sprite_8x.png'))
# vel
m=Image.open(os.path.join(R,'model','model_gekozen.png')).convert('RGB')
s=3.515625; TOP=13
mm=m.crop((3,3,3+225,3+int(round(43*s)))).resize((64,43),Image.LANCZOS)
mfull=Image.new('RGB',(64,64),(235,240,235)); mfull.paste(mm,(0,TOP))
BG=(235,240,235)
top=[rgb(a,BG),rgb(b,BG),mfull]
diff=np.array(rgb(b,BG)).copy(); 
W=Image.new('RGB',(3*512+40,512+40+260),(255,255,255)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate(zip(top,['r5 (invoer)','eindkeuring r5 (gecorrigeerd)','model verkleind (LANCZOS)'])):
    W.paste(im.resize((512,512),Image.NEAREST),(i*532,30)); d.text((i*532+4,10),t,fill=(0,0,0))
# rode kaders om gewijzigde pixels in het middelste paneel
for x,y,o,n,r in FIX:
    d.rectangle([532+x*8,30+y*8,532+x*8+7,30+y*8+7],outline=(255,0,0))
# 1x en 3x naast maatstaf, licht en donker
def load(p):
    im=Image.open(p); arr=np.array(im)[:64]; pl=im.getpalette()
    o=np.zeros((64,64,4),np.uint8)
    for i in range(1,16): o[arr==i]=pl[3*i:3*i+3]+[255]
    return Image.fromarray(o)
refs=[rgba(b),load(os.path.join(R,'..','satelliet_fase2','af','satelliet.png')),load(os.path.join(R,'..','satelliet_lijn','fase1','af','satelliet_fase1.png'))]
for sp in ('metagross','magneton','claydol'):
    refs.append(load(os.path.join(G,'graphics','pokemon',sp,'anim_front_gba.png')))
y0=512+50
for row,bg in enumerate(((245,245,240),(40,40,48))):
    strip=Image.new('RGBA',(len(refs)*70*3,64*3+12),bg+(255,))
    strip1=Image.new('RGBA',(len(refs)*70,70),bg+(255,))
    for i,r in enumerate(refs):
        strip.alpha_composite(r.resize((192,192),Image.NEAREST),(i*210,6))
        strip1.alpha_composite(r,(i*70+3,3))
    W.paste(strip1.convert('RGB'),(4,y0+row*100)); 
    W.paste(strip.convert('RGB').resize((strip.width//2,strip.height//2),Image.NEAREST),(470,y0+row*100))
d.text((4,y0-12),'1x en 1,5x: gecorrigeerd | fase 2 | fase 1 | Metagross | Magneton | Claydol (Gen 3 _gba)',fill=(0,0,0))
W.save(os.path.join(H,'vel.png'))
with open(os.path.join(H,'wijzigingen.txt'),'w') as f:
    for x,y,o,n,r in FIX: f.write('(%d,%d) %x -> %x  %s\n'%(x,y,o,n,r))
