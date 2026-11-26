# Natief raster terughalen: periode 10,24 px, fase 9,25 (meet.py). Per cel de mediaan van de binnenste 6x6 modelpixels.
# Lucht = bijna-wit dat met de rand verbonden is. Niets getekend.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/gemini_gekozen_v2.png').convert('RGB')).astype(int)
P=10.24; PH=9.25-P   # eerste cel begint bij -0,99
n=int((1024-PH)/P)
xs=PH+np.arange(n+1)*P
N=np.zeros((n,n,3),int)
for j in range(n):
    for i in range(n):
        y0,x0=int(round(xs[j]+2)),int(round(xs[i]+2))
        blk=a[max(0,y0):max(0,y0)+6,max(0,x0):max(0,x0)+6].reshape(-1,3)
        if len(blk)==0: N[j,i]=255; continue
        N[j,i]=np.median(blk,0)
L=(N*[299,587,114]).sum(2)/1000; sat=N.max(2)-N.min(2)
light=(L>=232)&(sat<25)
air=np.zeros(L.shape,bool); st=[(0,0)]
while st:
    j,i=st.pop()
    if j<0 or i<0 or j>=n or i>=n or air[j,i] or not light[j,i]: continue
    air[j,i]=True; st+=[(j+1,i),(j-1,i),(j,i+1),(j,i-1)]
yy,xx=np.where(~air); y0,y1,x0,x1=yy.min(),yy.max(),xx.min(),xx.max()
N=N[y0:y1+1,x0:x1+1]; air=air[y0:y1+1,x0:x1+1]
print('natief beest',N.shape[1],'x',N.shape[0],'cellen', (~air).sum())
np.savez('natief.npz',N=N,air=air,org=(x0,y0),xs=xs)
im=N.astype('uint8').copy(); im[air]=(152,208,160)
Image.fromarray(im).save('natief.png'); Image.fromarray(im).resize((N.shape[1]*8,N.shape[0]*8),Image.NEAREST).save('natief_8x.png')
