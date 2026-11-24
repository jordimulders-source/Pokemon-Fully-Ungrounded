# vel: r2 | r1 | model (A boven, B onder) op 8x, plus 1x/2x op licht en donker
from PIL import Image,ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
m0=Image.open('../r1/natief.png').convert('RGB'); m=Image.new('RGB',(120,120),'white'); m.paste(m0,(10,10)); S=82/60; oy=63-round(73/S)
mv=m.resize((64,64),Image.BOX,box=(20-2*S,23-oy*S,20+62*S,23+(64-oy)*S)).convert('RGBA')
rows=[[rgba('A.png'),rgba('../r1/A.png'),mv],[rgba('B.png'),rgba('../r1/B.png'),mv]]
lab=['r2','r1','model v8 verkleind']
V=Image.new('RGB',(3*400+20,2*390+40+150),'white'); d=ImageDraw.Draw(V)
for j,row in enumerate(rows):
    for i,im in enumerate(row):
        b=Image.new('RGBA',(64,64),(255,255,255,255)); b.alpha_composite(im)
        V.paste(b.resize((384,384),Image.NEAREST).convert('RGB'),(10+i*400,30+j*395)); d.text((10+i*400,15+j*395),('A ' if j==0 else 'B ')+lab[i],fill=(0,0,0))
x=10
for bgc in ((248,248,240),(40,48,64)):
    for im in (rows[0][0],rows[1][0]):
        for z in (1,2):
            b=Image.new('RGBA',(64*z,64*z),bgc+(255,)); b.alpha_composite(im.resize((64*z,64*z),Image.NEAREST)); V.paste(b.convert('RGB'),(x,820)); x+=64*z+10
V.save('vel.png')
