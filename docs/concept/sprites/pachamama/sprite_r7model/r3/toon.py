import sys,numpy as np; o=np.load(sys.argv[1]); y0,y1,x0,x1=[int(v) for v in sys.argv[2:6]]
ch={0:'.',1:'#',2:'2',3:'3',4:'4',5:'c',6:'b',7:'r',8:'R',9:'p',10:'P',11:'o',12:'O',13:'l',14:'g',15:'G'}
print('   '+' '.join('%2d'%x for x in range(x0,x1)))
for y in range(y0,y1): print('%2d '%y+' '.join(' '+ch[o[y,x]] for x in range(x0,x1)))
