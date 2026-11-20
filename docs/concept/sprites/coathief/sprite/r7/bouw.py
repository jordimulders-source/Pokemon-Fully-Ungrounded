# Tekstraster (hex-index per pixel, 0 = transparant) + palet.txt -> coathief_r1.png (geindexeerd) en 8x-weergave.
import sys, os; from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
src=sys.argv[1] if len(sys.argv)>1 else 'r1.txt'
out=sys.argv[2] if len(sys.argv)>2 else 'coathief_r1.png'
pal=[]
for l in open(os.path.join(D,'palet.txt')):
  if l.startswith('#') or not l.strip(): continue
  i,r,g,b=l.split()[:4]; pal+= [int(r),int(g),int(b)]
pal+=[0]*(48-len(pal))
rows=[l.rstrip('\n') for l in open(os.path.join(D,src)) if l.strip()]
assert len(rows)==64 and all(len(r)==64 for r in rows), 'raster moet 64x64 zijn'
im=Image.new('P',(64,64)); im.putpalette(pal)
im.putdata([int(c,16) for r in rows for c in r])
p=os.path.join(D,out); im.save(p,transparency=0)
im2=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(im2)
bg.resize((512,512),Image.NEAREST).save(p.replace('.png','_8x.png'))
print('kleuren gebruikt:',len(set(im.getdata())),'(incl. transparant)')
