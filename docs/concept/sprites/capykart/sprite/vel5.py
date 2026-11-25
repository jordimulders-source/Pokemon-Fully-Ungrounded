# vel r5: per variant kop 12x naast bron-tandzone 12x; volledige sprites 8x (V2, T1, T2, T3); 1x-rij licht/donker
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/sprite/'
op=lambda p: Image.open(p).convert('RGBA')
def z(im,box,f): return im.crop(box).resize(((box[2]-box[0])*f,(box[3]-box[1])*f),Image.NEAREST)
src={'T1':('bibarel/anim_front.png',(10,12,32,34)),'T2':('bidoof/anim_front.png',(12,30,34,52)),'T3':('raticate/anim_front.png',(4,32,26,54))}
V={k:op(R+f'r5/capykart_{k}.png') for k in ('T1','T2','T3')}; V2=op(R+'r4/capykart_V2.png')
BG=(236,236,236,255); out=Image.new('RGBA',(4*528+8,3*(264+12)+528+16+150),BG); d=ImageDraw.Draw(out); y=8
for k in ('T1','T2','T3'):
    a=z(V[k],(9,18,31,40),12); b=z(op(G+src[k][0]).crop((0,0,64,64)),src[k][1],12)
    bg=Image.new('RGBA',b.size,(152,208,160,255)); bg.alpha_composite(b)
    out.alpha_composite(a,(8,y)); out.alpha_composite(bg,(8+a.width+16,y)); d.text((8+a.width*2+40,y+4),k+'  bron: '+src[k][0]+' (frame 1)',fill=(0,0,0,255)); y+=a.height+12
for i,(im,t) in enumerate([(V2,'r4 V2'),(V['T1'],'T1 bibarel'),(V['T2'],'T2 bidoof'),(V['T3'],'T3 raticate')]):
    out.alpha_composite(im.resize((512,512),Image.NEAREST),(8+i*528,y)); d.text((12+i*528,y+2),t,fill=(0,0,0,255))
y+=528; x=8
for bg in [(236,236,236,255),(40,44,52,255)]:
    box=Image.new('RGBA',(4*70+10,70),bg)
    for i,im in enumerate([V2,V['T1'],V['T2'],V['T3']]): box.alpha_composite(im,(5+i*70,3))
    out.alpha_composite(box,(x,y)); x+=box.width+12
    out.alpha_composite(box.resize((box.width*2,box.height*2),Image.NEAREST),(x,y)); x+=box.width*2+12
out.save(R+'r5/vel.png'); print(out.size)
