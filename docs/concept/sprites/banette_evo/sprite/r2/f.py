import sys,numpy as np; from view import rgba; from PIL import Image
g=np.load(sys.argv[1]); im=rgba(g); bg=Image.new('RGBA',im.size,(255,255,255,255)); a=Image.alpha_composite(bg,im).convert('RGB')
m=Image.open('../../model/model.png').convert('RGB'); S=968/62
mw=Image.new('RGB',(1400,1400),'white'); mw.paste(m,(200,200)); B=mw.crop((int(24-S)+200,int(1-4*S)+200,int(24+63*S)+200,int(1+60*S)+200)).resize((640,640),Image.LANCZOS)
c=Image.new('RGB',(1290,640),'white'); c.paste(a.resize((640,640),Image.NEAREST),(0,0)); c.paste(B,(650,0)); c.save(sys.argv[2])
