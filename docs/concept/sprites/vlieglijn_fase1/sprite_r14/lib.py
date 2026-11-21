from PIL import Image, ImageDraw
SP='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/9fdf7d25-33f6-53eb-9518-4a6a1261da60/scratchpad/'
def rgba(im):
    im.save(SP+'_t.png',transparency=0)
    return Image.open(SP+'_t.png').convert('RGBA')
def onbg(im,col=(255,255,255)):
    a=rgba(im); bg=Image.new('RGBA',a.size,col+(255,)); bg.alpha_composite(a); return bg.convert('RGB')
def zoom(im,box,S=16,grid=True):
    x0,y0,x1,y1=box
    c=onbg(im).crop(box).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
    if grid:
        d=ImageDraw.Draw(c)
        for x in range(x0,x1):
            if x%2==0: d.text(((x-x0)*S+2,(y1-y0)*S-12),str(x),fill=(255,0,0))
        for y in range(y0,y1): d.text((2,(y-y0)*S+2),str(y),fill=(255,0,0))
    return c
def dump(im,xs,ys):
    s='0123456789ABCDEF';px=im.load()
    print('    '+' '.join('%2d'%x for x in xs))
    for y in ys: print('%2d  '%y+' '.join(' '+('.' if px[x,y]==0 else s[px[x,y]]) for x in xs))
