import sys,numpy as np; from PIL import Image, ImageDraw
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
X0,Y0,X1,Y1=17,21,38,29; z=int(sys.argv[1].split("z")[-1].split(".")[0]) if "z" in sys.argv[1].split("/")[-1] else 12
n=Image.open('natief.png').convert('RGB'); nx=OX+3*(xmin-x0); ny=OY+3*(ymin-y0)
gm=n.crop((nx+3*X0,ny+3*Y0,nx+3*X1,ny+3*Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST)
fs=sys.argv[2:]; W,H=gm.size; v=Image.new('RGB',(W,(len(fs)+1)*(H+14)),'white'); d=ImageDraw.Draw(v)
for k,f in enumerate(fs):
    b=Image.new('RGBA',(64,64),(214,222,214,255)); b.alpha_composite(Image.open(f).convert('RGBA'))
    v.paste(b.convert('RGB').crop((X0,Y0,X1,Y1)).resize((W,H),Image.NEAREST),(0,k*(H+14)+14)); d.text((0,k*(H+14)),f,fill='black')
v.paste(gm,(0,len(fs)*(H+14)+14)); d.text((0,len(fs)*(H+14)),'model',fill='black'); v.save(sys.argv[1])
