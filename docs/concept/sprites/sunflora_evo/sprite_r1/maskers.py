# Kop- en lijfmasker op het natieve raster (zelfde logica als gemini/gereedschap/kop_schaal.py)
import numpy as np; from PIL import Image; from scipy import ndimage
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
nw=a.sum(2)<700
g=(a[:,:,1]>a[:,:,0]+15)&(a[:,:,1]>a[:,:,2])
head=nw&~g&~((a.sum(2)<150)&ndimage.binary_dilation(g,iterations=1)); head[86:]=False
lab,n=ndimage.label(head); head=lab==(np.argmax(ndimage.sum(head,lab,range(1,n+1)))+1)
head=ndimage.binary_fill_holes(head)
np.save('kopmasker.npy',head)
ys,xs=np.where(head); print('kop natief x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'b',xs.max()-xs.min()+1,'h',ys.max()-ys.min()+1)
c=a.copy(); c[~head]=255; Image.fromarray(c.astype('uint8')).resize((c.shape[1]*4,c.shape[0]*4),Image.NEAREST).save('kop_natief_4x.png')
