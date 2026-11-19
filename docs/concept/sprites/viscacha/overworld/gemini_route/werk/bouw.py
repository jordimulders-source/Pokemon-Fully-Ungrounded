# Bouwt overworld.png (192x32, 6 frames) + palet + controlevellen uit voor/achter/opzij.txt
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'.'); from pal import P
AF='../af/'
def load(f): return [l.rstrip('\n') for l in open(f) if l.strip()]
def place(g, cx2, bottom=29):
    # cx2 = 2*middenx van het frame (31 -> midden 15.5)
    fr=[['.']*32 for _ in range(32)]; h=len(g); w=len(g[0])
    x0=(cx2-(w-1))//2; y0=bottom-h+1
    for y,r in enumerate(g):
        for x,c in enumerate(r): fr[y0+y][x0+x]=c
    return fr
def lift(fr, x0, x1):
    """voeten tussen x0..x1 (framecoord.) 1 px optillen: onderste rij weg, rij erboven wordt omlijning"""
    ys=[y for y in range(32) if any(fr[y][x]!='.' for x in range(x0,x1+1))]; yb=max(ys)
    for x in range(x0,x1+1):
        if fr[yb][x]!='.':
            fr[yb][x]='.'
            if fr[yb-1][x]!='.': fr[yb-1][x]='o'
    return fr
def shift(fr, y0,y1,x0,x1,dx):
    import copy; old=copy.deepcopy(fr)
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): fr[y][x]='.'
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if old[y][x]!='.': fr[y][x+dx]=old[y][x]
    return fr
import copy
def boven(g):
    g=[list(r) for r in g]; h=len(g)
    for y in range(h):
        for x in range(len(g[0])):
            if g[y][x]=='o' and (y==0 or g[y-1][x]=='.') and y < h-3:
                g[y][x]='B'
    return [''.join(r) for r in g]
V=boven(load('voor.txt')); A=boven(load('achter.txt')); O=boven(load('opzij.txt'))
f0=place(V,31); f2=place(A,31); f4=place(O,31)
f1=lift(copy.deepcopy(f0), 0, 15)
f3=lift(copy.deepcopy(f2), 0, 15)
f5=copy.deepcopy(f4)
exec(open('loop_opzij.py').read()) if __import__('os').path.exists('loop_opzij.py') else None
frames=[f0,f1,f2,f3,f4,f5]
idx={k:v[0] for k,v in P.items()}
used=sorted({idx[c] for f in frames for r in f for c in r})
arr=np.zeros((32,192),'uint8')
for i,f in enumerate(frames):
    for y in range(32):
        for x in range(32): arr[y,i*32+x]=idx[f[y][x]]
pal=[(0,0,0)]*16
for k,(i,rgb) in P.items(): pal[i]=rgb
im=Image.fromarray(arr,'P'); im.putpalette([v for c in pal for v in c]); im.info['transparency']=0
im.save(AF+'overworld.png',transparency=0)
open(AF+'overworld_normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in pal))
rgba=im.convert('RGBA'); rgb=Image.new('RGBA',rgba.size,pal[0]+(255,)); rgb.alpha_composite(rgba); rgb=rgb.convert('RGB')
rgb.resize((192*8,32*8),Image.NEAREST).save(AF+'overworld_8x.png')
# gif: per aanzicht stil/lopen naast elkaar
gif=[]
for t in range(4):
    seq=[0,1,1,0][t]
    fr=Image.new('RGB',(96*4,32*4),pal[0])
    for k,b in enumerate((0,2,4)):
        fr.paste(rgb.crop(((b+seq)*32,0,(b+seq)*32+32,32)).resize((128,128),Image.NEAREST),(k*128,0))
    gif.append(fr)
gif[0].save(AF+'loop.gif',save_all=True,append_images=gif[1:],duration=100,loop=0)
print('kleuren (zonder transparant):',len(used)-1, used)
