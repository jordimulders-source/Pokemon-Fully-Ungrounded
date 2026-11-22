# vel.png: sprite r1 8x | kale reductie 8x | model (natief, BOX-verkleind tot dezelfde maat) 8x; onder: 1x op licht en donker.
import numpy as np, sys; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from bouw_pal import PAL
r=sys.argv[1] if len(sys.argv)>1 else 'r1'
sp=Image.open(f'sprite_{r}/baltoy_{r}.png'); sp.load()
spr=sp.convert('RGBA')
kaal=np.load('gereedschap/kaal48_rgb.npy').astype('uint8'); kk=np.load('gereedschap/kaal48_k.npy')
H,W=kk.shape
ka=Image.new('RGBA',(64,64),(0,0,0,0)); ox=(64-W)//2; oy=64-H-1
ki=Image.fromarray(np.dstack([kaal,np.where(kk>0,255,0).astype('uint8')]),'RGBA'); ka.paste(ki,(ox,oy))
nat=Image.open('gereedschap/natief.png').convert('RGB').crop((15,13,83,83))
mask=Image.fromarray((np.asarray(nat).min(2)<215).astype('uint8')*255)
mo=Image.new('RGBA',(64,64),(0,0,0,0)); mi=nat.resize((W,H),Image.BOX).convert('RGBA'); mi.putalpha(mask.resize((W,H),Image.BOX).point(lambda v:255 if v>110 else 0)); mo.paste(mi,(ox,oy))
def op(im,bg,z):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
Z=8; panelen=[(f'sprite {r}',spr),('kale reductie (schrappen)',ka),('model, verkleind',mo)]
v=Image.new('RGB',(3*64*Z+40,64*Z+30+64*3+30),(255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(panelen):
    v.paste(op(im,(255,255,255,255),Z),(10+i*(64*Z+10),24)); d.text((10+i*(64*Z+10),6),t,fill=(0,0,0))
y=64*Z+40
for j,bg in enumerate([(248,248,240,255),(40,44,52,255)]):
    v.paste(op(spr,bg,1),(10+j*80,y)); v.paste(op(spr,bg,2),(180+j*150,y))
v.save(f'sprite_{r}/vel.png')
