import sys
from PIL import Image, ImageDraw
# gebruik: crop.py uit.png naam:x0:y0 ...  (14x14 uitsnede, 16x, met coördinaten)
S=22; N=9
items=[a.split(':') for a in sys.argv[2:]]
W=Image.new('RGB',(len(items)*(N*S+30)+30,N*S+50),(255,255,255)); d=ImageDraw.Draw(W)
for i,(n,x0,y0) in enumerate(items):
    x0,y0=int(x0),int(y0)
    im=Image.open(f'/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/{n}/anim_front_gba.png').crop((0,0,64,64)).convert('RGBA').crop((x0,y0,x0+N,y0+N))
    bg=Image.new('RGBA',im.size,(230,230,230,255)); bg.alpha_composite(im)
    big=bg.convert('RGB').resize((N*S,N*S),Image.NEAREST); dd=ImageDraw.Draw(big)
    for k in range(0,N*S,S): dd.line([(k,0),(k,N*S)],fill=(190,190,190)); dd.line([(0,k),(N*S,k)],fill=(190,190,190))
    X=30+i*(N*S+30)
    W.paste(big,(X,40)); d.text((X,2),n,fill=(0,0,0))
    for k in range(0,N,2):
        d.text((X+k*S+3,26),str(x0+k),fill=(0,0,200)); d.text((X-22,40+k*S+3),str(y0+k),fill=(0,0,200))
W.save(sys.argv[1])
