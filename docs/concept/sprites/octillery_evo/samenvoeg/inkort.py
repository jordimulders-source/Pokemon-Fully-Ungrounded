# Kort het bovenste kanon in: monding+knots (x<XC, y<YC) schuift D px langs de steel naar de kop. Gebruik: python3 inkort.py D [XC YC]
import sys; from PIL import Image; import numpy as np
D=float(sys.argv[1]); XC=int(sys.argv[2]) if len(sys.argv)>2 else 300; YC=int(sys.argv[3]) if len(sys.argv)>3 else 362
a=np.asarray(Image.open('samenvoeg/v3.png').convert('RGB')).copy(); H,W=a.shape[:2]
Y,X=np.mgrid[0:H,0:W]; P=(X<XC)&(Y<YC)&(a.min(axis=2)<235)
dx,dy=round(D*0.74),round(D*0.67)
out=a.copy(); out[P]=a[3,3]
ys,xs=np.where(P); out[ys+dy,xs+dx]=a[ys,xs]
Image.fromarray(out).save('samenvoeg/v3_ingekort.png')
g=np.asarray(Image.fromarray(out).convert('L'));yy,xx=np.where(g<200);w=xx.max()-xx.min();h=yy.max()-yy.min();print(w,h,round(w/h,2),'-> 64x',round(64*h/w))
