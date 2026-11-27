# vel.png: r3 8x | r2 8x | model op schaal 8x / close-ups kop en teken 12x (sprite | model op schaal | model met raster) / 1x en 2x / variant
#          / 1x op wit, crème, donker + model 1x / variant teken 8x
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from kijk import groot
from raster import raster
from PIL import ImageDraw
o=np.array(Image.open(HIER+'/hoatzin_r3.png')); ov=np.array(Image.open(HIER+'/hoatzin_r3_variant_teken.png'))
def r1img(bg):
    im=Image.open(HIER+'/../r2/hoatzin_r2.png').convert('RGBA'); out=Image.new('RGB',im.size,bg); out.paste(im,(0,0),im); return out
md=model_op_schaal()
W=(255,255,255)
rij1=[groot(rgb(o,W),8),groot(r1img(W),8),groot(md,8)]
def close(box,f=12):
    return [groot(rgb(o,W).crop(box),f,False),groot(md.crop(box),f,False),raster(box[0],box[1],box[2],box[3],f*S)]
kop=close((10,0,36,22)); tek=close((18,31,31,45))
een=[rgb(o,c_) for c_ in ((255,255,255),(248,240,208),(40,48,64))]+[md]
een=[im.resize((128,128),0) for im in een]+[r1img((255,255,255)).resize((128,128),0)]+[i for i in [rgb(o,(255,255,255)),r1img((255,255,255)),md]]
rij4=[groot(rgb(ov,W),8),groot(rgb(ov,W).crop((16,31,31,45)),12,False),groot(rgb(o,W).crop((16,31,31,45)),12,False)]
def rij(ims,pad=8):
    w=sum(i.width for i in ims)+pad*(len(ims)-1); h=max(i.height for i in ims)
    out=Image.new('RGB',(w,h),(220,220,220)); x=0
    for i in ims: out.paste(i,(x,0)); x+=i.width+pad
    return out
def label(im,t):
    out=Image.new('RGB',(im.width,im.height+16),(255,255,255)); out.paste(im,(0,16)); ImageDraw.Draw(out).text((4,2),t,fill=(0,0,0)); return out
rijen=[label(rij(rij1),'r3 8x | r2 8x | model op schaal 8x'),
       label(rij(kop),'kop 12x: r3 | model op schaal | model met spriteraster'),
       label(rij(tek),'teken 12x: r3 | model op schaal | model met spriteraster'),
       label(rij(een),'2x: r3 op wit, creme, donker | model | r2  ||  1x echt: r3, r2, model'),
       label(rij(rij4),'variant teken naar de buikrand 8x | close-up variant 12x | close-up hoofdversie 12x')]
w=max(r.width for r in rijen); h=sum(r.height for r in rijen)+8*len(rijen)
vel=Image.new('RGB',(w,h),(255,255,255)); y=0
for r in rijen: vel.paste(r,(0,y)); y+=r.height+8
vel.save(HIER+'/vel.png'); print(vel.size)
