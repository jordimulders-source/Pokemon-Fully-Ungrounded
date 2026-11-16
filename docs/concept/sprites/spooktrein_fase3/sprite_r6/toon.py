# Toont een geestraster (txt) op 16x naast de natieve modeluitsnede.
import sys; from PIL import Image; import numpy as np
C={'6':(65,126,76),'5':(97,179,109),'2':(137,233,137),'W':(232,248,232),'#':(60,55,50),'.':(255,255,255),'3':(77,194,91)}
rows=[l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]
h=len(rows); w=max(len(r) for r in rows)
im=Image.new('RGB',(w,h),(255,255,255))
for y,r in enumerate(rows):
    for x,ch in enumerate(r): im.putpixel((x,y),C.get(ch,(255,0,255)))
n=Image.open('model/natief.png').convert('RGB').crop((29,6,63,22))
Z=16; o=Image.new('RGB',(w*Z+34*Z+16,max(h,16)*Z),(200,200,200))
o.paste(im.resize((w*Z,h*Z),Image.NEAREST),(0,0)); o.paste(n.resize((34*Z,16*Z),Image.NEAREST),(w*Z+16,0))
o.save(sys.argv[2])
