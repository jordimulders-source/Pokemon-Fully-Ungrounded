# Klasse per natieve modelpixel = dichtstbijzijnde modelkleur (gemeten uit het model per zone). -> klassen.npy
from PIL import Image; import numpy as np
b=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
# code: (naam, groep, modelkleur)
M={0:('bg','bg',(255,255,255)),1:('zwart','z',(14,10,8)),
 2:('bruin licht','b',(205,134,91)),3:('bruin mid','b',(191,110,63)),4:('bruin donker','b',(138,73,46)),
 5:('creme licht','c',(243,233,201)),6:('creme mid','c',(224,206,171)),7:('creme donker','c',(200,179,141)),
 8:('wang','r',(222,87,77)),9:('grijs licht','g',(180,168,164)),10:('grijs mid','g',(118,106,104)),11:('grijs donker','g',(70,60,56)),
 12:('geel','y',(248,221,95)),13:('geel donker','y',(213,186,91)),14:('wit','w',(255,255,255))}
P=np.array([M[k][2] for k in range(14)])
d=((b[:,:,None,:]-P[None,None])**2).sum(3); K=d.argmin(2)
K[b.min(2)>=232]=0
np.save('klassen.npy',K)
H,W=K.shape; img=P[K].astype('uint8'); img[K==0]=(255,255,255)
Image.fromarray(img).resize((W*5,H*5),0).save('_klassen5x.png')
print(np.bincount(K.ravel(),minlength=14))
