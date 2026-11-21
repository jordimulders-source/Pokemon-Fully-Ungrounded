# zoom.py img.png out.png y0 y1 [S] : uitsnede rijen y0..y1 met rasternummers, plus model op dezelfde schaal ernaast
import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGB'); y0,y1=int(sys.argv[3]),int(sys.argv[4]); S=int(sys.argv[5]) if len(sys.argv)>5 else 16
W=im.size[0]; c=im.crop((0,y0,W,y1)).resize((W*S,(y1-y0)*S),Image.NEAREST); d=ImageDraw.Draw(c)
for x in range(W):
    for y in range(y1-y0):
        pass
for x in range(0,W,2): d.text((x*S+2,0),str(x),fill=(255,0,0))
for y in range(y0,y1,2): d.text((1,(y-y0)*S+3),str(y),fill=(255,0,0))
F=W/58; m=Image.open('../model/model_natief.png').convert('RGB').crop((24,3+int(y0/F),82,3+int(y1/F)+1))
m=m.resize((int(58*S*F),int(m.size[1]*S*F)),Image.NEAREST)
v=Image.new('RGB',(c.size[0]+m.size[0]+10,max(c.size[1],m.size[1])),(255,255,255)); v.paste(c,(0,0)); v.paste(m,(c.size[0]+10,0)); v.save(sys.argv[2])
