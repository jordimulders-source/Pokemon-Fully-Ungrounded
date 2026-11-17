# vel.png r11: kop 8x (p1 | p2 | p3 | r10 | model hoog), variant B; hele sprite 1x op licht/donker (B en rond).
import numpy as np, json; from PIL import Image, ImageDraw
PAL=json.load(open('../r9/palet.json'))
def rgba(f):
    s=np.asarray(Image.open(f)).astype(int); c=np.zeros((64,64,4),np.uint8); c[...,:3]=np.array(PAL,np.uint8)[s]; c[...,3]=(s>0)*255
    return Image.fromarray(c,'RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
M=Image.open('../../referenties/model_v14.png').convert('RGB')
fs=['sprite_B_p1.png','sprite_B_p2.png','sprite_B_p3.png','../r10/sprite_B.png']; KW,KH,Z=26,30,8
vel=Image.new("RGB",(max(5*(KW*Z+12),8*138)+30,30+KH*Z+40+2*(64*2+10)+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'kop 8x: p1 | p2 | p3 | r10 | model hoog',fill=0); y+=16
for i,f in enumerate(fs): vel.paste(op(rgba(f),(255,255,255,255)).crop((0,2,KW,KH+2)).resize((KW*Z,KH*Z),Image.NEAREST),(20+i*(KW*Z+12),y))
vel.paste(M.crop((106+12*1,120+12*3,106+12*23,120+12*29)).resize((KW*Z,KH*Z),Image.LANCZOS),(20+4*(KW*Z+12),y))
y+=KH*Z+24; d.text((20,y),'1x (2x vergroot) op licht / donker: B p1 p2 p3 r10 | rond p1 p2 p3 r10',fill=0); y+=16
alle=fs+['sprite_rond_p1.png','sprite_rond_p2.png','sprite_rond_p3.png','../r10/sprite_rond.png']
for r,c in enumerate([(248,248,248,255),(40,40,48,255)]):
    for i,f in enumerate(alle): vel.paste(op(rgba(f),c).resize((128,128),Image.NEAREST),(20+i*138,y+r*138))
vel.save('vel.png'); print(vel.size)
