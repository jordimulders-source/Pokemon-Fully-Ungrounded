import sys
from PIL import Image
HERE=sys.argv[1]
SIL=[l.strip() for l in open(sys.argv[2]) if l.strip()]
PAL={'.':(152,208,160),'k':(28,18,14),'d':(62,38,26),'b':(96,62,40),'l':(128,86,56),
 'c':(138,92,56),'g':(118,104,90),'h':(150,136,120),'s':(84,72,62),'m':(50,44,44),
 'r':(110,34,26),'i':(168,70,48),'w':(240,234,220),'n':(168,158,140),'p':(196,132,128),'q':(140,82,82)}
ORDER='.kdblcghsmriwnpq'
g=[['.']*64 for _ in range(64)]
for line in open(HERE+'/raster.txt'):
    line=line.split('#')[0].strip()
    if not line: continue
    y,x,s=line.split(); y=int(y); x=int(x)
    for i,ch in enumerate(s):
        g[y][x+i]=ch
err=[(x,y) for y in range(64) for x in range(64) if (g[y][x]!='.')!=(SIL[y][x]=='#')]
print('afwijkingen t.o.v. silhouet:',len(err), err[:40])
im=Image.new('P',(64,64)); flat=[]
for ch in ORDER: flat+=PAL[ch]
im.putpalette(flat+[0]*(768-len(flat)))
im.putdata([ORDER.index(g[y][x]) for y in range(64) for x in range(64)])
im.save(sys.argv[3],transparency=0)
open(HERE+'/raster_grid.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
