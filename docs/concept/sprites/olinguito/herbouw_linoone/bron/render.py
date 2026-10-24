"""Raster (64 regels x 64 tekens, palette-index als hex, '.' = transparant) -> PNG/zoom."""
import sys
from PIL import Image
D='/home/user/projectgrounded/docs/concept/sprites/olinguito/'
def pal():
    L=open(D+'ronde23/normal.pal').read().split('\n')[3:19]
    return [tuple(map(int,l.split())) for l in L]
def load(p):
    rows=[l.rstrip('\n') for l in open(p)]
    return rows
def to_img(rows,shift=(0,0)):
    im=Image.new('P',(64,64),0); P=pal(); flat=[c for t in P for c in t]; im.putpalette(flat)
    px=im.load()
    for y,r in enumerate(rows[:64]):
        for x,ch in enumerate(r[:64]):
            if ch!='.':
                X,Y=x+shift[0],y+shift[1]
                if 0<=X<64 and 0<=Y<64: px[X,Y]=int(ch,16)
    return im
def zoom(im,z,bg=(200,200,220)):
    r=im.convert('RGBA'); a=Image.new('RGBA',r.size,bg+(255,))
    pxi=im.load(); pr=r.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if pxi[x,y]!=0: a.putpixel((x,y),pr[x,y])
    return a.resize((im.size[0]*z,im.size[1]*z),Image.NEAREST)
if __name__=='__main__':
    rows=load(sys.argv[1]); im=to_img(rows)
    z=zoom(im,8); z.crop((0,int(sys.argv[3]) if len(sys.argv)>3 else 120, 512, 460)).save(sys.argv[2])
    print('px',sum(1 for x in range(64) for y in range(64) if im.getpixel((x,y))))
