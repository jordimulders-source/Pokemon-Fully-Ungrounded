# vel.png: voet 12x (r8 | r7 | model | model met spriteraster) / hele sprite 8x (r8 | r7 | model) / 1x
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from kijk import groot; from raster import raster
from PIL import ImageDraw
def w(p):
    im=Image.open(p).convert('RGBA'); x=Image.new('RGB',im.size,(255,255,255)); x.paste(im,(0,0),im); return x
def rij(ims,pad=8):
    out=Image.new('RGB',(sum(i.width for i in ims)+pad*(len(ims)-1),max(i.height for i in ims)),(220,220,220)); x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width+pad
    return out
def lab(im,t):
    out=Image.new('RGB',(im.width,im.height+16),(255,255,255)); out.paste(im,(0,16)); ImageDraw.Draw(out).text((4,2),t,fill=(0,0,0)); return out
md=model_op_schaal(); r8=w(HIER+'/hoatzin_r8.png'); r7=w(HIER+'/../r7/hoatzin_r7.png')
VB=(17,53,41,64)
rijen=[lab(rij([groot(x.crop(VB),12,False) for x in (r8,r7,md)]+[raster(*VB,12*S)]),'voeten 12x: r8 | r7 | model op schaal | model met spriteraster'),
       lab(rij([groot(r8,8),groot(r7,8),groot(md,8)]),'8x: r8 | r7 | model'),
       lab(rij([r8,r7,md]),'1x: r8 | r7 | model')]
W=max(r.width for r in rijen); H=sum(r.height+8 for r in rijen)
v=Image.new('RGB',(W,H),(255,255,255)); y=0
for r in rijen: v.paste(r,(0,y)); y+=r.height+8
v.save(HIER+'/vel.png'); print(v.size)
