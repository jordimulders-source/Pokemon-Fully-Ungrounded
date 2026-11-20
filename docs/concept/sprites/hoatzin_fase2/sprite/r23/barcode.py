# barcode.py: 1-px om-en-om binnen de figuur (a b a b a, 5 px) per rij en per kolom, a,b != 0
import sys, numpy as np; from PIL import Image
a=np.array(Image.open(sys.argv[1] if len(sys.argv)>1 else 'hoatzin.png')).astype(int); r=[]
for t,A in (('rij',a),('kol',a.T)):
    for i in range(64):
        for j in range(60):
            v=A[i,j:j+5]
            if (v>0).all() and v[0]==v[2]==v[4] and v[1]==v[3] and v[0]!=v[1]: r.append((t,i,j,int(v[0]),int(v[1])))
print('barcode',len(r),r)
