# Klasseer natieve modelpixels in letters (meting, geen tekenen). Gebruik: python3 klas.py x0 x1 y0 y1
import sys; from PIL import Image; import numpy as np, colorsys
a=np.asarray(Image.open(sys.argv[5] if len(sys.argv)>5 else '../model/natief.png').convert('RGB')).astype(int)
def k(p):
    r,g,b=p; s=r+g+b
    if s>700: return '.'
    h,l,sat=colorsys.rgb_to_hls(r/255,g/255,b/255)
    if s<120: return 'K'
    if g>r+25 and g>b:  # groen
        if l>0.62: return 'L'
        if l>0.45: return 'G'
        if l>0.30: return 'g'
        return 'd'
    if r>g+25:  # bruin/roest
        if l>0.55: return 'P'
        if l>0.38: return 'B'
        if l>0.22: return 'b'
        return 'x'
    if l>0.6: return 'W'
    if l>0.42: return 'S'
    if l>0.22: return 's'
    return 'K'
x0,x1,y0,y1=map(int,sys.argv[1:5])
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%3d '%y+''.join(k(a[y,x]) for x in range(x0,x1)))
