# vel.py: kleur_r8 vel: per hand model | A | B | C | Alakazam-lepelhand (12x), pupillen (12x), beste combinatie 8x + 1x
import sys,os; H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from PIL import Image,ImageDraw,ImageFont
from geo import *
import pal
try: F=ImageFont.load_default(size=18)
except TypeError: F=ImageFont.load_default()
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB')
GP=H+'/../../../../../graphics/pokemon/'
def spr(fn,b,z): im=pal.rgb(pal.load(H+'/'+fn)).crop(b); return im.resize((im.width*z,im.height*z),Image.NEAREST)
def mod(b,z): x0,y0,x1,y1=b; return src.crop((int(OX+x0*S),int(OY+y0*S),int(OX+x1*S),int(OY+y1*S))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def gf(n,b,z): im=Image.open(GP+n+'/anim_front.png').convert('RGB').crop(b); return im.resize((im.width*z,im.height*z),Image.NEAREST)
Z=12; rijen=[]
def rij(titel,items):
    h=max(i.height for _,i in items)+50; GAP=[max(i.width,max(len(l) for l in t.split("\n"))*9)+16 for t,i in items]; w=sum(GAP)
    o=Image.new('RGB',(max(w,10),h+30),'white'); d=ImageDraw.Draw(o); d.text((0,0),titel,fill=(0,0,0),font=F); x=0
    for (t,i),g in zip(items,GAP):
        o.paste(i,(x,30)); tt=t if max(len(l) for l in t.split("\n"))*9<=g-16 else t.replace(': ',':\n',1); d.multiline_text((x,34+i.height),tt,fill=(0,0,0),font=F); x+=g
    rijen.append(o)
bL=(2,33,22,47); bR=(45,20,59,38); bE=(29,12,43,21)
rij('LINKERHAND (achter de rug, met kaart) 12x',[('model',mod(bL,Z)),('A: drie vingers over\nde kaartrand',spr('var_links_A.txt',bL,Z)),
    ('B: duim op de\nkaart, vuist',spr('var_links_B.txt',bL,Z)),('C: kaarthoek tussen\nde vingers',spr('var_links_C.txt',bL,Z)),('Alakazam lepelhand',gf('alakazam',(0,20,20,38),Z))])
rij('RECHTERHAND (nonchalant getoond, met kaart) 12x',[('model',mod(bR,Z)),('A: duim langs de\nrand, vuist',spr('var_rechts_A.txt',bR,Z)),
    ('B: duim plat\nop de kaart',spr('var_rechts_B.txt',bR,Z)),('C: wijsvinger\nop de kaart',spr('var_rechts_C.txt',bR,Z)),('Alakazam lepelhand',gf('alakazam',(38,24,54,40),Z))])
rij('PUPIL open oog 12x',[('r7',spr('basis_r7.txt',bE,Z)),('pupil 1 px naar links',spr('var_pupil_1px.txt',bE,Z)),('pupil 2 px naar links',spr('var_pupil_2px.txt',bE,Z)),
    ('model',mod(bE,Z)),('Kadabra-oog',gf('kadabra',(24,17,34,26),Z))])
B='var_beste_linksA_rechtsA_pupil1'
full=pal.rgb(pal.load(H+'/'+B+'.txt')).resize((512,512),Image.NEAREST)
one=Image.open(H+'/'+B+'.png').convert('RGBA'); ones=[]
for bg in [(248,248,248),(152,208,160),(40,40,48)]:
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(one); ones.append(b.convert('RGB'))
o1=Image.new('RGB',(64*3+40,64),'white')
for i,b in enumerate(ones): o1.paste(b,(i*84,0))
rij('BESTE COMBINATIE: links A, rechts A, pupil 1 px (8x en 1x)',[('8x',full),('1x',o1),('r7 8x',pal.rgb(pal.load(H+'/basis_r7.txt')).resize((512,512),Image.NEAREST))])
W=max(r.width for r in rijen); O=Image.new('RGB',(W,sum(r.height+20 for r in rijen)),'white'); y=0
for r in rijen: O.paste(r,(0,y)); y+=r.height+20
O.save(H+'/vel.png'); print(O.size)
