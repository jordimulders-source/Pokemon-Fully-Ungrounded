import numpy as np; from PIL import Image
B=np.array(Image.open('gnometrotter_rock.png')).astype(int)
S={3,4,5,13}; P={7,8,15}; BL={10,11,12}; W={5,13,14}
parts={ # naam: (x0,x1,y0,y1, toegestane vultinten, lijn-tint)
 'muts':(18,45,0,15,S,2),'rots':(44,51,8,26,S,2),'haar L':(10,18,13,20,W,4),'haar R':(32,42,14,22,W,4),
 'baard':(15,31,21,37,W,4),'neus':(17,26,15,24,P,6),'lijf':(26,50,19,37,P,6),'vuist+arm L':(0,18,28,37,P,6),
 'arm R':(48,57,26,34,P,6),'hand R':(52,61,33,42,P,6),'riem':(17,51,36,42,S,2),'stok':(2,12,36,58,S,2),
 'broek':(16,51,40,56,BL,9),'schoen L':(13,31,53,58,S,2),'schoen R':(38,52,54,60,S,2)}
for n,(x0,x1,y0,y1,T,l) in parts.items():
  r=B[y0:y1,x0:x1]; u,c=np.unique(r,return_counts=True)
  d={('%X'%a):int(b) for a,b in zip(u,c) if a in T}
  print('%-12s vultinten %d %s'%(n,len(d),d))
