# vel.png r13: kop 8x (a | b | c | r12 p2 | model hoog | Jordi omcirkeld); ogen 16x (linkeroog a,b,c | rechteroog);
# hele sprite 1x (2x getoond) op licht/donker.
import numpy as np, json; from PIL import Image, ImageDraw
PAL=json.load(open('../r9/palet.json'))
def rgba(f):
    s=np.asarray(Image.open(f)).astype(int); c=np.zeros((64,64,4),np.uint8); c[...,:3]=np.array(PAL,np.uint8)[s]; c[...,3]=(s>0)*255
    return Image.fromarray(c,'RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
M=Image.open('../../referenties/model_v14.png').convert('RGB')
fs=['sprite_B_a.png','sprite_B_b.png','sprite_B_c.png','../r12/sprite_B_p2.png']; KW,KH,Z=26,30,8
vel=Image.new('RGB',(6*(KW*Z+12)+30,30+KH*Z+40+8*16+40+2*138+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'kop 8x: a | b | c | r12 p2 | model hoog | Jordi omcirkeld',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).crop((0,2,KW,KH+2)).resize((KW*Z,KH*Z),Image.NEAREST),(20+i*(KW*Z+12),y))
vel.paste(M.crop((106+12*1,120+12*3,106+12*23,120+12*29)).resize((KW*Z,KH*Z),Image.LANCZOS),(20+4*(KW*Z+12),y))
J=Image.open('../../referenties/jordi_linkeroog_omcirkeld.png').convert('RGB'); J=J.resize((int(J.size[0]*KH*Z/J.size[1]),KH*Z)); vel.paste(J,(20+5*(KW*Z+12),y))
y+=KH*Z+24; d.text((20,y),'16x: linkeroog a | b | c | r12 p2 (x2-8, y18-26)   ||   rechteroog (x10-16, y18-26)',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).crop((2,18,8,26)).resize((96,128),Image.NEAREST),(20+i*108,y))
vel.paste(op(rgba(fs[0]),(255,255,255,255)).crop((10,18,16,26)).resize((96,128),Image.NEAREST),(20+4*108+30,y))
y+=8*16+24; d.text((20,y),'1x (2x getoond) op licht / donker: B a b c r12p2 | rond a b c',fill=0); y+=16
alle=fs+['sprite_rond_a.png','sprite_rond_b.png','sprite_rond_c.png']
for r,c in enumerate([(248,248,248,255),(40,40,48,255)]):
    for i,f in enumerate(alle): vel.paste(op(rgba(f),c).resize((128,128),Image.NEAREST),(20+i*138,y+r*138))
vel.save('vel.png'); print(vel.size)
