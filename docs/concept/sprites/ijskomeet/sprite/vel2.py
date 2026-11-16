# vel_r2: r2 8x | r1 8x | model verkleind 8x ; daaronder r2 op 1x en 2x op licht en donker
from PIL import Image, ImageDraw
def lees(p): return Image.open(p).convert('RGBA')
r2=lees('r2.png'); r1=lees('r1.png'); mod=Image.open('model64.png').convert('RGBA')
def op(im,col,s):
    b=Image.new('RGBA',(64*s,64*s),col+(255,)); b.alpha_composite(im.resize((64*s,64*s),Image.NEAREST)); return b.convert('RGB')
V=Image.new('RGB',(3*512+40,512+30+150),(240,240,240)); d=ImageDraw.Draw(V)
for k,(im,t) in enumerate([(r2,'r2'),(r1,'r1'),(mod,'model verkleind')]):
    V.paste(op(im,(255,255,255),8),(10+k*522,25)); d.text((10+k*522,8),t+' (8x)',fill=(0,0,0))
x=10
for col in [(248,248,240),(40,44,60)]:
    V.paste(op(r2,col,1),(x,560)); x+=74
    V.paste(op(r2,col,2),(x,560)); x+=138
V.save('vel_r2.png')
