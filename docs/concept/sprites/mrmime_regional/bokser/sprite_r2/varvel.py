# varianten.png: uitsneden op 8x naast elkaar (ogen, vuisten, V) + model-uitsnede
import sys; from PIL import Image, ImageDraw
def crop8(p,box,Z=12):
    im=Image.open(p).convert('RGBA').crop(box); bg=Image.new('RGB',im.size,(232,240,232)); bg.paste(im,(0,0),im)
    return bg.resize((im.size[0]*Z,im.size[1]*Z),Image.NEAREST)
m=Image.open('../r12.png').convert('RGB'); pad=Image.new('RGB',(1424,1424),(255,255,255)); pad.paste(m,(200,200))
p=10.24; ph=10.25; s=88/63
def mod(box,Z=12):
    x0,y0,x1,y1=box; X=lambda c:200+ph+(12+(c-10)*s)*p; Y=lambda r:200+ph+(5+r*s)*p
    return pad.crop((int(X(x0)),int(Y(y0)),int(X(x1)),int(Y(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
rijen=[('ogen + snor',(29,5,43,19),[('A: MM, puntjes','var/oog_A.png'),('B: als model','var/oog_B.png'),('C: onderlid','var/oog_C.png')]),
       ('vuisten',(8,8,48,28),[('D: donker+tape','var/vuist_D.png'),('L: licht','var/vuist_L.png')]),
       ('V-patroon',(29,16,42,27),[('vlak','var/vuist_D.png'),('lijn 2px','var/v_lijn.png')])]
blokken=[]
for titel,box,vs in rijen:
    ims=[(t,crop8(f,box)) for t,f in vs]+[('model r12',mod(box))]
    w=sum(i.size[0]+16 for _,i in ims); h=ims[0][1].size[1]+30
    r=Image.new('RGB',(w,h),(255,255,255)); d=ImageDraw.Draw(r); x=0
    for t,i in ims: r.paste(i,(x,24)); d.text((x,4),t,fill=(0,0,0)); x+=i.size[0]+16
    blokken.append(r)
W=max(b.size[0] for b in blokken); H=sum(b.size[1]+10 for b in blokken)
o=Image.new('RGB',(W,H),(255,255,255)); y=0
for bl in blokken: o.paste(bl,(0,y)); y+=bl.size[1]+10
o.save('varianten.png')
