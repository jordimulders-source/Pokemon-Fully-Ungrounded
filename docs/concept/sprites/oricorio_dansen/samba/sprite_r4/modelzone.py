# hulpbeeld: alleen het natieve model met het spriteraster erover, elke kolom/rij genummerd (laatste cijfer), z px per spritepixel
import numpy as np, sys, json; from PIL import Image, ImageDraw
y0,y1,x0,x1=map(int,sys.argv[1:5]); z=int(sys.argv[6]); F,OY,OX=2.9,0,0.97; pl=json.load(open('plaats.json'))
n=np.asarray(Image.open('natief.png')); h,w=y1-y0,x1-x0
im=Image.new('RGB',(w*z+30,h*z+30),'white'); d=ImageDraw.Draw(im)
for y in range(h*z):
    for x in range(w*z):
        ny=int(((y0+y/z)-pl['dy'])*F+OY); nx=int(((x0+x/z)-pl['dx'])*F+OX)
        if 0<=ny<200 and 0<=nx<200: im.putpixel((30+x,30+y),tuple(int(c) for c in n[ny,nx]))
for k in range(w+1): d.line([30+k*z,30,30+k*z,30+h*z],fill=(255,80,80) if (x0+k)%5==0 else (170,170,170))
for k in range(h+1): d.line([30,30+k*z,30+w*z,30+k*z],fill=(255,80,80) if (y0+k)%5==0 else (170,170,170))
for x in range(w): d.text((30+x*z+z//3,4 if (x+x0)%2 else 16),str((x+x0)%100),fill='black')
for y in range(h): d.text((2,30+y*z+z//3),str(y+y0),fill='black')
im.save(sys.argv[5])
