# zoom.py PNG x0 y0 x1 y1 UIT: sprite | model (natief) op 16x met spriteraster en nummers
import sys; from PIL import Image, ImageDraw
p,x0,y0,x1,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]; Z=16
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/'
im=Image.open(p); im.save(S+'_z.png',transparency=0); sp=Image.new('RGBA',(64,64),'white'); sp.alpha_composite(Image.open(S+'_z.png').convert('RGBA'))
nat=Image.open('../kleur_r1/natief.png').convert('RGB'); mod=Image.new('RGB',(128,128),'white'); mod.paste(nat,(1,14))
a=sp.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
b=mod.crop((2*x0,2*y0,2*x1,2*y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
W=a.width; v=Image.new('RGB',(2*W+60,a.height+30),'white'); v.paste(a,(30,30)); v.paste(b,(W+60,30)); d=ImageDraw.Draw(v)
for ox in (30,W+60):
    for x in range(x0,x1+1): d.line([(ox+(x-x0)*Z,30),(ox+(x-x0)*Z,v.height)],fill=(255,0,0) if x%5==0 else (255,190,190))
    for y in range(y0,y1+1): d.line([(ox,30+(y-y0)*Z),(ox+W,30+(y-y0)*Z)],fill=(255,0,0) if y%5==0 else (255,190,190))
    for x in range(x0,x1,2): d.text((ox+(x-x0)*Z+3,10),str(x),fill=(0,0,0))
for y in range(y0,y1): d.text((2,30+(y-y0)*Z+3),str(y),fill=(0,0,0))
v.save(uit)
