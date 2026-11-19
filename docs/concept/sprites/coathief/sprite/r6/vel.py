# vel.png: r6 | r5 | Mightyena | Linoone (8x); lijf-close-up r6 vs r5 (12x); r6 1x licht/donker.
import os; from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); J=lambda *p: os.path.join(D,*p)
G=os.path.join(D,'..','..','..','..','..','..','graphics','pokemon')
def op(p,kleur,crop=None):
  im=Image.open(p)
  if crop: im=im.crop(crop)
  im=im.convert('RGBA'); b=Image.new('RGBA',im.size,kleur); b.alpha_composite(im); return b
W=(255,255,255,255)
def gen3(n):  # eerste frame, achtergrondindex 0 transparant
  im=Image.open(os.path.join(G,n,'anim_front.png')).crop((0,0,64,64)); im.info['transparency']=0
  p=J('_'+n+'.png'); im.save(p,transparency=0); return op(p,W)
r6=op(J('coathief_r6.png'),W); r5=op(J('..','r5','coathief_r5.png'),W)
vel=Image.new('RGBA',(4*512+60,512+20+28*12+20),(235,235,235,255)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate([(r6,'r6'),(r5,'r5'),(gen3('mightyena'),'Mightyena'),(gen3('linoone'),'Linoone')]):
  vel.paste(im.resize((512,512),Image.NEAREST),(i*532,0)); d.text((i*532+4,4),t,fill=(200,0,0))
y0=532; box=(19,28,52,56)
for i,(im,t) in enumerate([(r6,'lijf r6 12x'),(r5,'lijf r5 12x')]):
  w=(box[2]-box[0])*12; vel.paste(im.crop(box).resize((w,(box[3]-box[1])*12),Image.NEAREST),(i*(w+20),y0)); d.text((i*(w+20)+4,y0+2),t,fill=(200,0,0))
x=2*((box[2]-box[0])*12+20)
for kleur in [(255,255,255,255),(248,240,224,255),(40,40,48,255),(0,0,0,255)]:
  vel.paste(op(J('coathief_r6.png'),kleur),(x,y0)); x+=74
d.text((2*((box[2]-box[0])*12+20),y0+70),'r6 1x op licht/donker',fill=(60,60,60))
vel.convert('RGB').save(J('vel.png'))
for n in ['mightyena','linoone']: os.remove(J('_'+n+'.png'))
