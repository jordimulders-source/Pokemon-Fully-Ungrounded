# zoom.py SPRITE x0 y0 x1 y1 UIT : sprite-uitsnede 16x met raster/coordinaten | model (natief) op dezelfde plek, zelfde schaal
import sys; from PIL import Image, ImageDraw
sp,x0,y0,x1,y1,uit=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
Z=16
im=Image.open(sp); im.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/_t.png',transparency=0)
im=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/_t.png').convert('RGBA')
c=im.crop((x0,y0,x1,y1)); b=Image.new('RGBA',c.size,(255,255,255,255)); b.alpha_composite(c); b=b.convert('RGB').resize((c.width*Z,c.height*Z),Image.NEAREST)
nat=Image.open('../kleur_r1/natief.png').convert('RGB')
# spritepixel (x,y) = natief blok vanaf (2x-1, 2y-14)
m=nat.crop((2*x0-1,2*y0-14,2*x1-1,2*y1-14)).resize((c.width*Z,c.height*Z),Image.NEAREST)
W=c.width*Z; H=c.height*Z
v=Image.new('RGB',(2*W+60,H+30),'white'); v.paste(b,(30,30)); v.paste(m,(W+60,30)); d=ImageDraw.Draw(v)
for k in range(c.width+1):
    for ox in (30,W+60): d.line([(ox+k*Z,30),(ox+k*Z,30+H)],fill=(255,0,0) if (x0+k)%5==0 else (230,180,180))
for k in range(c.height+1):
    for ox in (30,W+60): d.line([(ox,30+k*Z),(ox+W,30+k*Z)],fill=(255,0,0) if (y0+k)%5==0 else (230,180,180))
for k in range(c.width):
    if (x0+k)%5==0: d.text((30+k*Z+2,2),str(x0+k),fill=(0,0,0)); d.text((W+60+k*Z+2,2),str(x0+k),fill=(0,0,0))
for k in range(c.height):
    if (y0+k)%5==0: d.text((2,30+k*Z+2),str(y0+k),fill=(0,0,0))
v.save(uit)
