# vel.py: r6 8x | r5 8x | model (zelfde schaal); 1x en 2x op licht en donker
import sys; from PIL import Image, ImageDraw
X0,Y0,NX,NY=[int(v) for v in open('info.txt').read().split()]
def op(f,bgc=(255,255,255)):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(Image.open(f).convert('RGBA')); return b.convert('RGB')
n=Image.open('natief.png')
mod=Image.new('RGB',(128,128),'white'); cx,cy=NX-X0*2,NY-Y0*2; mod.paste(n.crop((max(cx,0),max(cy,0),cx+128,cy+128)),(max(-cx,0),max(-cy,0)))
pan=[op('vuurduivel_r6.png').resize((512,512),Image.NEAREST),op('../sprite_r5/vuurduivel_r5.png').resize((512,512),Image.NEAREST),mod.resize((512,512),Image.NEAREST)]
v=Image.new('RGB',(3*522,20+512+30+150),(235,235,235)); d=ImageDraw.Draw(v)
for i,(p,t) in enumerate(zip(pan,['r6 (8x)','r5 (8x)','model (zelfde schaal)'])):
    v.paste(p,(i*522,20)); d.text((i*522+4,4),t,fill='black')
y=20+512+30; d.text((4,y-14),'r6 1x en 2x op licht en donker',fill='black')
for i,c in enumerate([(255,255,255),(200,220,200),(40,40,56),(16,16,16)]):
    v.paste(op('vuurduivel_r6.png',c),(i*74,y)); v.paste(op('vuurduivel_r6.png',c).resize((128,128),Image.NEAREST),(320+i*138,y))
v.save('vel.png')
