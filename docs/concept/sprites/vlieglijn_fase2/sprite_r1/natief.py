# Natief raster terughalen: pitch 6.828/6.826, fase uit randsterkte (raster.py); mediaan van de binnenste 3x3 per cel.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/gemini_gekozen_r1.png').convert('RGB')).astype(int)
px,phx,py,phy=6.828,5.7,6.826,5.8
xs=np.arange(phx+1+px/2-px,1024,px); xs=xs[xs>1]; ys=np.arange(phy+1+py/2-py,1024,py); ys=ys[ys>1]
out=np.zeros((len(ys),len(xs),3),'uint8'); var=np.zeros((len(ys),len(xs)))
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        yi,xi=int(round(y-.5)),int(round(x-.5))
        blk=a[max(0,yi-1):yi+2,max(0,xi-1):xi+2].reshape(-1,3)
        out[j,i]=np.median(blk,0); var[j,i]=blk.std(0).sum()
Image.fromarray(out).save('natief.png')
fg=out.min(-1)<235
print(out.shape,'gem. std in figuur',var[fg].mean(),'cellen std>20:',(var[fg]>20).sum(),'/',fg.sum())
yy,xx=np.where(fg); print('bbox',xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1)
