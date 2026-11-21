# veeromtrekken (rood) over het natieve model, spriteraster; controle of de vormen het model volgen
from PIL import Image, ImageDraw
from veren import VEREN
n=Image.open('natief.png').convert('RGB'); Z=12
x0=67+2*(0-4); y0=13+2*(6-9)
pad=Image.new('RGB',(n.width+100,n.height+100),'white'); pad.paste(n,(50,50))
im=pad.crop((x0+50,y0+50,x0+50+128,y0+50+104)).resize((128*Z//2*1,104*Z//2),Image.NEAREST)
# 1 spritepixel = 2 natief = Z px ; sprite (c,r) -> beeld ((c-0)*Z, (r-6)*Z)
im=pad.crop((x0+50,y0+50,x0+50+128,y0+50+104)).resize((64*Z,52*Z),Image.NEAREST); d=ImageDraw.Draw(im)
for nm,k,pts in VEREN:
    P=[(x*Z,(y-6)*Z) for x,y in pts]; d.line(P+[P[0]],fill=(255,0,0) if k=='F' else ((0,0,255) if k=='W' else (255,0,255)),width=2)
    d.text((pts[0][0]*Z,(pts[0][1]-6)*Z),nm,fill='black')
im.save('/tmp/claude-0/overlay.png')
