from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
S=8
sp=Image.open('sprite/r8/sprite_p1.png').convert('RGBA')
W=64*S*2+40; H=64*S+40+200
vel=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(vel)
big=sp.resize((64*S,64*S),Image.NEAREST); vel.alpha_composite(big,(0,30))
d.text((4,4),'r8 p1 8x - rood=MOET, oranje=KAN',fill=(0,0,0))
def ring(box,col,lab):
    x0,y0,x1,y1=box
    d.ellipse((x0*S-6,30+y0*S-6,(x1+1)*S+6,30+(y1+1)*S+6),outline=col,width=3)
    d.text(((x1+1)*S+8,30+y0*S-14),lab.split()[0],fill=col); leg.append((lab,col))
leg=[]
R=(220,0,0);O=(240,140,0)
ring((14,37,14,39),R,'1 wit ringgat (14,38)')
ring((32,16,34,18),R,'2 dambord (33,17)/(33,18)')
ring((14,21,19,25),R,'3 banding linkerrand lijf')
ring((28,15,31,19),O,'K1 knop hoekig')
ring((22,20,28,25),O,'K2 wit klein')
# rechts: 1x vergelijking
x=64*S+40; d.text((x,4),'1x: r8 p1, p2, magnemite, metang, claydol, lunatone, glalie',fill=(0,0,0))
ims=[sp,Image.open('sprite/r8/sprite_p2.png').convert('RGBA')]
for n in ['magnemite','metang','claydol','lunatone','glalie']:
    im=Image.open(G+n+'/anim_front.png').convert('RGBA'); ims.append(im.crop((0,0,64,64)))
for i,im in enumerate(ims):
    vel.alpha_composite(im,(x+(i%4)*70,30+(i//4)*70))
    vel.alpha_composite(im.resize((128,128),Image.NEAREST),(x+(i%4)*130,200+(i//4)*135))
for i,(l,c) in enumerate(leg): d.text((10,64*S+40+i*16),l,fill=c)
vel.save('keuring_r8/vel.png')
