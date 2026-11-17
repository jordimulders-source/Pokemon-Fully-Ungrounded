# Hoofd van hoofdarmen_r1 vergroten (Jordi: "is dat iets wat jij kan maken?"); armen, kruizen, Shuppets blijven.
import sys; from PIL import Image, ImageDraw; import numpy as np
S=float(sys.argv[1]); DY=int(sys.argv[2]); OUT=sys.argv[3]
im=Image.open('bron.png').convert('RGB')
g=[(210,170),(400,170),(520,240),(700,110),(820,130),(900,200),(1005,330),(1005,440),(900,430),(830,420),(830,600),(800,700),(780,820),(810,1050),(540,1050),(470,880),(380,800),(300,720),(230,710),(115,700),(115,600),(200,590),(200,300)]
poly=[(200+x/2,150+y/2) for x,y in g]
m=Image.new('L',im.size,0); ImageDraw.Draw(m).polygon(poly,fill=255)
a=np.asarray(im).astype(int); nw=a.min(2)<235
m=Image.fromarray(((np.asarray(m)>0)&nw).astype('uint8')*255)
bb=m.getbbox(); head=im.crop(bb); hm=m.crop(bb)
cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
W,H=int(head.width*S),int(head.height*S)
head=head.resize((W,H),Image.NEAREST); hm=hm.resize((W,H),Image.NEAREST)
out=im.copy(); out.paste(head,(int(cx-W/2),int(cy-H/2)+DY),hm)
out.save(OUT)
