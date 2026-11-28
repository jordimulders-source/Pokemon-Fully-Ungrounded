"""raster.txt -> icon.png (pal3) + 8x-vel naast de front en echte iconen + gif.
python3 bouw.py raster.txt uitmap"""
import sys,os
from PIL import Image,ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
def pal(p): L=open(p).read().split('\n'); return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(16)]
P=pal(R+'graphics/pokemon/icon_palettes/pal3.pal')
rows=[r.rstrip('\n') for r in open(sys.argv[1])][:64]
im=Image.new('P',(32,64),0); im.putpalette([c for t in P for c in t])
for y,r in enumerate(rows):
    for x,ch in enumerate(r[:32]):
        if ch!='.': im.putpixel((x,y),int(ch,16))
o=sys.argv[2]; os.makedirs(o,exist_ok=True); im.save(o+'/icon.png')
def rgba(i):
    a=i.convert('RGBA'); d=[(0,0,0,0) if i.getpixel((x%i.width,x//i.width))==0 else p for x,p in enumerate(a.getdata())]; a.putdata(d); return a
ic=rgba(im); bg=(115,197,164)
fr=Image.open(R+'docs/concept/sprites/poliwag_regional/af/poliwag_regional.png').convert('RGBA')
# 8x: front 4x | frame1 8x | frame2 8x
W=Image.new('RGB',(256*3+40,280),bg); W.paste(fr.resize((256,256),Image.NEAREST),(0,12),fr.resize((256,256),Image.NEAREST))
for k in range(2):
    f=ic.crop((0,32*k,32,32*k+32)).resize((256,256),Image.NEAREST); W.paste(f,(276+k*266,12),f)
W.save(o+'/icon_8x.png')
# 1x/3x tussen echte iconen
buren=[('poliwag',0),('poliwhirl',0),('pikachu',2),('zubat',2),('wooper',0),('umbreon',2)]
V=Image.new('RGB',((len(buren)+1)*40,80),bg)
for n,(s,p) in enumerate(buren):
    b=Image.open(R+f'graphics/pokemon/{s}/icon.png').copy(); b.putpalette([c for t in pal(R+f'graphics/pokemon/icon_palettes/pal{p}.pal') for c in t])
    b=rgba(b).crop((0,0,32,32)); V.paste(b,(n*40+4,4),b)
V.paste(ic.crop((0,0,32,32)),(len(buren)*40+4,4),ic.crop((0,0,32,32)))
V=V.resize((V.width*3,V.height*3),Image.NEAREST); V.save(o+'/buren_3x.png')
fs=[]
for k in range(2):
    f=Image.new('RGB',(32,32),bg); c=ic.crop((0,32*k,32,32*k+32)); f.paste(c,(0,0),c); fs.append(f.resize((128,128),Image.NEAREST))
fs[0].save(o+'/icon_anim.gif',save_all=True,append_images=fs[1:],duration=250,loop=0)
