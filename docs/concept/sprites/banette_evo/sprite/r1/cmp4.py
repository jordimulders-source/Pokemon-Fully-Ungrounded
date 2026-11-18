import sys,numpy as np; from view import rgba; from PIL import Image
g=np.load(sys.argv[1]); out=sys.argv[2]; z=int(sys.argv[3]) if len(sys.argv)>3 else 4
im=rgba(g); bg=Image.new('RGBA',im.size,(255,255,255,255)); im=Image.alpha_composite(bg,im).convert('RGB')
m=Image.open('../../model/model.png').convert('RGB'); mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200)); S=968/62
mb=(24-S,1-4*S,24+63*S,1+60*S); mm=mw.crop(tuple(int(round(v))+200 for v in mb)).resize((64*z,64*z),Image.LANCZOS)
c=Image.new('RGB',(64*z*2+20,64*z),'white'); c.paste(im.resize((64*z,64*z),Image.NEAREST),(0,0)); c.paste(mm,(64*z+20,0)); c.save(out)
