# raster.py file.npy x0 y0 x1 y1 : indexraster als tekens (. transp, 0 zwart, groen G=15 outline 2 3 4, goud 5 6 7 8, creme 9 a b c, p paars, w wit)
import sys,numpy as np
S=np.load(sys.argv[1]); ch='.0234' '5678' '9abc' 'pwG'
ch={0:'.',1:'#',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'p',14:'w',15:'G'}
x0,y0,x1,y1=map(int,sys.argv[2:6])
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print(f'{y:3d} '+''.join(ch[int(v)] for v in S[y,x0:x1]))
