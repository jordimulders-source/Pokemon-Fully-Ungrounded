# Bewijs: elke afwijkende pixel r2 <-> r1 valt in een benoemde reparatiezone; silhouetverschil apart geteld
import numpy as np
R1=np.load('r1.npy'); Z={'5 oog':(5,10,17,23),'1 snavel':(0,8,0,14),'2 aansluiting':(4,8,10,16),'3 kopomtrek':(0,3,16,25),'4 volume kop':(1,10,14,26),
 '4 volume buik':(20,30,12,30),'6 staart':(19,25,33,40),'7 vleugellijnen':(19,29,20,36)}
for nm in ('r2_a','r2_b'):
    A=np.load(nm+'.npy'); d=np.argwhere(A!=R1); per={k:0 for k in Z}; buiten=[]
    for y,x in d:
        for k,(y0,y1,x0,x1) in Z.items():
            if y0<=y<y1 and x0<=x<x1: per[k]+=1; break
        else: buiten.append((int(y),int(x)))
    sil_weg=int(((R1>0)&(A==0)).sum()); sil_bij=int(((R1==0)&(A>0)).sum())
    print(nm,'totaal',len(d),per,'buiten zones',buiten,'silhouet -',sil_weg,'+',sil_bij,'px',int((A>0).sum()),'kleuren',len(set(A.ravel())))
    for k,(y0,y1,x0,x1) in Z.items():
        m=np.zeros_like(A,bool); m[y0:y1,x0:x1]=1
        print('   ',k,'silhouet -',int(((R1>0)&(A==0)&m).sum()),'+',int(((R1==0)&(A>0)&m).sum()))
