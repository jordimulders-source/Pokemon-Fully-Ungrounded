import sys; sys.path.insert(0,'r5'); sys.path.insert(0,'.'); sys.path.insert(0,'r2')
import numpy as np
from PIL import Image, ImageDraw
from zones import E,M,ONDERKOP,LIJF
def rgba(fn):
    im=Image.open(fn); X=np.array(im); P=np.array(im.getpalette()[:48],'uint8').reshape(16,3)
    a=P[X]; return Image.fromarray(np.dstack([a,((X>0)*255).astype('uint8')]),'RGBA'),X
A,XA=rgba('r5/claydol_g3r5.png'); B,XB=rgba('r5/claydol_g3r5_paletB.png'); Ei,XE=rgba('eindkeuring/claydol_eind.png')
Mm=M.astype('uint8'); Mi=Image.fromarray(np.dstack([Mm,((E>0)*255).astype('uint8')]),'RGBA')
def onwit(im): b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB')
V=Image.new('RGB',(2140,1640),(236,236,236)); dr=ImageDraw.Draw(V)
for i,(t,im) in enumerate([('r5 (A: zonetinten)',A),('r5 B: alleen palet 5/6 globaal',B),('eind',Ei),('model per spritepixel',Mi)]):
    dr.text((10+i*530,5),t+' 8x',fill=(0,0,0)); V.paste(onwit(im).resize((512,512),0),(10+i*530,20))
y=545; dr.text((10,y),'onderkop + lijf 12x: r5 A | eind | model  (onderkop = rij 29-39, lijf = rij 40+)',fill=(0,0,0))
box=(9,28,51,61)
for i,im in enumerate([A,Ei,Mi]):
    c=onwit(im).crop(box); V.paste(c.resize((c.width*12,c.height*12),0),(10+i*(42*12+10),y+15))
y2=y+15+33*12+15; dr.text((10,y2),'krans 12x: r5 | eind | r6-model (stip)',fill=(0,0,0))
kb=(0,0,62,38)
for i,im in enumerate([A,Ei]):
    c=onwit(im).crop(kb); V.paste(c.resize((c.width*8,c.height*8),0),(10+i*(62*8+10),y2+15))
r6=Image.open('../gemini/claydol_r6.png').crop((150,100,874,480)).resize((500,262)); V.paste(r6,(10+2*(62*8+10),y2+15))
y3=y2+15+38*8+10; dr.text((1600,y),'1x licht/donker: r5 A, B, eind',fill=(0,0,0))
for j,im in enumerate([A,B,Ei]):
    for k,bg in enumerate([(255,255,255),(48,48,56)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); V.paste(b.convert('RGB').resize((128,128),0) if False else b.convert('RGB'),(1600+j*160+k*72,y+15))
D=onwit(A).convert('L').point(lambda v:v//3+150).convert('RGB'); Dp=D.load()
for yy,xx in np.argwhere(XA!=XE): Dp[int(xx),int(yy)]=(220,0,0) if (ONDERKOP|LIJF)[yy,xx] else (0,90,255)
dr.text((1600,y+100),'diff A vs eind (rood=zone-tint, blauw=ogen), 4x',fill=(0,0,0)); V.paste(D.resize((256,256),0),(1600,y+115))
V=V.crop((0,0,2140,max(y3,y+380)+10)); V.save('r5/vel.png')
