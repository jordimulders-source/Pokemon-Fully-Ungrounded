import sys; sys.path.insert(0,'sprite_r1'); import numpy as np; from PIL import Image, ImageDraw; import pal; from render import img
o=np.load('sprite_r3/r3_idx.npy').astype('uint8'); r1=np.load('sprite_r2/r2_idx.npy').astype('uint8'); kaal=np.load('sprite_r1/auto_idx.npy').astype('uint8')
p=Image.fromarray(o,'P'); fl=[v for c in pal.A for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save('sprite_r3/dustly_r3.png',transparency=0)
assert (np.asarray(Image.open('sprite_r3/dustly_r3.png'))==o).all()
img(o,pal.A,8).save('sprite_r3/dustly_r3_8x.png')
LICHT,DONKER=(248,248,240),(40,40,48)
m=Image.open('gemini/r6_a.png').convert('RGB').crop((150,150,880,880)).resize((512,512),Image.LANCZOS)
# gezicht 12x: sprite x9-29,y24-40 ; model natief zelfde stuk op 8x
fx0,fy0,fx1,fy1=9,24,29,40
fk=img(kaal,pal.A,1,LICHT).crop((fx0,fy0,fx1,fy1)).resize(((fx1-fx0)*12,(fy1-fy0)*12),Image.NEAREST).convert('RGB')
fs=img(o,pal.A,1,LICHT).crop((fx0,fy0,fx1,fy1)).resize(((fx1-fx0)*12,(fy1-fy0)*12),Image.NEAREST).convert('RGB')
f1=img(r1,pal.A,1,LICHT).crop((fx0,fy0,fx1,fy1)).resize(((fx1-fx0)*12,(fy1-fy0)*12),Image.NEAREST).convert('RGB')
nx0,ny0=17+(fx0-9)*1.5,18+(fy0-8)*1.5
fm=Image.open('basis/natief.png').convert('RGB').crop((int(nx0),int(ny0),int(nx0+(fx1-fx0)*1.5),int(ny0+(fy1-fy0)*1.5)))
fm=fm.resize((fm.width*8,fm.height*8),Image.NEAREST)
W=3*512+4*16; H=24+512+24+fs.height+24+140
out=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(out)
for i,(c,n) in enumerate(((m,'model r6_a'),(img(r1,pal.A,8,LICHT),'r2'),(img(o,pal.A,8,LICHT),'r3'))):
    out.paste(c.convert('RGB'),(16+i*528,24)); d.text((16+i*528,6),n,fill=(0,0,0))
y=24+512+24; d.text((16,y-16),'gezicht 12x: Gastly Gen 3 | model | kale reductie (A) | r3',fill=(0,0,0))
x=16
ga=Image.open('../../../../graphics/pokemon/gastly/anim_front.png').crop((0,0,64,64)); gb=Image.new('RGBA',(64,64),LICHT+(255,)); gb.alpha_composite(ga.convert('RGBA'))
gf=gb.crop((18,24,46,46)).resize((28*12,22*12),Image.NEAREST).convert('RGB')
W2=sum(c.width for c in (gf,fm,fk,fs))+5*16
if W2>out.width:
    o2=Image.new('RGB',(W2,out.height),(255,255,255)); o2.paste(out,(0,0)); out=o2; d=ImageDraw.Draw(out)
for c in (gf,fm,fk,fs): out.paste(c,(x,y)); x+=c.width+16
y+=fs.height+24; x=16
for bgc in (LICHT,DONKER):
    for s in (1,2):
        c=img(o,pal.A,s,bgc).convert('RGB'); out.paste(c,(x,y)); x+=c.width+8
    x+=24
out.save('sprite_r3/vel.png'); print('ok')
