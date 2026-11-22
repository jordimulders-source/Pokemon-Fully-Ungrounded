# vel.png r6: r6 | r5 op 8x ; diff (gewijzigde pixels magenta) ; kop 12x r6 | r5 ; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r6=rgba('cumbia.png'); r5=rgba('r5_ref.png'); d6=np.load('diff_r6.npy')
W=Image.new('RGB',(3*522,30+512+30+312+20),(230,230,230)); d=ImageDraw.Draw(W)
dm=op(r6,'white',8); dd=ImageDraw.Draw(dm)
for y,x in zip(*np.where(d6)): dd.rectangle([x*8,y*8,x*8+7,y*8+7],outline=(255,0,255),width=2)
for k,(im,t) in enumerate([(op(r6,'white',8),'r6'),(op(r5,'white',8),'r5'),(dm,'r6 met gewijzigde pixels (magenta), %d px'%d6.sum())]):
    W.paste(im,(k*522,30)); d.text((k*522+4,8),t,fill='black')
y=572; d.text((4,y-16),'kop 12x: r6 | r5 ; 1x licht/donker r6 | r5',fill='black')
W.paste(op(r6.crop((16,3,42,29)),'white',12),(0,y)); W.paste(op(r5.crop((16,3,42,29)),'white',12),(324,y))
W.paste(op(r6,(255,255,255),1),(660,y)); W.paste(op(r6,(40,40,48),1),(730,y)); W.paste(op(r5,(255,255,255),1),(820,y)); W.paste(op(r5,(40,40,48),1),(890,y))
W.save('vel.png'); print(W.size)
