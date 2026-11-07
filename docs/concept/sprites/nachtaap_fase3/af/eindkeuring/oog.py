# Linkeroog op 16x naast rechteroog + proef (kopie; sprite blijft ongewijzigd)
from PIL import Image, ImageDraw
AF='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_fase3/af/'
src=Image.open(AF+'nachtaap_fase3.png')
proef=src.copy(); p=proef.load()
p[5,37]=15; p[6,37]=12   # glans + donkere iris boven
proef.save(AF+'eindkeuring/proef_oog.png')
def z(im,box,s):
    c=im.crop(box).convert('RGBA'); w,h=c.size
    o=Image.new('RGB',(w*s,h*s),(248,248,248)); c=c.resize((w*s,h*s),Image.NEAREST)
    m=Image.frombytes('L',im.crop(box).size,bytes(255 if v else 0 for v in im.crop(box).tobytes())).resize((w*s,h*s),Image.NEAREST)
    o.paste(c,(0,0),m); d=ImageDraw.Draw(o)
    for x in range(0,w*s,s): d.line((x,0,x,h*s),fill=(120,120,120))
    for y in range(0,h*s,s): d.line((0,y,w*s,y),fill=(120,120,120))
    return o
box=(1,33,17,44)
a=z(src,box,16); b=z(proef,box,16)
def one(im,s):
    c=im.convert('RGBA').crop((0,20,24,50)); m=Image.frombytes('L',(24,30),bytes(255 if v else 0 for v in im.crop((0,20,24,50)).tobytes()))
    o=Image.new('RGB',c.size,(248,248,248)); o.paste(c,(0,0),m); return o.resize((c.size[0]*s,c.size[1]*s),Image.NEAREST)
W=a.width*2+24; vel=Image.new('RGB',(W,a.height+200),(255,255,255))
vel.paste(a,(0,0)); vel.paste(b,(a.width+24,0))
for i,im in enumerate([src,proef]):
    vel.paste(one(im,1),(i*(a.width+24)+4,a.height+10)); vel.paste(one(im,4),(i*(a.width+24)+40,a.height+10))
d=ImageDraw.Draw(vel); d.text((4,a.height+150),'nu',fill=0); d.text((a.width+28,a.height+150),'proef: (5,37)=15, (6,37)=12',fill=0)
vel.save(AF+'eindkeuring/oog16.png')
