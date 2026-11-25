"""Vel r13: 8x r13 creme | r13 wit | r12 creme | r7, maatstaf Zapacha + Dundragoon 8x, toren+achterbak 12x, 1x licht/donker."""
import os
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); S=os.path.join(D,'../../../')
P=lambda p: Image.open(os.path.join(D,p)).convert('RGBA')
r13c=P('capykart_creme.png'); r13w=P('capykart_wit.png'); r12=P('../r12/r12_creme.png'); r7=P('../../eindkeuring/capykart_r7.png')
vis=Image.open(os.path.join(S,'viscacha/af/viscacha.png')).convert('RGBA'); dun=Image.open(os.path.join(S,'dundragoon/af/dundragoon.png')).convert('RGBA')
BG=(200,210,200,255)
def tile(im,sc,box=None):
    if box: im=im.crop(box)
    b=Image.new('RGBA',im.size,BG); b.alpha_composite(im); return b.resize((im.width*sc,im.height*sc),Image.NEAREST)
G=16
row1=[r13c,r13w,r12,r7]; lab1=['r13 creme','r13 wit','r12 creme','r7']
W=4*512+5*G; Hh=G+20+512+G+20+576+G+20+140+G
V=Image.new('RGBA',(W,Hh),(235,235,235,255)); d=ImageDraw.Draw(V)
y=G
for i,(im,l) in enumerate(zip(row1,lab1)):
    x=G+i*(512+G); d.text((x,y),l,fill=(0,0,0,255)); V.paste(tile(im,8),(x,y+20))
y+=20+512+G
x=G
for im,l in ((vis,'maatstaf Zapacha'),(dun,'maatstaf Dundragoon')):
    d.text((x,y),l,fill=(0,0,0,255)); V.paste(tile(im,8),(x,y+20)); x+=512+G
box=(38,0,64,48)
for im,l in ((r13c,'r13 toren+achterbak 12x'),(r12,'r12 toren+achterbak 12x')):
    d.text((x,y),l,fill=(0,0,0,255)); t=tile(im,12,box); V.paste(t,(x,y+20)); x+=t.width+G
y+=20+576+G
d.text((G,y),'1x op licht en donker',fill=(0,0,0,255))
x=G
for bg in ((248,248,248,255),(40,40,48,255)):
    for im in (r13c,r13w,r12,r7):
        b=Image.new('RGBA',(64,64),bg); b.alpha_composite(im); b=b.resize((128,128),Image.NEAREST)
        V.paste(b.resize((64,64),Image.NEAREST),(x,y+20)); x+=64+8
    x+=G
V.save(os.path.join(D,'vel.png'))
