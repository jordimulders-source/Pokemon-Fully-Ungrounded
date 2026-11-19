# r1.npy -> picapau.png (indexed, index 0 transparant) + normal.pal
import numpy as np; from PIL import Image
o=np.load('r4.npy')
PAL=[(152,208,160),(24,20,16),(250,236,150),(238,206,86),(210,164,52),(232,82,58),(178,42,34),(200,130,72),(186,96,44),(123,41,8),
     (150,140,116),(64,64,72),(156,82,0),(98,49,8),(240,232,184),(255,255,255)]
MAP={16:15,17:13}; idx=np.vectorize(lambda v:MAP.get(v,v))(o)
ys,xs=np.where(idx>0); h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
full=np.zeros((64,64),'uint8'); x0=(64-w)//2; y0=63-h   # onderaan (1 rij marge), horizontaal gecentreerd
full[y0:y0+h,x0:x0+w]=idx[ys.min():ys.max()+1,xs.min():xs.max()+1]
p=Image.fromarray(full,'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('picapau.png',transparency=0)
with open('normal.pal','w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
used=sorted(set(full.ravel())); print('formaat',w,h,'px',(full>0).sum(),'kleuren gebruikt',len(used),used)
