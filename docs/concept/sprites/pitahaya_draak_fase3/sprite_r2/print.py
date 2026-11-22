import sys,numpy as np; from PIL import Image
o=np.asarray(Image.open(sys.argv[1])).astype(int); x0,y0,x1,y1=map(int,sys.argv[2:6])
ch={0:'.',1:'#',2:'d',3:'r',4:'p',5:'P',6:'g',7:'G',8:'h',9:'H',10:'w',11:'W',12:'o',13:'y',14:'Y',15:'s'}
print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+''.join(ch[o[y,x]] for x in range(x0,x1)))
