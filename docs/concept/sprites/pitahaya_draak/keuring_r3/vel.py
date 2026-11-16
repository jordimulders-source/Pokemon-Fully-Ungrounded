from PIL import Image, ImageDraw; import numpy as np
R='../../../../graphics/pokemon/'; S=8; X0,Y0,X1,Y1=14,5,49,57
def wit(im): b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b
r3=Image.open('sprite_r3/pitahaya_r3.png').convert('RGBA'); r2=Image.open('sprite_r2/pitahaya_r2.png').convert('RGBA'); sim=Image.open('keuring_r3/sim_moet.png').convert('RGBA')
A=wit(r3).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*S,(Y1-Y0)*S),Image.NEAREST)
nat=Image.open('sprite_r2/natief.png').convert('RGBA'); c0=1+3*(X0+1); r0=3*(Y0+2)
B=nat.crop((c0,r0,c0+3*(X1-X0),r0+3*(Y1-Y0))).resize(A.size,Image.NEAREST)
d=ImageDraw.Draw(A)
for col,pts in {(255,0,0):[(35,19),(37,10),(29,18),(36,15),(41,24)],(0,90,255):[(41,42)],(255,170,0):[(43,27),(43,28),(41,30),(38,34),(28,35),(30,13)]}.items():
  for x,y in pts: px,py=(x-X0)*S,(y-Y0)*S; d.rectangle([px,py,px+S-1,py+S-1],outline=col+(255,),width=2)
W=Image.new('RGBA',(1000,A.height+190),(235,235,235,255)); W.alpha_composite(A,(0,20)); W.alpha_composite(B,(A.width+30,20))
t=ImageDraw.Draw(W); t.text((2,4),'r3 8x: rood/blauw = MOET, oranje = KAN',fill=(0,0,0,255)); t.text((A.width+32,4),'natief model, zelfde raster',fill=(0,0,0,255))
y=A.height+30; x=6
def plak(im,sc,l):
  global x
  im=im.crop((0,0,64,64)).resize((64*sc,64*sc),Image.NEAREST); W.alpha_composite(im,(x,y)); t.text((x,y+64*sc+2),l,fill=(0,0,0,255)); x+=64*sc+8
plak(r2,1,'r2'); plak(r3,1,'r3'); plak(r2,2,'r2 2x'); plak(r3,2,'r3 2x'); plak(sim,2,'r3+MOET 2x')
for n in ['bagon','treecko','larvitar']:
  a=np.array(Image.open(R+n+'/anim_front_gba.png').convert('RGBA').crop((0,0,64,64))); m=(a[...,:3]==a[0,0,:3]).all(2); a[m,3]=0; plak(Image.fromarray(a),2,n)
W.save('keuring_r3/vel.png')
