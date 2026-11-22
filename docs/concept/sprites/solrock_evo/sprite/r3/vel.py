# vel: r2A | r3A | r3A letterlijk | r2B | r3B | r3B letterlijk op 8x (uitsnede kern), Solrocks oog op 8x, alles op 1x licht/donker
from PIL import Image, ImageDraw
def rgba(f,bg):
    Image.open(f).save('/tmp/_v.png',transparency=0)
    c=Image.open('/tmp/_v.png').convert('RGBA'); b=Image.new('RGBA',c.size,bg); b.alpha_composite(c); return b
L=(232,236,224,255); D=(40,44,64,255)
F=[('../r2/A.png','r2 A'),('A.png','r3 A (aangepast)'),('A_letterlijk.png','r3 A letterlijk'),
   ('../r2/B.png','r2 B'),('B.png','r3 B (aangepast)'),('B_letterlijk.png','r3 B letterlijk')]
z=8; W=64*z; pad=12
vel=Image.new('RGBA',(3*(W+pad)+pad+17*z+pad, 2*(W+pad+16)+pad+150),(255,255,255,255)); d=ImageDraw.Draw(vel)
for n,(f,t) in enumerate(F):
    x=pad+(n%3)*(W+pad); y=pad+(n//3)*(W+pad+16)
    d.text((x,y),t,fill=(0,0,0)); vel.paste(rgba(f,L).resize((W,W),Image.NEAREST),(x,y+14))
sr=Image.open('../../../../../../graphics/pokemon/solrock/anim_front_gba.png').convert('RGBA').crop((26,26,43,47))
x=pad+3*(W+pad); d.text((x,pad),'Solrock-oog 8x',fill=(0,0,0)); vel.paste(sr.resize((17*z,21*z),Image.NEAREST),(x,pad+14))
y=pad+2*(W+pad+16); x=pad
for f,t in F:
    d.text((x,y),t,fill=(0,0,0))
    vel.paste(rgba(f,L),(x,y+14)); vel.paste(rgba(f,D),(x,y+14+68))
    x+=150
vel.save('vel.png'); print(vel.size)
