import sys; sys.path.insert(0,'sprite_r1'); import numpy as np; from PIL import Image, ImageDraw; import pal; from render import img
o=np.load('sprite_r2/r2_idx.npy').astype('uint8'); r1=np.load('sprite_r2/r1_idx.npy').astype('uint8')
p=Image.fromarray(o,'P'); fl=[v for c in pal.A for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save('sprite_r2/dustly_r2.png',transparency=0)
assert (np.asarray(Image.open('sprite_r2/dustly_r2.png'))==o).all()
img(o,pal.A,8).save('sprite_r2/dustly_r2_8x.png')
LICHT,DONKER=(248,248,240),(40,40,48)
m=Image.open('gemini/r6_a.png').convert('RGB').crop((150,150,880,880)).resize((512,512),Image.LANCZOS)
# gezicht 12x: sprite x9-29,y24-40 ; model natief zelfde stuk op 8x
fx0,fy0,fx1,fy1=9,24,29,40
fs=img(o,pal.A,1,LICHT).crop((fx0,fy0,fx1,fy1)).resize(((fx1-fx0)*12,(fy1-fy0)*12),Image.NEAREST).convert('RGB')
f1=img(r1,pal.A,1,LICHT).crop((fx0,fy0,fx1,fy1)).resize(((fx1-fx0)*12,(fy1-fy0)*12),Image.NEAREST).convert('RGB')
nx0,ny0=17+(fx0-9)*1.5,18+(fy0-8)*1.5
fm=Image.open('basis/natief.png').convert('RGB').crop((int(nx0),int(ny0),int(nx0+(fx1-fx0)*1.5),int(ny0+(fy1-fy0)*1.5)))
fm=fm.resize((fm.width*8,fm.height*8),Image.NEAREST)
W=3*512+4*16; H=24+512+24+fs.height+24+140
out=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(out)
for i,(c,n) in enumerate(((m,'model r6_a'),(img(r1,pal.A,8,LICHT),'r1 A'),(img(o,pal.A,8,LICHT),'r2'))):
    out.paste(c.convert('RGB'),(16+i*528,24)); d.text((16+i*528,6),n,fill=(0,0,0))
y=24+512+24; d.text((16,y-16),'gezicht 12x: model | r1 A | r2',fill=(0,0,0))
x=16
for c in (fm,f1,fs): out.paste(c,(x,y)); x+=c.width+16
y+=fs.height+24; x=16
for bgc in (LICHT,DONKER):
    for s in (1,2):
        c=img(o,pal.A,s,bgc).convert('RGB'); out.paste(c,(x,y)); x+=c.width+8
    x+=24
out.save('sprite_r2/vel.png'); print('ok')
