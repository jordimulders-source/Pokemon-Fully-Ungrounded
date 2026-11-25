import sys, random
from PIL import Image
src=Image.open(sys.argv[1]).convert('RGB')
# crop to content
bg=(255,255,255)
px=src.load(); W,H=src.size
xs=[x for x in range(W) for y in range(0,H,4) if sum(px[x,y])<700]; ys=[y for y in range(H) for x in range(0,W,4) if sum(px[x,y])<700]
box=(min(xs),min(ys),max(xs)+1,max(ys)+1)
c=src.crop(box); s=max(c.size)
sq=Image.new('RGB',(s,s),bg); sq.paste(c,((s-c.size[0])//2,(s-c.size[1])//2))
base=sq.resize((56,56),Image.NEAREST)
spr=Image.new('RGB',(64,64),bg); spr.paste(base,(4,4))
spr=spr.quantize(colors=12).convert('RGB')
def tiles(im): return {(tx,ty):im.crop((tx*8,ty*8,tx*8+8,ty*8+8)) for tx in range(8) for ty in range(8)}
def filled(t): return sum(1 for p in t.getdata() if p!=bg)>10
out=[spr]
for seed in (3,7,11):
    r=random.Random(seed); im=spr.copy(); T=tiles(spr)
    full=[k for k,t in T.items() if filled(t)]
    # 1 swap tiles
    for _ in range(3):
        a,b=r.sample(full,2); im.paste(T[a],(b[0]*8,b[1]*8)); im.paste(T[b],(a[0]*8,a[1]*8))
    # 2 mirror a tile
    k=r.choice(full); im.paste(T[k].transpose(Image.FLIP_LEFT_RIGHT),(k[0]*8,k[1]*8))
    # 3 shift a band of rows
    y0=r.choice([16,24,32,40]); band=im.crop((0,y0,64,y0+8)); im.paste(bg,(0,y0,64,y0+8)); im.paste(band,(r.choice([-8,8,6,-6]),y0))
    # 4 garbage tiles: tile data with wrong palette (rotate colors)
    for _ in range(2):
        k=r.choice(full); t=T[k].copy().convert('RGB')
        g=Image.eval(t,lambda v:255-v); im.paste(g,(k[0]*8,k[1]*8))
    # 5 repeated tile row stray
    k=r.choice(full); im.paste(T[k],(min(56,k[0]*8+8),max(0,k[1]*8-8)))
    out.append(im)
sheet=Image.new('RGB',(64*len(out)+8*(len(out)+1),80),(230,230,230))
for i,im in enumerate(out): sheet.paste(im,(8+i*72,8))
sheet.resize((sheet.size[0]*4,sheet.size[1]*4),Image.NEAREST).save(sys.argv[2])
