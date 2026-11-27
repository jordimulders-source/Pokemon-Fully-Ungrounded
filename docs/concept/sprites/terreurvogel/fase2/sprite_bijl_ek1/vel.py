# 8x op wit + vel: ek1 | r4 | model op 8x; ek1 naast dodrio/fearow op 1x en 4x, licht en donker
import numpy as np, os; from PIL import Image, ImageDraw
R='../../../../../../'
def rgb(f,bg):
    im=Image.open(f)
    if 'graphics/pokemon' in f:
        p=open(os.path.join(os.path.dirname(f),'normal_gba.pal')).read().split('\n')[3:19]
        im.putpalette([int(v) for l in p for v in l.split()])
    a=np.array(im)[:64]; r=np.array(im.convert('RGB'))[:64].copy(); r[a==0]=bg; return Image.fromarray(r)
def big(im,k): return im.resize((im.size[0]*k,im.size[1]*k),Image.NEAREST)
EK='terreurvogel_ek1.png'; R4='../sprite_bijl_r4/terreurvogel_bijl_r4.png'
big(rgb(EK,(255,255,255)),8).save('terreurvogel_ek1_8x.png')
W=(255,255,255); D=(40,44,56)
model=Image.open('../gemini/r1_eenvoud.png').convert('RGB').resize((512,512),Image.LANCZOS)
vel=Image.new('RGB',(512*3+40,512+40+300),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate([(big(rgb(EK,W),8),'ek1'),(big(rgb(R4,W),8),'r4'),(model,'model r1_eenvoud')]):
    vel.paste(im,(10+i*522,30)); d.text((10+i*522,10),t,fill=(0,0,0))
refs=[EK,R+'graphics/pokemon/dodrio/anim_front_gba.png',R+'graphics/pokemon/fearow/anim_front_gba.png']
y=560
for j,bg in enumerate([W,D]):
    x=10
    for f in refs: vel.paste(rgb(f,bg),(x,y+j*140)); x+=70
    x+=20
    for f in refs: vel.paste(big(rgb(f,bg),2),(x,y+j*140)); x+=135
    for f in refs: vel.paste(big(rgb(f,bg),4).crop((0,64,256,256)),(x,y+j*140-64+64)) if False else None
vel.save('vel_tmp.png')
# 4x-rij apart (past niet in 300 px hoogte): nieuw vel samenstellen
v2=Image.new('RGB',(max(vel.size[0],3*266+10),vel.size[1]+2*266),(235,235,235)); v2.paste(vel,(0,0))
for j,bg in enumerate([W,D]):
    for i,f in enumerate(refs): v2.paste(big(rgb(f,bg),4),(10+i*266,vel.size[1]+j*266))
v2.save('vel.png'); os.remove('vel_tmp.png')
