# Route B, stap 3a: natief (na samenvoegen) eerst verkleinen door kolommen/rijen te SCHRAPPEN (Gengas-methode),
# op natieve resolutie (lijnen zijn hier nog 1 px en worden zelden gekozen). Daarna half.py (exacte 2x).
import sys; from PIL import Image; import numpy as np
NC=int(sys.argv[1]); NR=int(sys.argv[2]); GAP=int(sys.argv[3]) if len(sys.argv)>3 else 4
a=np.asarray(Image.open('natief_samen.png').convert('RGB')).astype(int)
fg=a.min(2)<225; ys,xs=np.where(fg); a=a[ys.min()-1:ys.max()+2,xs.min()-1:xs.max()+2]
def kies(A,n):
    cost=[np.abs(A[i]-A[i+1]).sum() for i in range(len(A)-1)]
    order=np.argsort(cost,kind='stable'); g=[]
    for i in order:
        if all(abs(i-j)>=GAP for j in g): g.append(int(i))
        if len(g)==n: break
    return sorted(g)
rows=kies(a,NR); cols=kies(a.transpose(1,0,2),NC)
b=np.delete(np.delete(a,rows,0),cols,1)
print('rijen',rows,'kolommen',cols,'->',b.shape[1],'x',b.shape[0])
Image.fromarray(b.astype(np.uint8)).save('natief_geschrapt.png'); open('schrap.txt','w').write(f'{rows}\n{cols}\n')
