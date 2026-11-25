# Materiaal per cel van het geschrapte model: 0 lucht 1 geel 2 rood 3 ijs 4 donker (ook oogwit-grijs telt als ijs)
import numpy as np
z=np.load('geschrapt.npz'); N=z['N'].astype(int); air=z['air']
R,G,B=N[...,0],N[...,1],N[...,2]; L=(R*299+G*587+B*114)/1000; sat=N.max(2)-N.min(2)
mat=np.full(L.shape,4)
mat[((B-R>10)&(L>=60))|((sat<25)&(L>120))]=3
mat[(R>90)&(R-B>50)&(G>70)]=1
mat[(R>120)&(R-G>50)&(R-B>40)]=2
mat[air]=0
H,W=mat.shape
if __name__=='__main__':
    print('   '+''.join(str(i%10) for i in range(W)))
    for j in range(H): print('%2d '%j+''.join('.yrik'[v] if not(v==3 and L[j,i]>=222) else 'w' for i,v in enumerate(mat[j])))
