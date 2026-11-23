# vel: V1 | V2 | V3 | r4 R2 | model (echte kleuren uit gemini_v8.png, zelfde uitsnede) — heel op 6x en close-up oog+mond op 16x
from PIL import Image,ImageDraw
def wit(p):
    q=Image.open(p).convert('RGBA'); b=Image.new('RGBA',q.size,(255,255,255,255)); b.alpha_composite(q); return b.convert('RGB')
T=['V1_oog4x5_mond+1+2.png','V2_oog4x6_mond+1+2.png','V3_oog4x5_mond+1+3.png','../r4/R2.png']
L=['V1 oog 4x5, mond +1 rechts +2 omlaag','V2 oog 4x6, mond +1 +2','V3 oog 4x5, mond +1 +3','r4 R2']
G=Image.open('../../r8/gemini_v8.png').convert('RGB'); S=82/60; OY=10
def mpx(x,y): return (-0.99+10.24*(10+(x-2)*S), -0.99+10.24*(13+(y-OY)*S))
def model(x0,y0,x1,y1,size):
    a=mpx(x0,y0); b=mpx(x1,y1); return G.resize(size,Image.LANCZOS,box=(max(0,a[0]),max(0,a[1]),min(1024,b[0]),min(1024,b[1])))
X0,Y0,X1,Y1=10,35,33,54; Z=16
W=(X1-X0)*Z
V=Image.new('RGB',(5*(W+10)+10,400+(Y1-Y0)*Z+60+90),'white'); d=ImageDraw.Draw(V)
for i,(t,l) in enumerate(zip(T,L)):
    V.paste(wit(t).resize((384,384),Image.NEAREST),(10+i*(W+10),30)); d.text((10+i*(W+10),12),l,fill=(0,0,0))
    V.paste(wit(t).crop((X0,Y0,X1,Y1)).resize((W,(Y1-Y0)*Z),Image.NEAREST),(10+i*(W+10),430))
V.paste(model(0,0,64,64,(384,384)),(10+4*(W+10),30)); d.text((10+4*(W+10),12),'model v8 (echte kleuren, zelfde raster)',fill=(0,0,0))
V.paste(model(X0,Y0,X1,Y1,(W,(Y1-Y0)*Z)),(10+4*(W+10),430)); d.text((10,415),'close-up x10-32, y35-53 op 16x',fill=(0,0,0))
x=10
for bgc in ((248,248,240),(40,48,64)):
    for t in T[:3]:
        q=Image.open(t).convert('RGBA'); b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(q); V.paste(b.convert('RGB'),(x,430+(Y1-Y0)*Z+20)); x+=74
V.save('vel.png')
