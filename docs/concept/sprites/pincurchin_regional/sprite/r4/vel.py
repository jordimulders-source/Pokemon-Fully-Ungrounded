# vel: R1 | R2 | R3 | r3 B115_c3 (8x) + close-up oog 16x met het model op dezelfde uitsnede
from PIL import Image,ImageDraw
def wit(p):
    q=Image.open(p).convert('RGBA'); b=Image.new('RGBA',q.size,(255,255,255,255)); b.alpha_composite(q); return b.convert('RGB')
T=['R1.png','R2.png','R3.png','../r3/B115_c3.png']; L=['R1 oog x14-17, mond voor oog','R2 oog x14-17, oog voor mond','R3 oog x13-16, kolom x13 lijfrand','r3 B115_c3']
S=82/60; oy=63-round(73/S); m00=Image.open('../r1/natief.png').convert('RGB'); m0=Image.new('RGB',(120,120),'white'); m0.paste(m00,(10,10))
X0,Y0,X1,Y1=10,36,24,48
def mod(x0,y0,x1,y1,size): return m0.resize(size,Image.NEAREST,box=(20+(x0-2)*S,23+(y0-oy)*S,20+(x1-2)*S,23+(y1-oy)*S))
V=Image.new('RGB',(5*410+10,410+(Y1-Y0)*16+40+150),'white'); d=ImageDraw.Draw(V)
for i,(t,l) in enumerate(zip(T,L)):
    V.paste(wit(t).resize((384,384),Image.NEAREST),(10+i*410,30)); d.text((10+i*410,12),l,fill=(0,0,0))
    V.paste(wit(t).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*16,(Y1-Y0)*16),Image.NEAREST),(10+i*410,430))
V.paste(mod(0,0,64,64,(384,384)),(10+4*410,30)); d.text((10+4*410,12),'model v8 (natief, zelfde raster)',fill=(0,0,0))
V.paste(mod(X0,Y0,X1,Y1,((X1-X0)*16,(Y1-Y0)*16)),(10+4*410,430)); d.text((10,415),'close-up x10-23, y36-47 op 16x',fill=(0,0,0))
x=10
for bgc in ((248,248,240),(40,48,64)):
    for t in T[:3]:
        q=Image.open(t).convert('RGBA'); b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(q); V.paste(b.convert('RGB'),(x,430+(Y1-Y0)*16+20)); x+=74
V.save('vel.png')
