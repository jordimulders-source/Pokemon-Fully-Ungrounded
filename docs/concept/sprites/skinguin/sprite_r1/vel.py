# vel.png: model verkleind | A 8x | B 8x ; daaronder A en B op 1x (en 2x) op licht en donker
import numpy as np; from PIL import Image, ImageDraw
def rgba(p):
    im=Image.open(p); return im.convert('RGBA')   # opgeslagen met transparency=0
A=rgba('skinguin_A.png'); B=rgba('skinguin_B.png')
for n,im in (('A',A),('B',B)): im.resize((512,512),Image.NEAREST).save(f'skinguin_{n}_8x.png')
m=Image.open('../model/model.png').convert('RGB')
# modeluitsnede = natief bbox (kolom 12..86, rij 16..90) in modelpixels, onderkant gelijk aan de sprite
P=10.24; x0=int(9.25+1-P+12*P); y0=int(9.25+1-P+16*P); mm=m.crop((x0,y0,x0+int(75*P),y0+int(75*P))).resize((488,488),Image.LANCZOS)
G=24; V=Image.new('RGB',(3*512+4*G,512+2*G+40+160),(255,255,255)); d=ImageDraw.Draw(V)
V.paste(mm,(G,G+24)); 
def plak(im,x,y,bg):
    t=Image.new('RGBA',im.size,bg); t.alpha_composite(im); V.paste(t.convert('RGB'),(x,y))
plak(Image.open('skinguin_A_8x.png').convert('RGBA'),2*G+512,G,(232,232,232,255))
plak(Image.open('skinguin_B_8x.png').convert('RGBA'),3*G+1024,G,(232,232,232,255))
for i,t in enumerate(('model (verkleind)','A (8x)','B: verre ski 2 px dichterbij (8x)')): d.text((G+i*(512+G),4),t,fill=(0,0,0))
y=512+2*G+20
for i,(bg) in enumerate(((248,248,248,255),(40,44,56,255))):
    for j,im in enumerate((A,B)):
        plak(im,G+(i*2+j)*(64+G),y,bg)
        plak(im.resize((128,128),Image.NEAREST),G+4*(64+G)+(i*2+j)*(128+G),y,bg)
d.text((G,y-16),'1x en 2x: A, B op licht | A, B op donker',fill=(0,0,0))
V.save('vel.png'); print(V.size)
