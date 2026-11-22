import numpy as np; from PIL import Image, ImageDraw
S=11.87; X0=138-0.5*S; Y0=107-1.2*S
def rgba(f,bg):
    Image.open(f).save('/tmp/_v.png',transparency=0)
    c=Image.open('/tmp/_v.png').convert('RGBA'); b=Image.new('RGBA',c.size,bg); b.alpha_composite(c); return b
L=(232,236,224,255); D=(40,44,64,255)
m=Image.open('../../referenties/model.png').convert('RGBA')
mod=m.crop((int(X0),int(Y0),int(X0+64*S),int(Y0+64*S))).resize((64,64),Image.LANCZOS)
sp=rgba('sprite.png',L)
z=8;W=512;pad=12
# gezicht: sprite x13-37,y22-46 op 16x; model zelfde stuk op dezelfde schaal
fx0,fy0,fx1,fy1=13,22,37,46; fz=16
face=sp.crop((fx0,fy0,fx1,fy1)).resize(((fx1-fx0)*fz,(fy1-fy0)*fz),Image.NEAREST)
mface=m.crop((int(X0+fx0*S),int(Y0+fy0*S),int(X0+fx1*S),int(Y0+fy1*S))).resize(face.size,Image.LANCZOS)
H=pad+14+W+pad+14+face.height+pad+150
vel=Image.new('RGBA',(2*W+3*pad,max(H,0)),(255,255,255,255)); d=ImageDraw.Draw(vel)
d.text((pad,pad),'r4 (8x)',fill=(0,0,0)); vel.paste(sp.resize((W,W),Image.NEAREST),(pad,pad+14))
d.text((2*pad+W,pad),'model verkleind (8x)',fill=(0,0,0)); vel.paste(mod.resize((W,W),Image.NEAREST),(2*pad+W,pad+14))
y=pad+14+W+pad
d.text((pad,y),'gezicht r4 (16x)',fill=(0,0,0)); vel.paste(face,(pad,y+14))
d.text((2*pad+W,y),'gezicht model (zelfde schaal)',fill=(0,0,0)); vel.paste(mface,(2*pad+W,y+14))
y+=14+face.height+pad
d.text((pad,y),'1x licht / donker / wit, en 2x',fill=(0,0,0))
for k,bg in enumerate([L,D,(255,255,255,255)]): vel.paste(rgba('sprite.png',bg),(pad+k*72,y+14))
vel.paste(sp.resize((128,128),Image.NEAREST),(pad+3*72+20,y+14))
vel.save('vel.png'); print(vel.size)
