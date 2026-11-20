# vel: r8 8x | r7 8x | model (natief raster, zelfde schaal en uitlijning) | 1x en 2x op licht/donker
from PIL import Image, ImageDraw
def plat(f,bg):
    s=Image.open(f).convert('RGBA'); t=Image.new('RGB',(64,64),bg); t.paste(s,(0,0),s); return t
n=Image.open('../sprite_r1/natief.png').convert('RGB')
M=Image.new('RGB',(128,128),(255,255,255)); M.paste(n,(2*15-18,2*18-4))   # sprite(x,y) <-> natief(2(x-15)+18, 2(y-18)+4)
M=M.resize((512,512),Image.NEAREST)
V=Image.new('RGB',(3*528+16+200,560),(255,255,255)); d=ImageDraw.Draw(V)
for i,(l,im) in enumerate([('r8 8x',plat('rufflet_r8.png',(255,255,255)).resize((512,512),0)),
                          ('r7 8x',plat('../sprite_r7/rufflet_r7.png',(255,255,255)).resize((512,512),0)),('model (natief, zelfde schaal)',M)]):
    V.paste(im,(16+i*528,36)); d.text((16+i*528,14),l,fill=(0,0,0))
x=16+3*528
for j,bg in enumerate([(232,232,232),(40,44,56)]):
    V.paste(plat('rufflet_r8.png',bg),(x,36+j*200)); V.paste(plat('rufflet_r8.png',bg).resize((128,128),0),(x+68,36+j*200))
d.text((x,14),'r8 1x / 2x',fill=(0,0,0)); V.save('vel.png')
