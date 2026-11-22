# hulpbeeld: klassenraster (npy) uitsnede op 16x met rasterlijnen en coördinaten
import sys, numpy as np; from PIL import Image, ImageDraw; from toon import COL
o=np.load(sys.argv[2]); y0,y1,x0,x1=map(int,sys.argv[3:7]); z=16
c=o[y0:y1,x0:x1]; im=Image.new('RGB',((x1-x0)*z+30,(y1-y0)*z+20),'white'); d=ImageDraw.Draw(im)
for y in range(y1-y0):
    for x in range(x1-x0):
        v=c[y,x]; d.rectangle([30+x*z,20+y*z,30+x*z+z-1,20+y*z+z-1],fill=COL[v] if v else (200,235,200),outline=(150,150,150))
for x in range(x1-x0): d.text((30+x*z+2,4),str((x+x0)%100),fill='black')
for y in range(y1-y0): d.text((2,20+y*z+2),str(y+y0),fill='black')
im.save(sys.argv[1])
