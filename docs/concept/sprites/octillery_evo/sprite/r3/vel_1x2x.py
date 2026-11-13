# vel_1x2x.py: sprite op 1x en 2x naast model (zelfde schaal) en 2 echte Gen 3-sprites
import sys,os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,D+'/..')
import pal,cfg
from PIL import Image,ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def gen3(n): return Image.open(G+n+'/anim_front_gba.png').convert('RGBA').crop((0,0,64,64))
items=[('model',cfg.model64().convert('RGBA')),('r3',Image.open(D+'/octi.png').convert('RGBA')),
       ('r2',Image.open(D+'/../r2/octi.png').convert('RGBA')),('Octillery',gen3('octillery')),('Scizor',gen3('scizor'))]
o=Image.new('RGB',(20+len(items)*150,375),(235,235,235)); d=ImageDraw.Draw(o)
for i,(n,im) in enumerate(items):
    x=20+i*150; d.text((x,4),n,fill=(0,0,0))
    for j,bg in enumerate([(255,255,255),(40,48,64)]):
        b=Image.new('RGB',(64,64),bg); b.paste(im,(0,0),im); o.paste(b,(x+j*70,20))
    b=Image.new('RGB',(64,64),(255,255,255)); b.paste(im,(0,0),im); o.paste(b.resize((128,128),Image.NEAREST),(x,100))
    b=Image.new('RGB',(64,64),(40,48,64)); b.paste(im,(0,0),im); o.paste(b.resize((128,128),Image.NEAREST),(x,235-0))
o.save(D+"/vel_1x2x.png"); print(o.size)
