"""Hulp: uitsnede van raster en gemini64 naast elkaar, 20x met raster en coordinaten. Gebruik: zoomvel.py raster x0 y0 x1 y1 uit.png"""
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7'); from palet import PAL
from PIL import Image, ImageDraw, ImageFont
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/'
rp,x0,y0,x1,y1,out=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
r=[l.rstrip('\n') for l in open(rp)][:64]; im=Image.new('RGB',(64,64)); im.putdata([(255,255,255) if c=='.' else PAL[int(c,16)] for row in r for c in row])
g=Image.open(D+'gemini64.png').convert('RGB'); Z=20; F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
w,h=(x1-x0)*Z,(y1-y0)*Z; W=Image.new('RGB',(2*w+60,h+30),'white'); d=ImageDraw.Draw(W)
for i,src in enumerate((im,g)):
    ox=30+i*(w+10); W.paste(src.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(ox,20))
    for x in range(x0,x1+1): d.line([(ox+(x-x0)*Z,20),(ox+(x-x0)*Z,20+h)],fill=(200,200,200) if x%5 else (90,90,255))
    for y in range(y0,y1+1): d.line([(ox,20+(y-y0)*Z),(ox+w,20+(y-y0)*Z)],fill=(200,200,200) if y%5 else (90,90,255))
    for x in range(x0,x1,2): d.text((ox+(x-x0)*Z+3,5),str(x),fill='black',font=F)
for y in range(y0,y1,1): d.text((2,20+(y-y0)*Z+5),str(y),fill='black',font=F)
W.save(out)
