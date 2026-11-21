# naast.py raster.txt out.png y0 y1 [x0 x1] : sprite-uitsnede (12x, met coordinaten) | model op dezelfde schaal met sprite-raster erover
import sys; from PIL import Image, ImageDraw
exec(open('png.py').read().split('L={c')[0].split('PAL=',1)[0]) if False else None
src=open('png.py').read(); PAL=eval(src[src.index('PAL=')+4:src.index('\nL={')])
C=dict(PAL); C['.']=(255,255,255)
rows=[r.rstrip('\n') for r in open(sys.argv[1]) if r.strip('\n')]
y0,y1=int(sys.argv[3]),int(sys.argv[4]); x0=int(sys.argv[5]) if len(sys.argv)>5 else 0; x1=int(sys.argv[6]) if len(sys.argv)>6 else 38
S=int(sys.argv[7]) if len(sys.argv)>7 else 18; F=0.66
A=Image.new('RGB',((x1-x0)*S,(y1-y0)*S),(255,255,255)); d=ImageDraw.Draw(A)
for y in range(y0,y1):
    for x in range(x0,x1):
        d.rectangle([(x-x0)*S,(y-y0)*S,(x-x0+1)*S-1,(y-y0+1)*S-1],fill=C[rows[y][x]])
for x in range(x0,x1): d.text(((x-x0)*S+2,(0)),str(x%100),fill=(255,0,0)) if x%2==0 else None
for y in range(y0,y1): d.text((1,(y-y0)*S+4),str(y),fill=(255,0,0)) if y%2==0 else None
m=Image.open('../model/model_natief.png').convert('RGB')
mx0=24+x0/F; my0=3+y0/F; mx1=24+x1/F; my1=3+y1/F
mc=m.crop((int(mx0),int(my0),int(mx1)+1,int(my1)+1)); s=S*F
mc=mc.resize((int(mc.size[0]*s),int(mc.size[1]*s)),Image.NEAREST)
ox=(mx0-int(mx0))*s; oy=(my0-int(my0))*s
B=Image.new('RGB',A.size,(255,255,255)); B.paste(mc,(-int(ox),-int(oy))); d=ImageDraw.Draw(B)
for x in range(x0,x1+1): d.line([((x-x0)*S,0),((x-x0)*S,A.size[1])],fill=(255,150,150))
for y in range(y0,y1+1): d.line([(0,(y-y0)*S),(A.size[0],(y-y0)*S)],fill=(255,150,150))
if len(sys.argv)>8:
    A.save(sys.argv[2].replace('.png','_s.png')); B.save(sys.argv[2].replace('.png','_m.png'))
else:
    V=Image.new('RGB',(A.size[0]*2+12,A.size[1]),(255,255,255)); V.paste(A,(0,0)); V.paste(B,(A.size[0]+12,0)); V.save(sys.argv[2])
