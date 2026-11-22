# klassenraster -> png in modelkleuren (schaal arg)
import numpy as np, sys; from PIL import Image
NAMEN=['_','O','D1','D2','D3','D4','D5','D6','K1','K2','K3','W','R']
C={'_':(235,235,235),'O':(0,0,0),'D1':(30,32,48),'D2':(48,52,72),'D3':(72,76,100),'D4':(90,94,122),'D5':(114,120,150),'D6':(150,156,184),'K1':(240,155,168),'K2':(200,108,122),'K3':(127,56,69),'W':(255,255,255),'R':(150,20,30)}
o=np.load(sys.argv[1]); z=int(sys.argv[3]) if len(sys.argv)>3 else 8
ys,xs=np.where(o>0); o=o[max(ys.min()-1,0):ys.max()+2,max(xs.min()-1,0):xs.max()+2]
a=np.zeros(o.shape+(3,),'uint8')
for i,n in enumerate(NAMEN): a[o==i]=C[n]
Image.fromarray(a).resize((a.shape[1]*z,a.shape[0]*z),Image.NEAREST).save(sys.argv[2])
