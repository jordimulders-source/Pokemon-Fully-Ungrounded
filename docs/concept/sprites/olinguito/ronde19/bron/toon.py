"""Toont een tekstraster (tekens .123456789abcdef = paletindex) vergroot. Gebruik: toon.py in.txt uit.png schaal"""
import sys
from PIL import Image
S='.123456789abcdef'
pal=[]
for r in open(__file__.replace('toon.py','palet.txt')):
    p=r.split('#')[0].split()
    if p: pal.append(tuple(int(v) for v in p[1:4]))
rows=[l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]
k=int(sys.argv[3]); w=max(map(len,rows))
im=Image.new('RGB',(w*k,len(rows)*k),(255,255,255))
for y,l in enumerate(rows):
    for x,c in enumerate(l):
        if c!='.':
            im.paste(pal[S.index(c)],(x*k,y*k,x*k+k,y*k+k))
im.save(sys.argv[2])
