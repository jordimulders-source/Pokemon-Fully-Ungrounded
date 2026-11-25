# Test op spriteschaal: hoornstrook 5 px breed, 40 px lang, 6x vergroot.
# 1 dof ijzer, 2 gepolijst staal, 3 spiegelglans + slijprand, 4 damascus
from PIL import Image, ImageDraw, ImageFont
import math
H,W = 40,5
def strook(fn):
    im = Image.new("RGB",(W,H)); px = im.load()
    for y in range(H):
        for x in range(W): px[x,y] = fn(x,y)
    return im
hx = lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
dof = [hx(c) for c in ("#3E3A38","#5E5854","#6E6862","#7A746C","#4A4542")]
pol = [hx(c) for c in ("#2C3038","#6A7480","#A8B4C0","#D0D8E0","#4A525C")]
spi = [hx(c) for c in ("#14161C","#5A6672","#FFFFFF","#B8C4D0","#2A2E36")]
def damas(x,y):
    v = math.sin((y*0.9) + math.sin(x*1.3)*2.0)
    base = pol[x]
    return tuple(min(255,max(0,int(b + (30 if v>0.3 else -30 if v<-0.3 else 0)))) for b in base)
rows = [("1 dof ijzer",lambda x,y: dof[x]),("2 gepolijst",lambda x,y: pol[x]),
        ("3 spiegel + slijprand",lambda x,y: spi[x]),("4 damascus",damas)]
S=6; f = ImageFont.load_default(size=14)
out = Image.new("RGB",(len(rows)*150+20, H*S+60),"#E6D3A8"); d = ImageDraw.Draw(out)
for i,(n,fn) in enumerate(rows):
    s = strook(fn).resize((W*S,H*S),Image.NEAREST)
    out.paste(s,(20+i*150+40,40)); out.paste(strook(fn),(20+i*150+100,40))
    d.text((20+i*150,12),n,fill="#000",font=f)
out.save("docs/concept/sprites/impala_lijn/staal_test.png")
