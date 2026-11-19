# vel.png: r1 8x | model op dezelfde schaal | oude sprite 8x ; daaronder kop r1 vs model 12x, r1 1x licht/donker.
import os; from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); J=lambda *p: os.path.join(D,*p)
def rgba(p):
  im=Image.open(p); return im.convert('RGBA')
def op(im,kleur):
  b=Image.new('RGBA',im.size,kleur); b.alpha_composite(im); return b
r1=rgba(J('coathief_r1.png')); oud=rgba(J('..','..','af','coathief.png'))
m=Image.open(J('..','..','gemini','r1_prompt_v1.png')).convert('RGBA')
# uitlijning gemeten: spritepixel (x,y) = model (16x+22 .. , 16y-16 ..)
mm=Image.new('RGBA',(1024,1024),(255,255,255,255)); mm.paste(m,(-22,16))
W=(255,255,255,255)
vel=Image.new('RGBA',(3*512+40,512+20+12*30+20+80),(235,235,235,255)); d=ImageDraw.Draw(vel)
vel.paste(op(r1,W).resize((512,512),Image.NEAREST),(0,0))
vel.paste(mm.resize((512,512),Image.LANCZOS),(532,0))
vel.paste(op(oud,W).resize((512,512),Image.NEAREST),(1064,0))
for t,x in [('r1',4),('model (Gemini r1)',536),('oude sprite',1068)]: d.text((x,4),t,fill=(200,0,0))
y0=532; box=(4,28,34,58)  # kop + geheven poot
k=op(r1,W).crop(box).resize((30*12,30*12),Image.NEAREST); vel.paste(k,(0,y0))
km=mm.crop((box[0]*16,box[1]*16,box[2]*16,box[3]*16)).resize((360,360),Image.LANCZOS); vel.paste(km,(380,y0))
d.text((4,y0+2),'kop r1 12x',fill=(200,0,0)); d.text((384,y0+2),'kop model 12x',fill=(200,0,0))
x=780
for kleur in [(255,255,255,255),(248,240,224,255),(40,40,48,255),(0,0,0,255)]:
  vel.paste(op(r1,kleur),(x,y0)); x+=74
vel.paste(op(r1,(152,208,160,255)).resize((128,128),Image.NEAREST),(780,y0+80))
d.text((780,y0+212),'r1 1x op licht/donker, 2x op Gen 3-groen',fill=(60,60,60))
vel.convert('RGB').save(J('vel.png'))
