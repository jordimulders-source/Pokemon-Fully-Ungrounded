# Hoatzin r9: Dragonfly Cave-eindkeuring op r8 (alleen uitvoering; silhouet gelijk, alpha-diff 0).
# Getoetst: randen (lichte tint op de buitenrand, zwart aan de lichtkant), zwarte binnenlijnen in groen, losse vlekjes.
# Zwarte scheidingen tussen de kuifpieken blijven: alles naar donkergroen maakte de kuif tot een vlek (pixelblur);
# Gen 3 en de maatstaf-sprites gebruiken zwarte binnenlijnen waar vorm over vorm valt (Skarmory 156, Dundragoon 61 px).
import os,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(H+'/../r8/hoatzin_r8.png'); a=np.array(im); pal=im.getpalette()
WIJZ=[  # (y,x,nieuw,reden)
 (6,18,5,'kuif: los zwart puntje midden in groen (geen K in 8-buren) -> donkerste eigen tint'),
 (37,21,7,'teken: grijs vlekje tussen de twee lichtste pixels van het linkerblad -> blad aaneen'),
 (57,23,2,'linkervoet: middentint op de bovenrand (lichtkant) -> selout D'),
 (58,24,1,'linkervoet: lichte tint op de onderrand (schaduwkant) -> zwart'),
]
o=a.copy()
for y,x,v,r in WIJZ: print(y,x,a[y,x],'->',v,r); o[y,x]=v
print('gewijzigd',(o!=a).sum(),'alpha-diff',((o>0)!=(a>0)).sum(),'kleuren',len(np.unique(o)))
r=Image.fromarray(o.astype('uint8'),'P'); r.putpalette(pal); r.info['transparency']=0
r.save(H+'/hoatzin_r9.png',transparency=0)
def rgb(x,bg):
    p=Image.fromarray(x.astype('uint8'),'P'); p.putpalette(pal); w=np.array(p.convert('RGB')); w[x==0]=bg; return Image.fromarray(w)
rgb(o,(255,255,255)).resize((512,512),0).save(H+'/hoatzin_r9_8x.png')
import sys; sys.path.insert(0,H+'/../r8'); from gemeen import model_op_schaal
from PIL import ImageDraw
md=model_op_schaal().convert('RGB')
def rij(ims,pad=8,bg=(220,220,220)):
    out=Image.new('RGB',(sum(i.width for i in ims)+pad*(len(ims)-1),max(i.height for i in ims)),bg); xx=0
    for i in ims: out.paste(i,(xx,0)); xx+=i.width+pad
    return out
groot=lambda i:i.resize((i.width*8,i.height*8),0)
r1=rij([groot(rgb(o,(255,255,255))),groot(rgb(a,(255,255,255))),groot(md)])
r2=rij([rgb(o,(255,255,255)),rgb(a,(255,255,255)),md,rgb(o,(40,40,48)),rgb(a,(40,40,48))])
v=Image.new('RGB',(r1.width,r1.height+r2.height+40),(255,255,255)); dd=ImageDraw.Draw(v)
dd.text((4,2),'8x: r9 | r8 | model',fill=(0,0,0)); v.paste(r1,(0,16))
dd.text((4,r1.height+20),'1x: r9 | r8 | model | r9 donker | r8 donker',fill=(0,0,0)); v.paste(r2,(0,r1.height+36))
v.save(H+'/vel.png'); print(v.size)
