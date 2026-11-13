# maak_vel.py: abra_r3_8x.png, vel.png (r3 8x | r2 8x | model zelfde schaal | 1x/2x licht/donker/groen),
# closeup.png (onderhelft en handen 12x naast het model)
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/'
def rgba(p):
    im=Image.open(p); im.save(S+'_v.png',transparency=0); return Image.open(S+'_v.png').convert('RGBA')
def op(img,kl):
    b=Image.new('RGBA',img.size,kl); b.alpha_composite(img); return b.convert('RGB')
r3=rgba('abra_r3.png'); r2=rgba('../kleur_r2/abra_r2.png')
r3.resize((512,512),Image.NEAREST).save('abra_r3_8x.png')
nat=Image.open('../kleur_r1/natief.png').convert('RGB')
mod=Image.new('RGB',(128,128),'white'); mod.paste(nat,(1,14))
mod8=mod.resize((512,512),Image.NEAREST)
klein=Image.new('RGB',(512,512),(200,200,200))
for k,kl in enumerate([(248,248,248,255),(40,40,48,255),(144,200,144,255)]):
    klein.paste(op(r3,kl),(16+k*80,16)); klein.paste(op(r3,kl).resize((128,128),Image.NEAREST),(16+k*164,120))
v=Image.new('RGB',(4*532,560),'white'); d=ImageDraw.Draw(v)
for k,(x,t) in enumerate(((op(r3,(255,255,255,255)).resize((512,512),Image.NEAREST),'r3 8x'),(op(r2,(255,255,255,255)).resize((512,512),Image.NEAREST),'r2 8x'),(mod8,'model (natief raster), zelfde schaal'),(klein,'r3 1x en 2x op licht/donker/groen'))):
    v.paste(x,(k*532,40)); d.text((k*532+8,12),t,fill=(0,0,0))
v.save('vel.png')
Z=12; x0,y0,x1,y1=6,36,58,64
sp=op(r3,(255,255,255,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
m=mod.resize((128*Z//2,128*Z//2),Image.NEAREST).crop((x0*Z,y0*Z,x1*Z,y1*Z))
c=Image.new('RGB',(sp.width,2*sp.height+60),'white'); dd=ImageDraw.Draw(c)
dd.text((6,6),'r3 12x (onderhelft en handen)',fill=(0,0,0)); c.paste(sp,(0,24))
dd.text((6,sp.height+34),'model, zelfde schaal',fill=(0,0,0)); c.paste(m,(0,sp.height+56))
c.save('closeup.png')
