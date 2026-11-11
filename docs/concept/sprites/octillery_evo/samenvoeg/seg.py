# Knipt het kanon uit r5 via floodfill binnen de zwarte omlijning. Gebruik: python3 seg.py DREMPEL
import sys; from PIL import Image, ImageFilter; import numpy as np
from collections import deque
T=int(sys.argv[1])
a=np.asarray(Image.open('referenties/gemini_gekozen_r5.png').convert('RGB')).astype(int); H,W=a.shape[:2]
dark=(a.max(axis=2)<T)|(a.min(axis=2)>235)
seen=np.zeros((H,W),bool); q=deque()
for x,y in [(330,410),(400,412),(480,415),(560,418)]:
    if not dark[y,x]: seen[y,x]=True; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=y+dy,x+dx
        if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and not dark[ny,nx] and nx<720:
            seen[ny,nx]=True; q.append((ny,nx))
yy,xx=np.mgrid[0:H,0:W]; seen&=~((xx<520)&(yy<372))
m=Image.fromarray((seen*255).astype('uint8')).filter(ImageFilter.MaxFilter(7))
from PIL import ImageDraw
f=m.point(lambda v:255 if v else 0); ImageDraw.floodfill(f,(0,0),128); m=f.point(lambda v:0 if v==128 else 255)
m.save('samenvoeg/kanon_masker.png')
o=np.full_like(a,255); M=np.asarray(m)>0; o[M]=a[M]
Image.fromarray(o.astype('uint8')).crop((200,300,760,500)).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/edb145cf-71a4-55a5-8012-167050278397/scratchpad/k.png')
print(seen.sum())
