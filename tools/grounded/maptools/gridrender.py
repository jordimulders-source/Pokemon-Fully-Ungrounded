import struct,os,re
from PIL import Image
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))+'/'
def load2(dirn):
    tiles=open(dirn+'/tiles.4bpp','rb').read(); mts=open(dirn+'/metatiles.bin','rb').read()
    pals=[]
    for i in range(16):
        f=f'{dirn}/palettes/{i:02}.pal'
        if not os.path.exists(f): pals.append([(0,0,0)]*16); continue
        lines=open(f).read().split('\n')[3:19]; pals.append([tuple(map(int,l.split())) for l in lines])
    return tiles,mts,pals
def render(grid, prim='general', sec='cave', scale=1):
    pt,pm,ppal=load2(R+'data/tilesets/primary/'+prim)
    st,sm,spal=load2(R+'data/tilesets/secondary/'+sec)
    pal=ppal[:6]+spal[6:13]
    H=len(grid); W=len(grid[0])
    img=Image.new('RGB',(W*16,H*16)); px=img.load()
    def tilepix(idx):
        data,i=(pt,idx) if idx<512 else (st,idx-512)
        b=data[i*32:(i+1)*32]
        if len(b)<32: return [[0]*8 for _ in range(8)]
        return [[(b[y*4+x//2]>>(4*(x&1)))&15 for x in range(8)] for y in range(8)]
    for my in range(H):
        for mx in range(W):
            m=grid[my][mx]&0x3ff
            src,mi=(pm,m) if m<512 else (sm,m-512)
            ent=struct.unpack_from('<8H',src,mi*16)
            for layer in range(2):
                for k in range(4):
                    e=ent[layer*4+k]; t=e&0x3FF; hf=(e>>10)&1; vf=(e>>11)&1; pn=(e>>12)&15
                    tp=tilepix(t); ox=mx*16+(k%2)*8; oy=my*16+(k//2)*8
                    for y in range(8):
                        for x in range(8):
                            c=tp[7-y if vf else y][7-x if hf else x]
                            if c==0 and layer==1: continue
                            col=pal[pn][c] if pn<len(pal) else (255,0,255)
                            px[ox+x,oy+y]=col
    if scale!=1: img=img.resize((W*16*scale,H*16*scale),Image.NEAREST)
    return img
