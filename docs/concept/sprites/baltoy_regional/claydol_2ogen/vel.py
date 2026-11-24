# vel.png: varianten | 3-ogenbasis op 8x, Baltoy r19 op 1x en 4x, gezichten 12x, 1x op licht/donker
from twee import *
from PIL import ImageDraw
V={n:rgba(bouw(**kw)[0]) for n,kw in VARIANTEN.items()}
basis=rgba(E)
bal=Image.open(os.path.join(HIER,'../sprite_r19/baltoy_r19.png'))
bal.info.setdefault('transparency',0); bal=bal.convert('RGBA')
items=[('A: d=3',V['A']),('B: d=4',V['B']),('C: d=4, oog 2 smaller',V['C']),('basis 3 ogen (r5 paletB)',basis)]
W=4*530+20; H=20+512+20+12*22+20+ 140
v=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(items):
    x=10+i*530; d.text((x,4),t,fill='black')
    v.alpha_composite(im.resize((512,512),Image.NEAREST),(x,18))
    v.alpha_composite(im.crop((8,10,56,32)).resize((48*11,22*11),Image.NEAREST),(x,18+512+10))
    y=18+512+10+22*11+10
    for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
        t2=Image.new('RGBA',(80,80),bg); t2.alpha_composite(im,(8,8)); v.alpha_composite(t2,(x+j*90,y))
        t3=Image.new('RGBA',(136,136),bg); t3.alpha_composite(im.resize((128,128),Image.NEAREST),(4,4)); v.alpha_composite(t3,(x+190+j*0,y)) if j==0 else None
    # Baltoy ernaast op 1x en 4x (alleen onder de laatste kolom en bij elke variant 1x)
    t4=Image.new('RGBA',(72,72),(248,248,240,255)); t4.alpha_composite(bal,(4,4)); v.alpha_composite(t4,(x+340,y))
v.alpha_composite(bal.resize((256,256),Image.NEAREST),(W-270,H-270)) if False else None
v.save(os.path.join(HIER,'vel.png'))
# apart: Baltoy 4x naast de varianten op 4x
w2=Image.new('RGBA',(5*266+10,280),(255,255,255,255))
for i,im in enumerate([V['A'],V['B'],V['C'],basis,bal]): w2.alpha_composite(im.resize((256,256),Image.NEAREST),(10+i*266,12))
v2=Image.new('RGBA',(W,H+290),(255,255,255,255)); v2.alpha_composite(v,(0,0)); v2.alpha_composite(w2,(0,H)); v2.save(os.path.join(HIER,'vel.png'))
