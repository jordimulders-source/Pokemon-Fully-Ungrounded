"""Rendert echte stukken kaart (metatiles met juiste paletten) uit data/maps, zodat brokken
herkenbare game-assets zijn (huis, boom, bord, water). Naar tools/grounded/maptools/render_map.py,
maar zonder gebouwde .4bpp (tegels direct uit tiles.png)."""
import json, struct, os, re, random, glob
from PIL import Image
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../../..'))
def _b4(png):
    im=Image.open(png); w,h=im.size; px=im.load(); out=bytearray()
    for ty in range(h//8):
        for tx in range(w//8):
            for y in range(8):
                for x in range(0,8,2): out.append((px[tx*8+x,ty*8+y]&0xF)|((px[tx*8+x+1,ty*8+y]&0xF)<<4))
    return bytes(out)
def _tsname(sym): return re.sub(r'(?<!^)(?=[A-Z])','_',sym.replace('gTileset_','')).lower()
_cache={}
def _load(dirn):
    if dirn in _cache: return _cache[dirn]
    base=dirn
    if os.path.exists(dirn+'/BASE'): base=os.path.join(os.path.dirname(dirn),open(dirn+'/BASE').read().strip())
    tdir=base
    if os.path.exists(dirn+'/TILES'): tdir=os.path.join(os.path.dirname(dirn),open(dirn+'/TILES').read().strip())
    tiles=_b4(tdir+'/tiles.png'); mts=open(base+'/metatiles.bin','rb').read(); pals=[]
    for i in range(16):
        f=f'{dirn}/palettes/{i:02}.pal'
        if not os.path.exists(f): pals.append([(0,0,0)]*16); continue
        pals.append([tuple(map(int,l.split())) for l in open(f).read().split('\n')[3:19]])
    _cache[dirn]=(tiles,mts,pals); return _cache[dirn]
LAYOUTS=json.load(open(os.path.join(REPO,'data/layouts/layouts.json')))['layouts']
LAYOUTS=[l for l in LAYOUTS if l.get('blockdata_filepath') and os.path.exists(os.path.join(REPO,l['blockdata_filepath']))]
def brok(r,mw=2,mh=2,transparant_l0=False):
    """Willekeurig stuk kaart van mw x mh metatiles (16 px per stuk), RGBA."""
    for _ in range(30):
        L=r.choice(LAYOUTS)
        try:
            pt,pm,pp=_load(os.path.join(REPO,'data/tilesets/primary/'+_tsname(L['primary_tileset'])))
            st,sm,sp=_load(os.path.join(REPO,'data/tilesets/secondary/'+_tsname(L['secondary_tileset'])))
        except Exception: continue
        w,h=L['width'],L['height']
        if w<mw or h<mh: continue
        v=struct.unpack(f'<{w*h}H',open(os.path.join(REPO,L['blockdata_filepath']),'rb').read())
        pal=pp[:6]+sp[6:13]
        x0,y0=r.randrange(0,w-mw+1),r.randrange(0,h-mh+1)
        img=Image.new('RGBA',(mw*16,mh*16),(0,0,0,0)); px=img.load()
        for my in range(mh):
            for mx in range(mw):
                m=v[(y0+my)*w+x0+mx]&0x3FF; src=pm if m<512 else sm; mi=m if m<512 else m-512
                if mi*16+16>len(src): continue
                ent=struct.unpack_from('<8H',src,mi*16)
                for layer in range(2):
                    for k in range(4):
                        e=ent[layer*4+k]; t=e&0x3FF; hf=(e>>10)&1; vf=(e>>11)&1; pn=(e>>12)&15
                        data,i=(pt,t) if t<512 else (st,t-512); b=data[i*32:i*32+32]
                        if len(b)<32: continue
                        for y in range(8):
                            for x in range(8):
                                yy,xx=(7-y if vf else y),(7-x if hf else x)
                                c=(b[yy*4+xx//2]>>(4*(xx&1)))&15
                                if c==0 and (layer==1 or transparant_l0): continue
                                col=pal[pn][c] if pn<len(pal) else (255,0,255)
                                px[mx*16+(k%2)*8+x,my*16+(k//2)*8+y]=col+(255,)
        if sum(1 for p in img.getdata() if p[3])>0: return img
    return Image.new('RGBA',(mw*16,mh*16),(0,0,0,0))
