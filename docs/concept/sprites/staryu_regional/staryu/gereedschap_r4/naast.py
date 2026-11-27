# naast.py SPRITE.png UIT.png: sprite 10x | model (zelfde uitsnede) | model op schaal 10x
import sys; sys.path.insert(0,'gereedschap_r4'); from gemeen import *
o=np.asarray(Image.open(sys.argv[1]))
a=rgb(o,(255,255,255)).crop((6,8,56,58)).resize((500,500),Image.NEAREST)
m=model_op_schaal().crop((6,8,56,58)).resize((500,500),Image.NEAREST)
M=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
u0=(6-X0)/S+U0; u1=(56-X0)/S+U0; v0=(8-Y0)/S+V0; v1=(58-Y0)/S+V0
M=M.crop((int(f(u0,FX)),int(f(v0,FY)),int(f(u1,FX)),int(f(v1,FY)))).resize((500,500),Image.LANCZOS)
v=Image.new('RGB',(1520,500),'white'); v.paste(a,(0,0)); v.paste(M,(510,0)); v.paste(m,(1020,0)); v.save(sys.argv[2])
