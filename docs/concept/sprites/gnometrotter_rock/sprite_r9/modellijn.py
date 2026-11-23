# modellijn.py: per spritepixel het aandeel donkere modellijn (lum < T per kleurgroep) -> lijn.npy
import numpy as np; from PIL import Image
m=np.array(Image.open('../r8/gemini_r8.png').convert('RGB')).astype(float); L=m.mean(2)
P=8.1
G=[l.rstrip('\n') for l in open('grid.txt') if l.strip()]
T={'P':100,'B':80,'S':55,'W':95}
fam=lambda c: 'P' if c in '678F' else 'B' if c in '9ABC' else 'W' if c in 'DE' else 'S'
out=np.zeros((64,64))
for y in range(64):
    for x in range(64):
        c=G[y][x]
        if c=='.': continue
        x0=512+(x-32)*P; y0=523-(60-y)*P
        blk=L[int(round(y0)):int(round(y0+P)),int(round(x0)):int(round(x0+P))]
        out[y,x]=(blk<T[fam(c)]).mean() if blk.size else 0
np.save('lijn.npy',out)
