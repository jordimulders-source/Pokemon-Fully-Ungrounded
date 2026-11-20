# grid.py uit.png y0 y1 x0 x1 S  bestand(en): toont gemiddelde kleur + gegeven rasters met coordinaten
import numpy as np, sys; from PIL import Image, ImageDraw
out=sys.argv[1]; y0,y1,x0,x1,S=map(int,sys.argv[2:7]); C=np.load('pal18.npy'); avg=np.load('avg.npy'); cov=np.load('cov.npy')
def rgbof(f):
    if f=='avg': return np.where((cov>=.5)[:,:,None],avg.clip(0,255),232).astype('uint8')
    if f.endswith('.png'):
        im=np.asarray(Image.open(f).convert('RGBA')); r=im[3:64,13:51]; return np.where(r[:,:,3:]>0,r[:,:,:3],232).astype('uint8')
    i=np.load(f); rgb=np.full(i.shape+(3,),232,'uint8'); m=i>0; rgb[m]=C[i[m]-1].astype('uint8'); return rgb
ims=[rgbof(f)[y0:y1,x0:x1] for f in sys.argv[7:]]
h,w=y1-y0,x1-x0; V=Image.new('RGB',(len(ims)*(w*S+20)+20,h*S+20),(255,255,255)); d=ImageDraw.Draw(V)
for k,r in enumerate(ims):
    ox=20+k*(w*S+20); V.paste(Image.fromarray(r).resize((w*S,h*S),Image.NEAREST),(ox,20))
    for x in range(w+1): d.line([(ox+x*S,20),(ox+x*S,20+h*S)],fill=(200,120,120) if (x+x0)%5==0 else (215,215,215))
    for y in range(h+1): d.line([(ox,20+y*S),(ox+w*S,20+y*S)],fill=(200,120,120) if (y+y0)%5==0 else (215,215,215))
    for x in range(0,w,5): d.text((ox+x*S+2,4),str(x+x0) if (x+x0)%5==0 else '',fill=(0,0,0))
    if k==0:
        for y in range(h):
            if (y+y0)%5==0: d.text((2,20+y*S+2),str(y+y0),fill=(0,0,0))
V.save(out)
