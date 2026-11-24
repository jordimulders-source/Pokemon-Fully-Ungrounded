# Paneelzones in modelcoordinaten: convex omhulsel van de grote paneelvlakken (klasse 9/10/15, comp > 2000 px, oog uitgesloten)
import numpy as np
from scipy import ndimage as nd
from scipy.spatial import ConvexHull
from PIL import Image, ImageDraw
k=np.load('klassen.npy')
m=np.isin(k,[9,10,15]); lab,n=nd.label(m); sz=nd.sum(m,lab,range(1,n+1)); cm=nd.center_of_mass(m,lab,range(1,n+1))
yy,xx=np.mgrid[0:1024,0:1024]; Z=np.zeros((1024,1024),np.uint8)
for zid,cond in ((1,lambda c:c[1]<330),(2,lambda c:c[1]>420)):
    sel=[i+1 for i in range(n) if sz[i]>2000 and cond(cm[i]) and not (abs(cm[i][0]-495)<60 and abs(cm[i][1]-339)<60)]
    ys,xs=np.where(np.isin(lab,sel)); pts=np.c_[xs,ys]; h=ConvexHull(pts); poly=pts[h.vertices]
    im=Image.new('L',(1024,1024),0); ImageDraw.Draw(im).polygon([tuple(map(int,p)) for p in poly],fill=1,outline=1)
    inside=nd.binary_dilation(np.asarray(im)>0,iterations=6)   # met de lichte rand erbij
    Z[inside&(Z==0)]=zid; print(zid,len(sel),poly.tolist())
oog=(xx-345)**2+(yy-492)**2<=112**2
Z[(Z==1)&oog]=0
Image.fromarray(Z).save('zones.png')  # zones.py gebruikt de eerste klassen.npy (klassen.py zonder zone-uitsluiting); bewaard als png
from PIL import Image
a=np.asarray(Image.open('../model.png').convert('RGB')).astype(float)
a[Z==1]=a[Z==1]*0.6+np.array([255,0,0])*0.4; a[Z==2]=a[Z==2]*0.6+np.array([0,200,0])*0.4
Image.fromarray(a.astype('uint8')).resize((512,512)).save('zones_check.png')
