import sys
from PIL import Image, ImageDraw
src, out, s = sys.argv[1], sys.argv[2], int(sys.argv[3])
box = tuple(map(int, sys.argv[4].split(','))) if len(sys.argv)>4 else (0,0,64,64)
bg = sys.argv[5] if len(sys.argv)>5 else 'light'
im = Image.open(src).convert('RGBA').crop(box)
w,h = im.size
col = (235,235,235,255) if bg=='light' else (40,40,48,255)
base = Image.new('RGBA',(w,h),col); base.alpha_composite(im)
big = base.resize((w*s,h*s), Image.NEAREST)
if s>=8:
    d = ImageDraw.Draw(big)
    for i in range(w+1):
        c=(255,0,0,255) if (box[0]+i)%8==0 else (128,128,128,90)
        if (box[0]+i)%8==0 or s>=12: d.line([(i*s,0),(i*s,h*s)],fill=c)
    for j in range(h+1):
        c=(255,0,0,255) if (box[1]+j)%8==0 else (128,128,128,90)
        if (box[1]+j)%8==0 or s>=12: d.line([(0,j*s),(w*s,j*s)],fill=c)
big.save(out)
