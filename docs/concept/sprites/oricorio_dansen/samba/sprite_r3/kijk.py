# snel: huidig resultaat van bouw.py naast r1 op 8x (wit). python3 kijk.py out.png
import sys
exec(open('bouw.py').read())
def rgbof(a):
    p=np.array(PAL).reshape(16,3); r=p[a].astype('uint8'); r[a==0]=255; return r
im=np.concatenate([rgbof(o),np.full((64,4,3),255,'uint8'),rgbof(R1)],1)
Image.fromarray(im).resize((im.shape[1]*8,512),Image.NEAREST).save(sys.argv[1]); print(LOG)
