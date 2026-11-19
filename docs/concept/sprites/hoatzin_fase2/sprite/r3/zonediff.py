import numpy as np; from PIL import Image
S=np.load('stapS.npy'); A=np.load('stapA.npy'); Z=np.load('zone_t.npy')
im=np.asarray(Image.open('hoatzin.png')); O=np.asarray(Image.open('onderlaag.png'))[...,3]>0
print('silhouet-diff t.o.v. onderlaag:',int(((im>0)!=O).sum()))
for z,n in [('M','lijf/vleugel'),('W','vleugelstrepen'),('C','kuif'),('F','gezicht'),('E','oog'),('S','snavel'),('P','buik'),('T','poten'),('D','staart'),('K','modellijn'),('.','buiten silhouet')]:
    m=Z==z; print(z,n,int(m.sum()),int((S!=A)[m].sum()))
print('totaal',int((S!=A).sum()))
