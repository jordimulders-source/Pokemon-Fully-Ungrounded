# vel.png: r6 | r5 | model op 8x; kop 12x (r6 | r5 | model); 1x (r6, r5, model, variant teken)
# vel_kuif.png: K1 | K2 | K3 | K4 op 8x (kop 12x eronder) en 1x
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
def stapel(rijen,naam):
    W=max(r.width for r in rijen); H=sum(r.height+8 for r in rijen)
    v=Image.new('RGB',(W,H),(255,255,255)); y=0
    for r in rijen: v.paste(r,(0,y)); y+=r.height+8
    v.save(HIER+'/'+naam); print(naam,v.size)
md=model_op_schaal(); r6=w(HIER+'/hoatzin_r6.png'); r5=w(HIER+'/../r5/hoatzin_r5.png'); vt=w(HIER+'/hoatzin_r6_variant_teken.png')
KOP=(4,0,36,26)
stapel([lab(rij([groot(r6,8),groot(r5,8),groot(md,8)]),'r6 8x | r5 8x | model op schaal 8x'),
        lab(rij([groot(x.crop(KOP),12,False) for x in (r6,r5,md)]),'kop 12x: r6 | r5 | model'),
        lab(rij([r6,r5,md,vt]),'1x: r6 | r5 | model | r6 variant teken')],'vel.png')
K=[w(HIER+'/hoatzin_r6_%s.png'%k) for k in ('K1','K2','K3','K4')]
stapel([lab(rij([groot(x,8) for x in K]),'8x: K1 volledig | K2 1/3 | K3 1/2 (= r6) | K4 2/3'),
        lab(rij([groot(x.crop(KOP),12,False) for x in K]),'kop 12x: K1 | K2 | K3 | K4'),
        lab(rij(K+[md]),'1x: K1 | K2 | K3 | K4 | model')],'vel_kuif.png')
