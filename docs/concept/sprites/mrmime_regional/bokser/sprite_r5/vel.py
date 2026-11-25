# vel.png: r5 | r3 | r4 | model (8x) + 1x; kop_12x.png: koppen r5 | r3 | r4 | model op 12x
from PIL import Image, ImageDraw
def sp(p,box=(0,0,64,64),Z=8):
    im=Image.open(p).convert('RGBA').crop(box); bg=Image.new('RGB',im.size,(232,240,232)); bg.paste(im,(0,0),im)
    return bg.resize((im.size[0]*Z,im.size[1]*Z),Image.NEAREST)
m=Image.open('../r12.png').convert('RGB'); pad=Image.new('RGB',(1424,1424),(255,255,255)); pad.paste(m,(200,200))
p=10.24; ph=10.25; s=88/63
def mod(box,Z):
    x0,y0,x1,y1=box; X=lambda c:200+ph+(12+(c-10)*s)*p; Y=lambda r:200+ph+(5+r*s)*p
    return pad.crop((int(X(x0)),int(Y(y0)),int(X(x1)),int(Y(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
F=[('r5','bokser.png'),('r3','../sprite_r3/bokser.png'),('r4','../sprite_r4/bokser.png')]
for naam,box,Z in [('vel.png',(0,0,64,64),8),('kop_12x.png',(24,0,56,20),12)]:
    ims=[(t,sp(f,box,Z)) for t,f in F]+[('model r12',mod(box,Z))]
    w=ims[0][1].size[0]; o=Image.new('RGB',(4*(w+10)+(120 if naam=='vel.png' else 0),ims[0][1].size[1]+24),(255,255,255)); d=ImageDraw.Draw(o)
    for i,(t,im) in enumerate(ims): o.paste(im,(i*(w+10),22)); d.text((i*(w+10),5),t,fill=(0,0,0))
    if naam=='vel.png':
        ra=Image.open('bokser.png').convert('RGBA')
        for i,c in enumerate([(248,248,248),(40,48,64)]):
            t=Image.new('RGB',(80,80),c); t.paste(ra,(8,8),ra); o.paste(t,(4*(w+10)+20,22+i*100))
    o.save(naam)
b=sp('bokser.png'); w=Image.new('RGB',b.size,(255,255,255)); im=Image.open('bokser.png').convert('RGBA').resize((512,512),Image.NEAREST); w.paste(im,(0,0),im); w.save('bokser_8x.png')
