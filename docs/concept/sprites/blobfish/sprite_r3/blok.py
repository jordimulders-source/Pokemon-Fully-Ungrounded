# blok.py SPRITE.png x,y ... : modelmeting per spritepixel uit zijn 4x4-blok natieve pixels (gem, min, max helderheid,
# mediaankleur van donker (<62) en van de rest) + huidige spritewaarde. Meten, niet tekenen.
import sys,numpy as np; from PIL import Image
sp=sys.argv[1]; OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); L=n@[0.299,0.587,0.114]
s=np.asarray(Image.open(sp)); pal=Image.open(sp).getpalette()
for t in sys.argv[2:]:
    x,y=map(int,t.split(',')); ny=OY+4*(y-y0+ymin); nx=OX+4*(x-x0+xmin)
    b=n[ny:ny+4,nx:nx+4].reshape(-1,3); l=L[ny:ny+4,nx:nx+4].ravel(); d=l<62
    print(f'({x},{y}) sprite {s[y,x]} {pal[3*s[y,x]:3*s[y,x]+3]}  lum gem {l.mean():.0f} min {l.min():.0f} max {l.max():.0f}  donker {d.sum()} {np.median(b[d],0).astype(int).tolist() if d.any() else "-"}  rest {np.median(b[~d],0).astype(int).tolist() if (~d).any() else "-"}')
