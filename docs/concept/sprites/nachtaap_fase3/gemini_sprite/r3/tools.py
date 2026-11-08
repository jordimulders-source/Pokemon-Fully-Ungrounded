import numpy as np, sys, os
from PIL import Image, ImageDraw, ImageFont
H=os.path.dirname(os.path.abspath(__file__)); G=os.path.dirname(H)
P=[(0,0,0),(24,16,40),(140,148,200),(116,122,178),(80,84,138),(56,52,96),(48,40,64),(214,162,190),(144,98,130),
 (240,246,250),(92,206,210),(184,192,224),(154,162,194),(110,116,150),(170,234,236),(44,138,150)]
CH='.123456789abcdef'
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
def load(fn):
    return np.array([[CH.index(c) for c in l.rstrip('\n')] for l in open(fn) if l.strip('\n')][:64])
def save_txt(a,fn):
    open(fn,'w').write('\n'.join(''.join(CH[v] for v in r) for r in a)+'\n')
def rgb(a,bg=(255,255,255),pal=P):
    o=np.zeros(a.shape+(3,),np.uint8); o[:]=bg
    for k in range(1,16): o[a==k]=pal[k]
    return Image.fromarray(o)
def png(a,fn,pal=P):
    im=Image.fromarray(a.astype(np.uint8),'P'); flat=[c for p in pal for c in p]
    im.putpalette(flat+[0]*(768-len(flat))); im.save(fn,transparency=0); return im
def cmp(a,x0,y0,x1,y1,fn,s=16):
    g=Image.open(os.path.join(G,'grid128.png'))
    w,h=x1-x0,y1-y0
    L=g.crop((2*x0,2*y0,2*x1,2*y1)).resize((w*s,h*s),Image.NEAREST)
    R=rgb(a[y0:y1,x0:x1],(255,255,255)).resize((w*s,h*s),Image.NEAREST)
    v=Image.new('RGB',(2*w*s+30,h*s+20),'white'); v.paste(L,(20,20)); v.paste(R,(w*s+30,20)); d=ImageDraw.Draw(v)
    for k in range(w+1):
        for X in (20,w*s+30): d.line([(X+k*s,20),(X+k*s,20+h*s)],fill=(255,0,0) if (x0+k)%5==0 else (200,200,200))
        if k<w and (x0+k)%2==0: d.text((w*s+30+k*s+2,4),str(x0+k),font=F,fill='black')
    for k in range(h+1):
        for X in (20,w*s+30): d.line([(X,20+k*s),(X+w*s,20+k*s)],fill=(255,0,0) if (y0+k)%5==0 else (200,200,200))
        if k<h: d.text((2,20+k*s+3),str(y0+k),font=F,fill='black')
    v.save(fn)
if __name__=='__main__':
    a=load(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); cmp(a,x0,y0,x1,y1,sys.argv[6])
