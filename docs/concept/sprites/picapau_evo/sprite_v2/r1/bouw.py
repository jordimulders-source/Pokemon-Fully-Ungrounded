# r1.npy -> picaraio.png (indexed 64x64, index 0 transparant) + normal.pal + picaraio_8x.png. Codes = paletindex.
# Gen 3-palet: modelkleuren met meer contrast (licht linksboven); vorm komt uit het model.
import sys; import numpy as np; from PIL import Image
f=sys.argv[1] if len(sys.argv)>1 else 'r1.npy'
PAL=[(152,208,160),(24,20,16),(226,150,96),(192,110,60),(142,74,42),(250,242,214),(230,210,166),(196,170,124),
     (232,82,74),(204,196,192),(142,132,130),(78,70,70),(252,226,96),(212,170,52),(255,255,255),(98,48,26)]
o=np.load(f); ys,xs=np.where(o>0); h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
full=np.zeros((64,64),'uint8'); x0=(64-w)//2; y0=63-h
full[y0:y0+h,x0:x0+w]=o[ys.min():ys.max()+1,xs.min():xs.max()+1]
p=Image.fromarray(full,'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('picaraio.png',transparency=0)
with open('normal.pal','w') as fh: fh.write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
rgb=np.array(PAL,'uint8')[full]; rgb[full==0]=(255,255,255)
Image.fromarray(rgb).resize((512,512),0).save('picaraio_8x.png')
print('formaat',w,h,'offset',x0-xs.min(),y0-ys.min(),'px',(full>0).sum(),'kleuren',len(set(full.ravel())))
