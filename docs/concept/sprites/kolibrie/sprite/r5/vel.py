# gifs (frame1 <-> frame2, 4x, 0,5 s) en vel.png: r1 | a | b op 12x (zone), 8x (geheel) en 1x
import numpy as np; from PIL import Image, ImageDraw
pal=np.array([tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[3:19]])
def rgba(p,crop=None):
    a=np.array(Image.open(p));
    if crop: a=a[crop[1]:crop[3],crop[0]:crop[2]]
    return Image.fromarray(np.dstack([pal[a],np.where(a==0,0,255)]).astype('uint8'),'RGBA')
for v in 'ab':
    fr=[]
    for p in ('frame1.png','frame2_%s.png'%v):
        c=Image.new('RGB',(256,256),(248,248,248)); s=rgba(p).resize((256,256),0); c.paste(s,(0,0),s); fr.append(c)
    fr[0].save('anim_%s.gif'%v,save_all=True,append_images=[fr[1]],duration=500,loop=0)
F=[('r1','../r1/frame2.png'),('a','frame2_a.png'),('b','frame2_b.png')]
G=12; Z=(38,6,56,25); zw,zh=(Z[2]-Z[0])*12,(Z[3]-Z[1])*12
V=Image.new('RGB',(G+3*(512+G),G+18+zh+G+18+512+G+18+80),(60,60,68)); d=ImageDraw.Draw(V)
for k,(t,p) in enumerate(F):
    x=G+k*(512+G); y=G
    d.text((x,y),t+' zone 12x',fill=(255,255,255)); V.paste(Image.new('RGB',(zw,zh),(200,200,208)),(x,y+16)); s=rgba(p,Z).resize((zw,zh),0); V.paste(s,(x,y+16),s)
    y=G+18+zh+G
    d.text((x,y),t+' 8x',fill=(255,255,255)); V.paste(Image.new('RGB',(512,512),(200,200,208)),(x,y+16)); s=rgba(p).resize((512,512),0); V.paste(s,(x,y+16),s)
    d.rectangle([x+Z[0]*8,y+16+Z[1]*8,x+Z[2]*8,y+16+Z[3]*8],outline=(255,80,80))
    y=y+16+512+G
    for j,bg in enumerate([(248,248,248),(32,32,40)]):
        V.paste(Image.new('RGB',(68,68),bg),(x+j*74,y)); s=rgba(p); V.paste(s,(x+2+j*74,y+2),s)
V.save('vel.png'); print(V.size)
