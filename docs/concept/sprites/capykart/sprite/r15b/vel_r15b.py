import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
ld=lambda p: Image.open(os.path.join(H,p)).convert('RGBA')
ims=[('r15b creme',ld('capykart_creme.png')),('r15b wit',ld('capykart_wit.png')),('r15 creme',ld('../r15/capykart_creme.png'))]
BG=(200,212,200,255)
def onbg(im,s,bg=BG):
    b=Image.new('RGBA',(im.width*s,im.height*s),bg); b.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST)); return b
V=Image.new('RGBA',(3*522+10,640),(236,236,236,255)); d=ImageDraw.Draw(V)
for i,(n,im) in enumerate(ims): d.text((10+i*522,2),n+' 8x',fill=(0,0,0)); V.alpha_composite(onbg(im,8),(10+i*522,14))
x=10; y=545; d.text((10,y-12),'1x licht / donker: r15b creme, r15b wit, r15 creme',fill=(0,0,0))
for bg in ((248,248,248,255),(40,40,48,255)):
    for n,im in ims: V.alpha_composite(onbg(im,1,bg),(x,y)); x+=72
    x+=20
V.save(os.path.join(H,'vel.png'))
