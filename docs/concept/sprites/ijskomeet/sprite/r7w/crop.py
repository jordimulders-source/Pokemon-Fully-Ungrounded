# crop.py y0 y1 x0 x1 out  files...  (txt-bestanden met p6-palet of gio-palet; model eerst)
import sys; sys.path.insert(0,'r7w'); sys.path.insert(0,'.'); sys.path.insert(0,'r6w')
from proj import *; from PIL import ImageDraw
import p6, gio
y0,y1,x0,x1=map(int,sys.argv[1:5]); out=sys.argv[5]; fs=sys.argv[6:]
s=12; W=(x1-x0)*s; H=(y1-y0)*s
def grid(im):
    d=ImageDraw.Draw(im)
    for k in range(x0,x1+1):
        c=(255,0,0) if k%5==0 else (190,190,190); d.line([(k-x0)*s,0,(k-x0)*s,H],fill=c) if k%5==0 else None
    for k in range(y0,y1+1):
        if k%5==0: d.line([0,(k-y0)*s,W,(k-y0)*s],fill=(255,0,0))
    return im
ims=[grid(model_s(s).crop((x0*s,y0*s,x1*s,y1*s)).convert('RGB'))]
R5PAL=[(16,20,48),(238,248,250),(192,220,234),(150,186,212),(108,142,176),(72,92,136),(58,54,112),(88,80,150),(112,92,170),(162,134,218),(200,204,238),(102,226,236),(196,255,255),(80,180,204),(178,236,242)]
for f in fs:
    if f.endswith('.npy'): o=np.load(f); ch=p6.CH; pal=p6.PAL
    elif 'r5' in f or f.startswith('g:'): f=f.replace('g:',''); o=gio.from_txt(f); pal=R5PAL
    else: o=p6.from_txt(f); pal=p6.PAL
    a=np.full((64,64,3),255,'uint8')
    for j in range(64):
        for i in range(64):
            if o[j,i]>=0: a[j,i]=pal[o[j,i]]
    ims.append(grid(Image.fromarray(a).crop((x0,y0,x1,y1)).resize((W,H),0)))
V=Image.new('RGB',(len(ims)*(W+8),H),'white')
for k,im in enumerate(ims): V.paste(im,(k*(W+8),0))
V.save(out)
