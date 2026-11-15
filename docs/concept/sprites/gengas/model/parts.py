from PIL import Image; import numpy as np, sys
sys.path.insert(0,sys.argv[2]); from seg import label
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
R,G,B=a[...,0],a[...,1],a[...,2]; lum=0.299*R+0.587*G+0.114*B
bg=a.min(axis=2)>=232
sat=a.max(axis=2)-a.min(axis=2)
dark=(lum<60)&~bg
grey=(sat<28)&~bg&~dark
body=~bg&~dark&~grey
H,W=bg.shape; cls=np.zeros((H,W),int); cls[body]=1; cls[grey]=2
for y,x in zip(*np.where(dark)):
    w=cls[max(0,y-2):y+3,max(0,x-2):x+3]
    nb,ng=(w==1).sum(),(w==2).sum()
    cls[y,x]=2 if ng>nb else 1
lab,n=label(cls==2)
np.save(sys.argv[3]+'/cls.npy',cls); np.save(sys.argv[3]+'/lab.npy',lab)
for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    print(i,len(xs),xs.min(),xs.max(),ys.min(),ys.max())
v=np.zeros((H,W,3),'uint8')+255; v[cls==1]=(200,60,90)
cols=[(0,0,0),(40,120,220),(40,180,60),(230,150,0),(140,0,200),(0,180,180),(120,120,120)]
for i in range(1,n+1): v[lab==i]=cols[i%len(cols)]
Image.fromarray(v).resize((W*6,H*6),Image.NEAREST).save(sys.argv[3]+'/parts.png')
