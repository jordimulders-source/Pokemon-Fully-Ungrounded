import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..')
ld=lambda p: Image.open(p).convert('RGBA')
c14=ld(os.path.join(H,'capykart_creme.png')); w14=ld(os.path.join(H,'capykart_wit.png'))
c13=ld(os.path.join(H,'../r13/capykart_creme.png')); m=ld(os.path.join(R,'referenties/model_r5.png'))
BG=(200,212,200,255)
def onbg(im,s,bg=BG):
    b=Image.new('RGBA',(im.width*s,im.height*s),bg); b.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST)); return b
mt=m.crop((600,100,880,560)); mt=mt.resize((int(mt.width*8/12),int(mt.height*8/12)),Image.NEAREST)
tiles=[('r14 creme 8x',onbg(c14,8)),('r13 creme 8x',onbg(c13,8)),('model toren (8x-schaal)',mt),
       ('r14 toren 12x',onbg(c14.crop((40,0,64,40)),12)),('r13 toren 12x',onbg(c13.crop((40,0,64,40)),12)),('r14 wit toren 12x',onbg(w14.crop((40,0,64,40)),12))]
W=sum(t.width for _,t in tiles[:3])+40; row1=max(t.height for _,t in tiles[:3]); row2=max(t.height for _,t in tiles[3:])
V=Image.new('RGBA',(max(W,sum(t.width for _,t in tiles[3:])+40),row1+row2+200),(236,236,236,255)); d=ImageDraw.Draw(V)
x=10
for n,t in tiles[:3]: d.text((x,2),n,fill=(0,0,0)); V.alpha_composite(t,(x,14)); x+=t.width+10
x=10; y=row1+30
for n,t in tiles[3:]: d.text((x,y-12),n,fill=(0,0,0)); V.alpha_composite(t,(x,y)); x+=t.width+10
y+=row2+20; d.text((10,y-12),'1x licht / donker: r14 creme, r14 wit, r13 creme',fill=(0,0,0)); x=10
for bg in ((248,248,248,255),(40,40,48,255)):
    for im in (c14,w14,c13): V.alpha_composite(onbg(im,1,bg),(x,y)); x+=72
    x+=20
V.save(os.path.join(H,'vel.png'))
