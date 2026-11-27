import numpy as np; from PIL import Image, ImageDraw
G='../../../../../graphics/pokemon/'
def rgb(path,bg=(240,240,236)):
    im=Image.open(path); a=np.array(im); P=np.array(im.getpalette()[:48]).reshape(16,3).astype('uint8')
    x=P[a]; x[a==0]=bg; return Image.fromarray(x),a
def gba(n,bg=(240,240,236)):
    a=np.array(Image.open(G+n+'/anim_front_gba.png'))[:64]
    P=np.array([[int(v) for v in l.split()] for l in open(G+n+'/normal_gba.pal').read().split('\n')[3:19]],'uint8')
    x=P[a]; x[a==0]=bg; return Image.fromarray(x)
e,ea=rgb('sprite.png'); r,ra=rgb('../sprite_r9/sprite_C.png')
dif=np.array(e).copy(); m=ea!=ra
dif=(dif*0.35+255*0.65).astype('uint8'); dif[m]=(255,0,200)
V=Image.new('RGB',(3*522+10,2*530+20),'white'); d=ImageDraw.Draw(V)
for i,(t,im) in enumerate([('eind',e),('r9 C',r),('verschil (%d px, magenta)'%m.sum(),Image.fromarray(dif))]):
    V.paste(im.resize((512,512),Image.NEAREST),(i*522,18)); d.text((i*522+2,2),t,fill=(0,0,0))
y=545; x=1044
for bg in ((240,240,236),(40,40,56)):
    for s in (1,2):
        V.paste(rgb('sprite.png',bg)[0].resize((64*s,64*s),Image.NEAREST),(x,y)); x+=64*s+10
d.text((1044,y+140),'eind 1x/2x licht en donker',fill=(0,0,0))
x=0
for n in ('ho_oh','fearow'):
    V.paste(gba(n).resize((512,512),Image.NEAREST),(x,y)); d.text((x,y-12),n+' _gba 8x',fill=(0,0,0)); x+=522
V.save('vel.png')
