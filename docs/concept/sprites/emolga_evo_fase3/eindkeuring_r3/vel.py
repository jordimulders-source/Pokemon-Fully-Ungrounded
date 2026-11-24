# vel.py: eindkeuring r3, alleen A_geel (Jordi koos A_geel) (Dragonfly Cave + omlijningsronde). Markeert de benoemde reparaties op A0/A/A_geel (8x)
# en zet ze op 1x/3x naast fase 2 en Gen 3-sprites op licht en donker. Wijzigt geen sprite.
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/'
E=D+'docs/concept/sprites/emolga_evo_fase3/'
G=D+'graphics/pokemon/%s/anim_front.png'
def rgba(f):
    im=Image.open(f)
    if im.size[1]==128: im=im.crop((0,0,64,64))
    if im.mode=='P':
        im=im.convert('RGBA'); px=im.load(); t=Image.open(f).getpalette()[:3]
        for y in range(64):
            for x in range(64):
                if px[x,y][:3]==tuple(t): px[x,y]=(0,0,0,0)
    return im
# reparaties: (x,y,kleur) ; R=rood outline base, M=magenta binnenlijn/cluster, O=oranje open rand, C=cyaan losse pixel, G=groen OH binnen de lijn (aanbevolen)
R=(230,30,30); M=(220,0,220); O=(255,140,0); C=(0,200,220); Gr=(0,170,60)
common=[(28,1,R),(33,4,R),(33,5,R),(33,6,R),(28,8,R),(26,11,R),(26,12,R),(20,28,R),
 (20,54,R),(20,55,R),(20,56,R),(19,57,R),(19,58,R),(19,59,R),(19,60,R),
 (31,52,R),(31,53,R),(31,54,R),(32,55,R),(32,56,R),(33,57,R),(33,58,R),
 (21,54,Gr),(21,55,Gr),(21,56,Gr),(20,57,Gr),(20,58,Gr),(20,59,Gr),
 (26,16,M),(28,16,M),(20,35,C),(24,51,M),
 (35,7,O),(35,8,O),(20,46,C)]
extraA=[(26,51,M)]
Z=8
def mark(f,marks,title):
    im=rgba(f); W=64*Z
    bg=Image.new('RGBA',(W,W+16),(232,232,220,255))
    bg.alpha_composite(im.resize((W,W),0),(0,16))
    d=ImageDraw.Draw(bg)
    for i in range(0,64,4):
        d.text((i*Z+1,16+1),str(i),fill=(120,120,120))
        d.text((1,16+i*Z+1),str(i),fill=(120,120,120))
    for x,y,c in marks:
        d.rectangle([x*Z,16+y*Z,x*Z+Z-1,16+y*Z+Z-1],outline=c,width=2)
    d.text((15*Z+4,2),title,fill=(0,0,0))
    return bg.crop((15*Z,0,49*Z,W+16))
panels=[mark(E+'sprite_r3/A_geel.png',common,'A_geel r3')]
# legenda
leg=Image.new('RGBA',(300,panels[0].size[1]),(255,255,255,255)); d=ImageDraw.Draw(leg)
y=8
for c,t in [(R,'1 outline base: lichte tint 3 (of zwart)'),(R,'  op de lichtkant -> 2'),(Gr,'1c aanbevolen: OH 2->3 binnen de lijn'),
            (M,'2 binnenlijn: 2x2-zwart weg / gat dicht'),(M,'5 kruinlijn rij 51 doorlopend zwart'),(O,'3 open rand: geel op buitenrand -> 1'),
            (C,'4 lichte/losse pixel: (20,46) a->3,'),(C,'  (20,35) 1->2')]:
    d.rectangle([6,y,18,y+12],outline=c,width=2); d.text((24,y),t,fill=(0,0,0)); y+=20
y+=10; d.text((6,y),'Pixels: zie KEURING.md',fill=(0,0,0))
top=Image.new('RGBA',(sum(p.size[0] for p in panels)+300+30,panels[0].size[1]),(255,255,255,255))
x=0
for p in panels: top.alpha_composite(p,(x,0)); x+=p.size[0]+10
top.alpha_composite(leg,(x,0))
# vergelijkingsstrook
refs=[('A_geel',E+'sprite_r3/A_geel.png'),('fase 2',E+'../emolga_evo/af/model.png')]+[(n,G%n) for n in ['murkrow','golbat','sableye','gligar','taillow','umbreon']]
cw=64*3+8
strip=Image.new('RGBA',(len(refs)*cw,64*3+64+40),(255,255,255,255)); d=ImageDraw.Draw(strip)
for i,(n,f) in enumerate(refs):
    im=rgba(f); x=i*cw
    for j,col in enumerate([(232,232,220,255),(40,44,52,255)]):
        b=Image.new('RGBA',(64,64),col); b.alpha_composite(im); strip.alpha_composite(b,(x+j*66,0))
    b=Image.new('RGBA',(192,192),(232,232,220,255)); b.alpha_composite(im.resize((192,192),0)); strip.alpha_composite(b,(x,66))
    d.text((x+2,66+194),n,fill=(0,0,0))
out=Image.new('RGBA',(max(top.size[0],strip.size[0]),top.size[1]+strip.size[1]+10),(255,255,255,255))
out.alpha_composite(top,(0,0)); out.alpha_composite(strip,(0,top.size[1]+10))
out.convert('RGB').save(E+'eindkeuring_r3/vel.png')
print(out.size)
