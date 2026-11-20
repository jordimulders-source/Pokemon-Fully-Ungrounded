import numpy as np, sys; from PIL import Image
C=np.load('pal18.npy'); avg=np.load('avg.npy'); cov=np.load('cov.npy')
def im18(i):
    rgb=np.full(i.shape+(3,),232,'uint8'); m=i>0; rgb[m]=C[i[m]-1].astype('uint8'); return rgb
ims=[np.where((cov>=.5)[:,:,None],avg.clip(0,255),232).astype('uint8')]+[im18(np.load(f)) for f in sys.argv[2:]]
S=8; W=sum(x.shape[1]*S+8 for x in ims)
V=Image.new('RGB',(W,61*S),(255,255,255)); x=0
for r in ims: V.paste(Image.fromarray(r).resize((r.shape[1]*S,r.shape[0]*S),Image.NEAREST),(x,0)); x+=r.shape[1]*S+8
V.save(sys.argv[1])
