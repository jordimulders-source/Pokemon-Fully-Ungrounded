from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
L=(200,220,200,255); D=(40,44,52,255)
def sp(p,front=True):
    return Image.open(p).convert('RGBA').crop((0,0,64,64))
def on(im,z,bg):
    b=Image.new('RGBA',(64*z,64*z),bg); b.alpha_composite(im.resize((64*z,64*z),Image.NEAREST)); return b
new=sp('nachtaap_fase3.png'); old=sp('../ronde1s/nachtaap_fase3.png')
model=Image.open('../../silhouet/onderlaag_256.png').convert('RGBA').resize((192,192),Image.LANCZOS)
refs=[sp(G+'vigoroth/anim_front_gba.png'),sp(G+'aipom/anim_front_gba.png'),sp(G+'primeape/anim_front_gba.png'),sp(G+'aipom/back_gba.png'),sp(G+'salamence/anim_front_gba.png'),sp(G+'linoone/anim_front_gba.png')]
names=['vigoroth','aipom','primeape','aipom (back)','salamence','linoone']
W=1600; H=256+30+192+30+192+30+80
out=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(out)
d.text((4,2),'ronde 3 lijf 4x licht / 4x donker',fill=(0,0,0,255))
out.paste(on(new,4,L),(4,14)); out.paste(on(new,4,D),(270,14))
d.text((540,2),'3x: ronde1s (basis) | ronde3_lijf | model',fill=(0,0,0,255))
out.paste(on(old,3,L),(540,14)); out.paste(on(new,3,L),(740,14))
m=Image.new('RGBA',(192,192),L); m.alpha_composite(model); out.paste(m,(940,14))
d.text((1140,2),'1x: 1s | r3 (licht, donker)',fill=(0,0,0,255))
for i,(im,bg) in enumerate([(old,L),(new,L),(old,D),(new,D)]):
    out.paste(on(im,1,bg),(1140+(i%2)*70,14+(i//2)*70))
y=300; d.text((4,y-14),'referenties 3x',fill=(0,0,0,255))
for i,(r,n) in enumerate(zip(refs,names)):
    out.paste(on(r,3,L),(4+i*198,y)); d.text((4+i*198,y+194),n,fill=(0,0,0,255))
y=520; d.text((4,y-14),'3x ronde3_lijf naast dezelfde referenties',fill=(0,0,0,255))
out.paste(on(new,3,L),(4,y))
for i,r in enumerate(refs[:3]): out.paste(on(r,3,L),(204+i*198,y))
out.paste(on(new,1,L),(820,y)); 
for i,r in enumerate(refs[:3]): out.paste(on(r,1,L),(890+i*70,y))
out.save('vel.png')
# varianten
V=['nachtaap_fase3.png']+['varianten/dij_min%d.png'%k for k in (1,2,3,4)]
lab=['ronde3_lijf (0)','dij -1','dij -2','dij -3','dij -4']
o=Image.new('RGBA',(5*200+8,192+30+80),(255,255,255,255)); d=ImageDraw.Draw(o)
for i,(p,l) in enumerate(zip(V,lab)):
    im=sp(p); o.paste(on(im,3,L),(4+i*200,16)); d.text((4+i*200,2),l,fill=(0,0,0,255))
    o.paste(on(im,1,L),(4+i*200,216)); o.paste(on(im,1,D),(74+i*200,216))
o.save('vel_varianten.png')
