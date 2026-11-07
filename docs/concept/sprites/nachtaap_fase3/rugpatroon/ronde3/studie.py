# Studievel: banden in echte Gen 3-sprites (3x) + close-ups 8x.
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
F2='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_evo/af/nachtaap_evo.png'
def load(p,back=False):
    im=Image.open(p).convert('RGBA')
    if im.size[1]==128: im=im.crop((0,0,64,64))
    bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg
refs=[('fase 2',F2)]+[(n,G+n+'/anim_front_gba.png') for n in ['furret','dusclops','linoone','raikou','zigzagoon','sentret','typhlosion']]+[('typhlosion rug',G+'typhlosion/back_gba.png'),('furret rug',G+'furret/back_gba.png')]
crops=[('fase 2 8x',F2,(14,22,44,44)),('furret 8x',G+'furret/anim_front_gba.png',(20,26,50,48)),('dusclops 8x',G+'dusclops/anim_front_gba.png',(14,20,44,42))]
W=5*200; H=2*215+260
sheet=Image.new('RGBA',(max(W,3*250),H),(235,235,240,255)); d=ImageDraw.Draw(sheet)
for i,(n,p) in enumerate(refs):
    x=(i%5)*200; y=(i//5)*215
    sheet.paste(load(p).resize((192,192),Image.NEAREST),(x+4,y+18)); d.text((x+4,y+4),n+' (3x)',fill=(0,0,0,255))
for i,(n,p,b) in enumerate(crops):
    im=load(p).crop(b); im=im.resize((im.size[0]*8,im.size[1]*8),Image.NEAREST)
    x=i*250; y=2*215
    im=im.resize((240,int(240*im.size[1]/im.size[0])),Image.NEAREST)
    sheet.paste(im,(x+4,y+18)); d.text((x+4,y+4),n,fill=(0,0,0,255))
sheet.save('studie_banden.png')
