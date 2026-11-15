# vel: sprite 8x | model op dezelfde schaal 8x ; 1x op licht en donker ; kop close-up 12x (sprite | model)
import sys,numpy as np; from PIL import Image, ImageDraw
SP=sys.argv[1]; UIT=sys.argv[2]
P,PH=5.12,4.1; s=165/46; top=22; left=9
ox=PH+P*(18-left*s); oy=PH+P*(37-top*s); k=P*s  # originele px per spritepixel
mod0=Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')
padm=Image.new("RGB",(1800,1800),(255,255,255)); padm.paste(mod0,(400,400)); mod=padm
def modcrop(x0,y0,x1,y1,z): return mod.crop((int(ox+x0*k)+400,int(oy+y0*k)+400,int(ox+x1*k)+400,int(oy+y1*k)+400)).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
sp=Image.open(SP); spr=sp.convert('RGBA') if False else None
sp.save('/tmp/_v.png',transparency=0); spr=Image.open('/tmp/_v.png').convert('RGBA')
def on(bg,im): b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB')
big=on((255,255,255),spr.resize((512,512),Image.NEAREST)); m8=modcrop(0,0,64,64,8)
KX0,KY0,KX1,KY1=9,22,32,42  # kopvak
kz=12; ks=on((255,255,255),spr.crop((KX0,KY0,KX1,KY1)).resize(((KX1-KX0)*kz,(KY1-KY0)*kz),Image.NEAREST)); km=modcrop(KX0,KY0,KX1,KY1,kz)
W=512*2+30; H=512+20+max(ks.height,140)+20
v=Image.new('RGB',(W,H),(200,200,200)); v.paste(big,(0,0)); v.paste(m8,(542,0))
y=532; v.paste(ks,(0,y)); v.paste(km,(ks.width+10,y))
x=ks.width*2+30
for bg in ((248,248,240),(40,40,56)):
  t=on(bg,spr); v.paste(t,(x,y)); v.paste(on(bg,spr.resize((128,128),Image.NEAREST)),(x+70,y)); y+=135
v.save(UIT)
