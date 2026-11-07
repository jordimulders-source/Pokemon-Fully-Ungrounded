# box1x.py ronde uit.png [x0 y0 x1 y1 zoom]: BOX-verkleind model | sprite, pixel voor pixel vergroot
import sys; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
m=Image.open(P+'silhouet/model_64_box.png').convert('RGB')
p=Image.open(P+sys.argv[1]+'/potoo.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(64,160,64,255)); bg.alpha_composite(p); s=bg.convert('RGB')
x0,y0,x1,y1,z=list(map(int,sys.argv[3:8])) if len(sys.argv)>3 else [0,0,64,64,8]
o=Image.new('RGB',(2*(x1-x0)*z+8,(y1-y0)*z),'white')
o.paste(m.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),(0,0))
o.paste(s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),((x1-x0)*z+8,0))
o.save(sys.argv[2])
