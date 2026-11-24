# Vel r14: r14 | r13 | model op 8x, close-ups 12x (arm, achterbeen, rokpanden) naast het model, 1x/2x licht/donker.
import numpy as np; from PIL import Image, ImageDraw
LICHT=(220,220,220); DONKER=(40,44,52)
M=Image.open('../gemini/r9.png').convert('RGB')
def sp(p,bg=LICHT):
    s=Image.open(p).convert('RGBA'); b=Image.new('RGBA',s.size,bg+(255,)); b.alpha_composite(s); return b.convert('RGB')
def mod(x0,y0,x1,y1,z):  # spritecoordinaten -> modeluitsnede op dezelfde schaal
    box=(40.4+12.8*x0,94.2+12.8*y0,40.4+12.8*x1,94.2+12.8*y1)
    return M.crop(tuple(int(round(v)) for v in box)).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def label(im,t):
    W=Image.new('RGB',(im.width,im.height+22),(255,255,255)); W.paste(im,(0,22)); ImageDraw.Draw(W).text((4,5),t,fill=(0,0,0)); return W
r14=sp('mr_prime.png'); r13=sp('../sprite_r13/mr_prime.png')
rows=[]
# rij 1: 8x, model niet afgesneden (sprite-x -3..72, y -2..66)
m8=mod(-3,-2,72,66,8)
rows.append([label(r14.resize((512,512),0),'r14 (8x)'),label(r13.resize((512,512),0),'r13 (8x)'),label(m8,'model r9 (zelfde schaal; kader = 64x64 vanaf x24,y16)')])
d=ImageDraw.Draw(rows[0][2]); d.rectangle([24,22+16,24+512,22+16+512],outline=(255,0,0))
# rij 2: close-ups 12x
for (n,(x0,y0,x1,y1)) in [('verre arm',(42,25,59,42)),('achterbeen',(40,43,64,64)),('rokpanden',(33,46,50,57))]:
    rows.append([label(r14.crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),0),'r14 %s 12x'%n),
                 label(r13.crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),0),'r13'),
                 label(mod(x0,y0,x1,y1,12),'model (zelfde uitsnede)')])
# rij: 1x/2x licht/donker
s=[]
for bg in (LICHT,DONKER):
    a=sp('mr_prime.png',bg); s+= [a, a.resize((128,128),0)]
strip=Image.new('RGB',(64+128+64+128+60,150),(255,255,255)); x=10
for im in s: strip.paste(im,(x,10)); x+=im.width+10
rows.append([label(strip,'1x / 2x licht en donker')])
W=max(sum(i.width for i in r)+20*(len(r)-1) for r in rows); H=sum(max(i.height for i in r) for r in rows)+20*len(rows)
V=Image.new('RGB',(W+20,H+10),(255,255,255)); y=10
for r in rows:
    x=10
    for im in r: V.paste(im,(x,y)); x+=im.width+20
    y+=max(i.height for i in r)+20
V.save('vel.png')
r14_8=Image.new('RGB',(512,512)); r14.resize((512,512),0).save('mr_prime_8x.png')
