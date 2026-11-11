# vel.py: kleur_r12b: rechterarm r11 | V1 | V2 | model op 12x; hele sprite 8x en 1x
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from PIL import Image,ImageDraw,ImageFont
from geo import *
import pal
try: F=ImageFont.load_default(size=18)
except TypeError: F=ImageFont.load_default()
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB'); GP=H+'/../../../../../graphics/pokemon/'
def spr(fn,b,z): im=pal.rgb(pal.load(H+'/'+fn)).crop(b); return im.resize((im.width*z,im.height*z),Image.NEAREST)
def mod(b,z): x0,y0,x1,y1=b; return src.crop((int(OX+x0*S),int(OY+y0*S),int(OX+x1*S),int(OY+y1*S))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
rijen=[]
def rij(titel,items):
    GAP=[max(i.width,max(len(l) for l in t.split('\n'))*9)+16 for t,i in items]
    o=Image.new('RGB',(sum(GAP),max(i.height for _,i in items)+80),'white'); d=ImageDraw.Draw(o); d.text((0,0),titel,fill=(0,0,0),font=F); x=0
    for (t,i),g in zip(items,GAP): o.paste(i,(x,30)); d.multiline_text((x,34+i.height),t,fill=(0,0,0),font=F); x+=g
    rijen.append(o)
Z=12
ala=None
def heel(fn):
    big=pal.rgb(pal.load(H+'/'+fn)).resize((512,512),Image.NEAREST); one=Image.open(H+'/'+fn.replace('.txt','.png')).convert('RGBA')
    o=Image.new('RGB',(512,512+84),'white'); o.paste(big,(0,0))
    for i,bg in enumerate([(248,248,248),(152,208,160),(40,40,48)]):
        q=Image.new('RGBA',(64,64),bg+(255,)); q.alpha_composite(one); o.paste(q.convert('RGB'),(i*84,520))
    return o
bR=(32,24,54,40)
rij('RECHTERARM 12x',[('r11',spr('r11.txt',bR,Z)),('V1: arm 3 px',spr('var_V1.txt',bR,Z)),('V2: breedte model,\nlichter',spr('var_V2.txt',bR,Z)),('model',mod(bR,Z))])
rij('HELE SPRITE 8x en 1x (L1, rechts A, pupil 1 px)',[('V1',heel('var_V1.txt')),('V2',heel('var_V2.txt'))])
W=max(r.width for r in rijen); O=Image.new('RGB',(W,sum(r.height+20 for r in rijen)),'white'); y=0
for r in rijen: O.paste(r,(0,y)); y+=r.height+20
O.save(H+'/vel.png'); print(O.size)
