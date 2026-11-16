# Keuringsvel r2: r2 8x met MOET-markeringen | natief model op dezelfde schaal | 1x/2x r1, r2 en Gen 3-refs
from PIL import Image, ImageDraw; import numpy as np
R='../../../../graphics/pokemon/'
S=8; X0,Y0,X1,Y1=14,5,49,57
sp=Image.open('sprite_r2/pitahaya_r2.png').convert('RGBA'); r1=Image.open('sprite_r2/pitahaya_r1.png').convert('RGBA')
def wit(im): b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b
A=wit(sp).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*S,(Y1-Y0)*S),Image.NEAREST)
nat=Image.open('sprite_r2/natief.png').convert('RGBA'); c0=1+3*(X0+1); r0=3*(Y0+2)
B=nat.crop((c0,r0,c0+3*(X1-X0),r0+3*(Y1-Y0))).resize(A.size,Image.NEAREST)
M={ # kleur: punten
 (255,0,0):[(37,10),(36,15),(29,18),(38,27),(35,19)],                 # M1 losse naadpixel -> vul
 (255,140,0):[(25,14),(30,13),(31,14),(31,15)],                       # M2 zwart in licht kopvlak
 (0,90,255):[(25,39),(25,40),(33,39),(20,43),(21,43),(21,44),(17,45),(24,50),(25,51)],# M3 lijf lichtkant
 (200,0,200):[(23,49),(23,50),(20,52),(21,52)],                       # M4 buitenlijn lichtkant
 (0,170,0):[(38,39),(39,39),(38,40)],                                  # M5 dambord
 (0,200,200):[(38,28),(38,29),(38,30),(37,31),(35,39),(35,40),(36,40),(37,40),(37,41)], # M6 dunne zwarte binnenlijn -> selout
}
d=ImageDraw.Draw(A)
for col,pts in M.items():
  for x,y in pts:
    px,py=(x-X0)*S,(y-Y0)*S; d.rectangle([px,py,px+S-1,py+S-1],outline=col+(255,),width=2)
d.rectangle([(18-X0)*S,(22-Y0)*S,(35-X0)*S-1,(35-Y0)*S-1],outline=(120,120,120,255))  # gezicht (ter info)
W=Image.new('RGBA',(max(A.width*2+30,1000), A.height+190),(235,235,235,255))
W.alpha_composite(A,(0,20)); W.alpha_composite(B,(A.width+30,20))
t=ImageDraw.Draw(W)
t.text((2,4),'r2 8x: rood M1, oranje M2, blauw M3, paars M4, groen M5, cyaan M6',fill=(0,0,0,255))
t.text((A.width+32,4),'natief model (zelfde raster); grijs kader = gezicht, info',fill=(0,0,0,255))
y=A.height+30; x=6
def plak(im,sc,label):
  global x
  im=im.crop((0,0,64,64)).resize((64*sc,64*sc),Image.NEAREST); W.alpha_composite(im,(x,y)); t.text((x,y+64*sc+2),label,fill=(0,0,0,255)); x+=64*sc+8
plak(r1,1,'r1'); plak(sp,1,'r2'); plak(r1,2,'r1 2x'); plak(sp,2,'r2 2x')
for n in ['bagon','treecko','larvitar','oddish']:
  im=Image.open(R+n+'/anim_front_gba.png').convert('RGBA')
  im=im.crop((0,0,64,64)); a=np.array(im); 
  # transparant = kleur linksboven
  bg=a[0,0].copy(); m=(a[...,:3]==bg[:3]).all(2); a[m,3]=0; plak(Image.fromarray(a),2,n)
W.save('keuring_r2/vel.png')
