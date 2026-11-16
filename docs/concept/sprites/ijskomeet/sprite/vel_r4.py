# vel_r4: r4 | r3 | model (8x); daaronder 1x/2x licht/donker; r4 op 2x naast regice en lunatone
from PIL import Image, ImageDraw
G='../../../../../graphics/pokemon/'
def rgba(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
def mon(s):
    im=rgba(G+s+'/anim_front.png'); px=im.load(); bg=px[0,0]
    if bg[3]==255:
        for y in range(64):
            for x in range(64):
                if px[x,y]==bg: px[x,y]=(0,0,0,0)
    return im
def op(im,c):
    b=Image.new('RGBA',im.size,c+(255,)); b.alpha_composite(im); return b.convert('RGB')
r4,r3=rgba('r4.png'),rgba('r3.png'); mod=Image.open('keuring/model3x_r2.png').convert('RGBA')
W=Image.new('RGB',(1600,1000),(255,255,255)); d=ImageDraw.Draw(W)
for i,(im,n) in enumerate([(r4,"r4"),(r3,"r3"),(mod,'model (natief /3)')]):
    W.paste(op(im,(255,255,255)).resize((512,512),0),(10+530*i,24)); d.text((10+530*i,6),n,fill=0)
y=560; x=10
for im,n in [(r4,"r4"),(r3,"r3")]:
    for c in [(255,255,255),(40,40,48)]:
        W.paste(op(im,c),(x,y)); W.paste(op(im,c).resize((128,128),0),(x+70,y)); x+=210
    d.text((x-420,y+132),n+' (1x/2x licht, donker)',fill=0)
y=720; x=10
for im,n in [(r4,'r4'),(mon('regice'),'regice'),(mon('lunatone'),'lunatone')]:
    W.paste(op(im,(255,255,255)).resize((128,128),0),(x,y)); W.paste(op(im,(104,160,112)).resize((128,128),0),(x,y+140)); d.text((x,y-14),n,fill=0); x+=150
W.save('vel_r4.png')
