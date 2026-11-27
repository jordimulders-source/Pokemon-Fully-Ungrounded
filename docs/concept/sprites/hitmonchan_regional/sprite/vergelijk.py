# vergelijk.py rN x0 y0 x1 y1 out [Z]: sprite-uitsnede op Zx met coordinaten | model (natief) vervormd met dezelfde stuksgewijze
# afbeelding als de reductie (oogzone 1-op-1), zodat elke spritepixel exact over zijn modelgebied ligt.
from PIL import Image, ImageDraw; import numpy as np, sys, os
D='docs/concept/sprites/hitmonchan_regional/sprite/'
r=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); out=sys.argv[6]; Z=int(sys.argv[7]) if len(sys.argv)>7 else 16
S=np.load(D+f'{r}/idx.npy'); pal=eval(open(D+(f'{r}/pal.txt' if os.path.exists(D+f'{r}/pal.txt') else 'pal.txt')).read())
nat=np.asarray(Image.open(D+'natief.png').convert('RGB'))
def randen(N,a,b,A,uit):
    k1=a/A; B=A+(b-a); k2=(N-b)/(uit-B); return [i*k1 if i<=A else (a+(i-A) if i<=B else b+(i-B)*k2) for i in range(uit+1)]
ry=randen(81,24,32,18,64); cx=randen(50,28,38,21,40)
w,h=(x1-x0)*Z,(y1-y0)*Z
sp=np.zeros((h,w,3),np.uint8); md=np.zeros((h,w,3),np.uint8)
for j in range(h):
    yy=y0+(j+0.5)/Z; iy=int(yy); ny=ry[iy]+(ry[iy+1]-ry[iy])*(yy-iy)
    for i in range(w):
        xx=x0+(i+0.5)/Z; ix=int(xx); nx=cx[ix]+(cx[ix+1]-cx[ix])*(xx-ix)
        v=S[iy,ix]; sp[j,i]=pal[v] if v else (255,255,255)
        md[j,i]=nat[min(int(ny),80),min(int(nx),49)]
v=Image.new('RGB',(2*w+50,h+20),(255,255,255)); v.paste(Image.fromarray(sp),(20,20)); v.paste(Image.fromarray(md),(w+40,20))
d=ImageDraw.Draw(v)
for i in range(x1-x0):
    d.text((20+i*Z+3,4),str((x0+i)%10),fill=(200,0,0))
    for X in (20,w+40): d.line([(X+i*Z,20),(X+i*Z,20+h)],fill=(255,190,190) if (x0+i)%5 else (255,0,0))
for j in range(y1-y0):
    d.text((2,20+j*Z+2),str(y0+j),fill=(200,0,0))
    for X in (20,w+40): d.line([(X,20+j*Z),(X+w,20+j*Z)],fill=(255,190,190) if (y0+j)%5 else (255,0,0))
v.save(out)
