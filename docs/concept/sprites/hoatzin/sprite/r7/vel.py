# vel.png: r7 | r6_K1 | model op 8x; snavel 12x (r7 | K1 | model); teken 12x (r7 | K1 | variant r6 | model); 1x
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from kijk import groot
from PIL import ImageDraw
def w(p):
    im=Image.open(p).convert('RGBA'); x=Image.new('RGB',im.size,(255,255,255)); x.paste(im,(0,0),im); return x
def rij(ims,pad=8):
    out=Image.new('RGB',(sum(i.width for i in ims)+pad*(len(ims)-1),max(i.height for i in ims)),(220,220,220)); x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width+pad
    return out
def lab(im,t):
    out=Image.new('RGB',(im.width,im.height+16),(255,255,255)); out.paste(im,(0,16)); ImageDraw.Draw(out).text((4,2),t,fill=(0,0,0)); return out
md=model_op_schaal(); r7=w(HIER+'/hoatzin_r7.png'); k1=w(HIER+'/../r6/hoatzin_r6_K1.png'); vt=w(HIER+'/../r6/hoatzin_r6_variant_teken.png')
SN=(4,13,22,27); TK=(16,31,31,46)
rijen=[lab(rij([groot(r7,8),groot(k1,8),groot(md,8)]),'r7 8x | r6_K1 8x | model op schaal 8x'),
       lab(rij([groot(x.crop(SN),12,False) for x in (r7,k1,md)]),'snavel 12x: r7 | r6_K1 | model'),
       lab(rij([groot(x.crop(TK),12,False) for x in (r7,k1,vt,md)]),'teken 12x: r7 (halverwege) | r6_K1 (plek B) | r6 variant (buikrand) | model'),
       lab(rij([r7,k1,md]),'1x: r7 | r6_K1 | model')]
W=max(r.width for r in rijen); H=sum(r.height+8 for r in rijen)
v=Image.new('RGB',(W,H),(255,255,255)); y=0
for r in rijen: v.paste(r,(0,y)); y+=r.height+8
v.save(HIER+'/vel.png'); print(v.size)
