from PIL import Image, ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
m=Image.open('../model/gemini_r10.png').convert('RGB'); x0,y0,s=19.3344,29.216,950.272; k=s/64
b=(36,6,56,20); mc=m.crop((int(x0+b[0]*k),int(y0+b[1]*k),int(x0+b[2]*k),int(y0+b[3]*k))).resize((20*12,14*12),Image.LANCZOS)
V=[(rgba('samba_%s.png'%v),t) for v,t in (('A','A = r10 (huidig)'),('B','B = kleine veer naar links'),('C','C = hybride'))]
W=Image.new('RGB',(3*532,30+512+40+168+40+70),(232,232,232)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate(V): W.paste(op(im,'white',8),(i*532,30)); d.text((i*532+4,10),t+' (8x)',fill='black')
y=30+512+40; d.text((4,y-18),'12x uitsnede x36-56, y6-20: A | B | C | model',fill='black')
for i,(im,t) in enumerate(V): W.paste(op(im.crop(b),'white',12),(i*250,y))
W.paste(mc,(3*250,y))
y=y+168+40; d.text((4,y-18),'1x: A | B | C op wit, donker, gevechtsgroen',fill='black'); xx=0
for bg in [(255,255,255),(40,40,48),(152,208,160)]:
    for im,t in V: W.paste(op(im,bg,1),(xx,y)); xx+=68
    xx+=16
W.save('varianten.png')
