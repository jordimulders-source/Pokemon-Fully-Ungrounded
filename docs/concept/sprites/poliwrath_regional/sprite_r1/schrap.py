# Model gespiegeld (Jordi: "gespiegeld uiteraard he") en 75x72 -> 62x60 ZONDER resamplen (Gengas-methode):
# 13 kolommen en 12 rijen schrappen die het meest op hun buur lijken, gespreid (>=3 uit elkaar),
# niet door ogen (O1) en modelspiraal (S1). Elke overgebleven cel is een echte modelcel.
import numpy as np, sys; from PIL import Image
z=np.load('natief.npz'); N=z['N'][:,::-1].astype(int); air=z['air'][:,::-1]
A=N.copy(); A[air]=-400                      # lucht telt als sterk verschillend
NC,NR=int(sys.argv[1]) if len(sys.argv)>1 else 13, int(sys.argv[2]) if len(sys.argv)>2 else 12
VR=set(range(7,20))|set(range(28,43))           # oog- en mondrijen (kop), spiraalrijen
VK=set(range(20,29))|set(range(25,47))|set(range(39,48))  # oogkolommen, spiraalkolommen
def kies(a,n,axis,verboden):
    B=a if axis==0 else a.transpose(1,0,2)
    cost=[np.abs(B[i]-B[i+1]).sum() for i in range(len(B)-1)]
    gek=[]
    for i in np.argsort(cost,kind='stable'):
        if i in verboden or i+1 in verboden: continue
        if all(abs(i-j)>=3 for j in gek): gek.append(int(i))
        if len(gek)==n: break
    return sorted(gek)
rows=kies(A,NR,0,VR); cols=kies(A,NC,1,VK)
M=np.delete(np.delete(N,rows,0),cols,1); Ma=np.delete(np.delete(air,rows,0),cols,1)
print('rijen',rows); print('kolommen',cols); print('maat',M.shape[1],'x',M.shape[0])
np.savez('geschrapt.npz',N=M,air=Ma,rows=rows,cols=cols)
im=M.astype('uint8').copy(); im[Ma]=(152,208,160)
Image.fromarray(im).resize((M.shape[1]*8,M.shape[0]*8),Image.NEAREST).save('geschrapt_8x.png')
