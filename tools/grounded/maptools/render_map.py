import json,struct,sys,os
from PIL import Image, ImageDraw
mapname=sys.argv[1]; out=sys.argv[2]
d=json.load(open(f'data/maps/{mapname}/map.json'))
L=[l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l['id']==d['layout']][0]
w,h=L['width'],L['height']; v=struct.unpack(f'<{w*h}H',open(L['blockdata_filepath'],'rb').read())
def tsdir(sym):
    import re
    for f in ['src/data/tilesets/headers.h']:
        s=open(f).read()
    m=re.search(r'const struct Tileset '+sym+r' =\s*\{(.*?)\};',s,re.S)
    t=re.search(r'\.tiles = (\w+)',m.group(1)).group(1)
    return t
import re,glob
graphics=open('src/data/tilesets/graphics.h').read()+open('src/data/tilesets/metatiles.h').read()
def paths(sym):
    hdr=open('src/data/tilesets/headers.h').read()
    body=re.search(r'const struct Tileset '+sym+r' =\s*\{(.*?)\};',hdr,re.S).group(1)
    tiles=re.search(r'\.tiles = (\w+)',body).group(1); mts=re.search(r'\.metatiles = (\w+)',body).group(1)
    pal=re.search(r'\.palettes = (\w+)',body).group(1)
    tp=re.search(tiles+r'\[\] = INCGFX_U32\("([^"]+)"|'+tiles+r'\[\] = INCBIN_U32\("([^"]+)"',graphics)
    tp=[x for x in tp.groups() if x][0]
    mp=re.search(mts+r'\[\] = INCBIN_U16\("([^"]+)"',graphics).group(1)
    pp=re.findall(r'INCBIN_U16\("([^"]+)"\)',re.search(pal+r'\[\]\[16\] =\s*\{(.*?)\};',graphics,re.S).group(1))
    return tp,mp,pp
def load(sym):
    tp,mp,pp=paths(sym)
    tp=tp.replace('.smol','').replace('.fastSmol','').replace('.lz','')
    if not tp.endswith('.4bpp'): tp=os.path.splitext(tp)[0]+'.4bpp'
    tiles=open(tp,'rb').read(); mts=open(mp,'rb').read()
    pals=[]
    for p in pp:
        b=open(p,'rb').read() if os.path.exists(p) else open(p.replace('.gbapal','.pal'),'rb').read()
        if p.endswith('.gbapal') and os.path.exists(p):
            cols=[struct.unpack_from('<H',b,i*2)[0] for i in range(16)]
            pals.append([((c&31)<<3,((c>>5)&31)<<3,((c>>10)&31)<<3) for c in cols])
        else:
            lines=b.decode().split('\n')[3:19]; pals.append([tuple(map(int,l.split())) for l in lines])
    return tiles,mts,pals
def load2(dirn):
    base=dirn  # tileset met alleen eigen paletten (bijv. nightmare_general): BASE noemt de tileset met tiles/metatiles
    if os.path.exists(dirn+'/BASE'): base=os.path.join(os.path.dirname(dirn),open(dirn+'/BASE').read().strip())
    tiles=open(base+'/tiles.4bpp','rb').read(); mts=open(base+'/metatiles.bin','rb').read()
    pals=[]
    for i in range(16):
        f=f'{dirn}/palettes/{i:02}.pal'
        if not os.path.exists(f): pals.append([(0,0,0)]*16); continue
        lines=open(f).read().split('\n')[3:19]; pals.append([tuple(map(int,l.split())) for l in lines])
    return tiles,mts,pals
def tsname(sym):
    return re.sub(r'(?<!^)(?=[A-Z])','_',sym.replace('gTileset_','')).lower()
pt,pm,ppal=load2('data/tilesets/primary/'+tsname(L['primary_tileset']))
st,sm,spal=load2('data/tilesets/secondary/'+tsname(L['secondary_tileset']))
pal=ppal[:6]+spal[6:13]
def tilepix(idx):
    if idx<512: data=pt; i=idx
    else: data=st; i=idx-512
    b=data[i*32:(i+1)*32]
    if len(b)<32: return [[0]*8 for _ in range(8)]
    return [[ (b[y*4+x//2]>>(4*(x&1)))&15 for x in range(8)] for y in range(8)]
img=Image.new('RGB',(w*16,h*16))
px=img.load()
for my in range(h):
    for mx in range(w):
        m=v[my*w+mx]&0x3FF
        src=pm if m<512 else sm; mi=m if m<512 else m-512
        ent=struct.unpack_from('<8H',src,mi*16)
        for layer in range(2):
            for k in range(4):
                e=ent[layer*4+k]; t=e&0x3FF; hf=(e>>10)&1; vf=(e>>11)&1; pn=(e>>12)&15
                tp_=tilepix(t)
                ox=mx*16+(k%2)*8; oy=my*16+(k//2)*8
                for y in range(8):
                    for x in range(8):
                        c=tp_[7-y if vf else y][7-x if hf else x]
                        if c==0 and layer==1: continue
                        if c==0 and layer==0: col=pal[pn][0] if pn<len(pal) else (0,0,0)
                        else: col=pal[pn][c] if pn<len(pal) else (255,0,255)
                        px[ox+x,oy+y]=col
dr=ImageDraw.Draw(img)
for o in d['object_events']:
    dr.rectangle([o['x']*16+3,o['y']*16+3,o['x']*16+12,o['y']*16+12],outline=(255,0,0))
for x in range(0,w,5): dr.text((x*16+2,2),str(x),fill=(255,0,0))
for y in range(0,h,5): dr.text((2,y*16+2),str(y),fill=(255,0,0))
y0,y1=int(sys.argv[3]),int(sys.argv[4])
img.crop((0,y0*16,w*16,y1*16)).save(out)
