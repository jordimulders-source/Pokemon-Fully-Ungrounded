# D opnieuw: armstuk niet meer in het hoofd, armen (met kruizen, draden, Shuppets) DYA px lager.
import sys; from PIL import Image, ImageDraw; import numpy as np
S=1.8; DY=-20; DYA=int(sys.argv[1]); OUT=sys.argv[2]
im=Image.open('../hoofdarmen_groter/bron.png').convert('RGB')
g=[(215,178),(400,170),(520,240),(700,110),(820,130),(900,200),(1004,325),(1004,440),(900,440),(830,420),(830,600),(800,700),(780,820),(810,1050),(540,1050),(470,880),(380,800),(300,720),(230,715),(115,705),(115,600),(240,600),(300,640),(300,410),(250,370),(205,320)]
poly=[(200+x/2,150+y/2) for x,y in g]
m=Image.new('L',im.size,0); ImageDraw.Draw(m).polygon(poly,fill=255)
a=np.asarray(im).astype(int); nw=a.min(2)<235
m=Image.fromarray(((np.asarray(m)>0)&nw).astype('uint8')*255)
bb=m.getbbox(); head=im.crop(bb); hm=m.crop(bb)
cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
W,H=int(head.width*S),int(head.height*S)
head=head.resize((W,H),Image.NEAREST); hm=hm.resize((W,H),Image.NEAREST)
base=Image.new('RGB',im.size,'white'); base.paste(im,(0,DYA))
base.paste(head,(int(cx-W/2),int(cy-H/2)+DY),hm)
base.save(OUT)
