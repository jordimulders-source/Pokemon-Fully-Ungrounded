# r15: basis = model 3x verkleind; in het ijs wint de donkerste pixel (modellijnen blijven), elders mediaan; palet r14
import numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
a=np.pad(a,((30,30),(30,30),(0,0)),constant_values=255)
ox,oy=15,-6
T=np.full((64,64,3),255); line=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64):
    b=a[3*j+oy+30:3*j+oy+33,3*i+ox+30:3*i+ox+33].reshape(-1,3); l=b.mean(1)
    icy=((l>165)&(b[:,2]>=b[:,0])&(np.abs(b[:,0]-b[:,1])<40)).any()   # licht ijs in het blok
    purp=((b[:,2]-b[:,1])>35).sum()>=3                                    # paars/pieken
    if (l<80).sum()>=2 and icy and not purp: T[j,i]=b[l.argmin()]; line[j,i]=True
    else: T[j,i]=np.median(b,0)
fg=T.sum(2)<738
r=Image.open('r14.png'); pal=r.getpalette(); P=np.array(pal[:48]).reshape(16,3).astype(float)
o=np.zeros((64,64),int)
for j,i in zip(*np.where(fg)):
  if line[j,i]: o[j,i]=1
  else: o[j,i]=1+int(np.argmin(((P[1:]-T[j,i])**2).sum(1)))
np.save('r15w/line.npy',line&fg); np.save('r15w/o0.npy',o)
im=Image.fromarray(o.astype(np.uint8)).convert('P'); im.putpalette(pal); im.save('r15w/o0.png',transparency=0)
im.convert('RGB').resize((512,512),Image.NEAREST).save('r15w/o0_8x.png')
