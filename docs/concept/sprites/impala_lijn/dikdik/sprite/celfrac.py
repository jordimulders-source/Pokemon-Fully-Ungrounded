# Per spritecel het aandeel modelpixels per klasse (modelpalet-index -> groep), om pixels uit het model te lezen
import sys, numpy as np
from PIL import Image
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); H=52
GR={0:'0',1:'D',2:'D',3:'S',4:'S',6:'S',7:'S',8:'M',9:'M',10:'M',11:'L',12:'L',13:'L',14:'L',15:'C',5:'I'}
a=np.asarray(Image.open('../referenties/model_r3b.png').convert('RGB')).astype(float)
C=np.load('model_pal.npy'); fg=a.min(2)<225
lab=((a.reshape(-1,1,3)-C[None])**2).sum(2).argmin(1).reshape(a.shape[:2])
ys,xs=np.nonzero(fg); x0,y0,y1=xs.min(),ys.min(),ys.max()+1; p=(y1-y0)/H
print('cel: top2 klassen (aandeel%)  .=achtergrond')
for j in range(Y0,Y1):
    row=[]
    for i in range(X0,X1):
        xa,xb=int(round(x0+i*p)),int(round(x0+(i+1)*p)); ya,yb=int(round(y0+j*p)),int(round(y0+(j+1)*p))
        f=fg[ya:yb,xa:xb]; l=lab[ya:yb,xa:xb]
        cnt={'.':(~f).sum()}
        for v in l[f].ravel(): g=GR[v]; cnt[g]=cnt.get(g,0)+1
        tot=f.size; s=sorted(cnt.items(),key=lambda t:-t[1])
        row.append(''.join('%s%02d'%(k,min(99,round(100*v/tot))) for k,v in s[:2]))
    print('%2d '%j+' '.join(row))
print('    '+' '.join('%-6d'%i for i in range(X0,X1)))
