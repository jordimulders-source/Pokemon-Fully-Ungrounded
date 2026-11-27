# vel r3: poten 12x (r3|r2|model), hele sprite 8x (r3|r2|model) met rode modelomtrek over r3, 1x/2x naast dodrio en fearow
import numpy as np; from PIL import Image, ImageDraw
import lib1 as lib, modelover
R3='terreurvogel_bijl_r3.png'; R2='../sprite_bijl_r2/oog_B.png'
def groot(p,s):
    a=Image.open(p).convert('RGBA').resize((64*s,64*s),Image.NEAREST); b=Image.new('RGBA',a.size,(255,255,255,255)); b.alpha_composite(a); return b
def omtrek(s):
    m=np.asarray(Image.open('../gemini/r1_eenvoud.png').convert('RGB')).astype(int).min(2)<225
    f=lib.S/10.24*s; ox=(lib.OX+((0-9.25)/10.24-lib.X0)*lib.S)*s; oy=(lib.OY+((0-9.25)/10.24-lib.Y0)*lib.S)*s
    z=Image.fromarray((m*255).astype('uint8')).resize((round(1024*f),round(1024*f)),Image.BILINEAR); c=Image.new('L',(64*s,64*s),0); c.paste(z,(round(ox),round(oy)))
    M=np.asarray(c)>127; P=np.pad(M,1); return M&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
def gba(n):
    im=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%n).crop((0,0,64,64))
    pal=[int(v) for l in open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/normal_gba.pal'%n).read().split('\n')[3:19] for v in l.split()]
    im.putpalette(pal+[0]*(768-48)); a=np.array(im.convert('RGBA')); a[np.array(im)==0,3]=0; return Image.fromarray(a)
z=12; pb=(0,44*z,62*z,63*z); pw=pb[2]-pb[0]; ph=pb[3]-pb[1]
W=3*(64*8+10)+10; H=30+ph+40+(64*8-160)+40+140
vel=Image.new('RGBA',(max(W,3*(pw+10)+10),H),(236,236,236,255)); d=ImageDraw.Draw(vel)
for i,(t,im) in enumerate([('poten r3 12x',groot(R3,z)),('poten r2 12x',groot(R2,z)),('model 12x',modelover.model_op(z).convert('RGBA'))]):
    x=10+i*(pw+10); vel.alpha_composite(im.crop(pb),(x,24)); d.text((x,8),t,fill=(0,0,0))
y2=24+ph+30
r3=groot(R3,8); a=np.array(r3); a[omtrek(8)]=(230,0,0,255); r3o=Image.fromarray(a)
for i,(t,im) in enumerate([('r3 8x + rode modelomtrek',r3o),('r2 (oog B) 8x',groot(R2,8)),('model 8x',modelover.model_op(8).convert('RGBA'))]):
    x=10+i*(512+10); vel.alpha_composite(im.crop((0,160,512,512)),(x,y2)); d.text((x,y2-16),t,fill=(0,0,0))
y3=y2+352+30
x=10
for j,(bg,nm) in enumerate([((248,248,240,255),'licht'),((40,44,52,255),'donker')]):
    d.text((x,y3-14),nm+': r3 1x | r2 1x | dodrio | fearow | r3 2x',fill=(0,0,0))
    for k,(src,s) in enumerate([(R3,1),(R2,1),('dodrio',1),('fearow',1),(R3,2)]):
        b=Image.new('RGBA',(64*s,64*s),bg)
        im=gba(src) if src in('dodrio','fearow') else Image.open(src).convert('RGBA')
        b.alpha_composite(im.resize((64*s,64*s),Image.NEAREST)); vel.alpha_composite(b,(x+k*70,y3))
    x+=500
vel.save('vel.png'); print(vel.size)
