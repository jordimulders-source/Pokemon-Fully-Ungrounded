# maakt ../vel.png (ronde 2): ronde1 en ronde2 naast de onderlaag, kop en ogen op 8x naast fase 1, refs
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'../../../../../../../'); D=os.path.join(H,'../../../')
def ld(path,pal=None):
    im=Image.open(path).crop((0,0,64,64))
    if pal:
        p=[tuple(int(v) for v in l.split()) for l in open(pal).read().split('\n')[3:19] if l.strip()]
        im.putpalette([c for q in p for c in q])
    idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
r1=ld(os.path.join(H,'../../ronde1/nachtaap.png')); r2=ld(os.path.join(H,'../nachtaap.png'))
f1=ld(os.path.join(D,'referenties/fase1_goedgekeurd.png'),os.path.join(D,'../nachtaap/ronde12/variant_spiraal/normal.pal'))
ond=Image.open(os.path.join(D,'silhouet/onderlaag_256.png')).convert('RGBA')
refs=['lairon','sableye','aipom','grumpig','mismagius']
RF=[ld(os.path.join(R,f'graphics/pokemon/{n}/anim_front.png'),os.path.join(R,f'graphics/pokemon/{n}/normal.pal')) for n in refs]
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1360,900),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST)
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
put(r1,0,0,L,'ronde 1, 4x',4); put(r2,266,0,L,'ronde 2, 4x',4); put(r2,532,0,DK,'ronde 2 op donker',4)
put(ond,798,0,(255,255,255,255),'onderlaag 4x')
put(r1,1064,0,L,'r1 1x'); put(r2,1140,0,L,'r2 1x'); put(r2,1216,0,DK,'r2 donker'); put(f1,1064,90,L,'fase 1, 1x'); put(r2,1140,90,L,'r2 1x')
y=280; d.text((0,y-14),'kop op 8x: ronde 1 | ronde 2 | onderlaag (zelfde plek) | fase 1',fill=(30,30,30,255))
put(r1.crop((2,34,28,57)),0,y,L,None,8); put(r2.crop((2,34,28,57)),216,y,L,None,8)
put(ond.crop((8,136,112,228)).resize((26,23),Image.BOX) if False else ond.crop((8,136,112,228)),432,y,(255,255,255,255),None,2)
put(f1.crop((10,16,42,40)),648,y,L,None,6)
y=480; d.text((0,y+190),'ogen op 8x: ronde 2 (verre | nabije) naast fase 1',fill=(30,30,30,255))
put(r2.crop((5,42,22,50)),0+0,y+0,L,None,8) if False else None
put(r2.crop((5,42,22,50)),0,y+500-500+0+0+0+0+0+0,L,None,8) if False else None
e2=r2.crop((5,42,22,50)); e1=f1.crop((14,28,36,38))
put(e2,1000,280,L,'ogen r2, 8x',8); put(e1,940,370+20,L,'ogen fase 1, 8x',8) if False else put(e1,1000,380,L,'ogen fase 1, 8x',8)
x=0; y=500
for n,r in zip(['ronde 2']+refs,[r2]+RF): put(r,x,y,L,n,3); x+=210
x=0; y=720
for n,r in zip(['r2','r1','fase 1']+refs,[r2,r1,f1]+RF): put(r,x,y,L,n); x+=76
x=640
for r in [r2,r1,f1]+RF: put(r,x,y,DK); x+=76
o.save(os.path.join(H,'../vel.png'))
