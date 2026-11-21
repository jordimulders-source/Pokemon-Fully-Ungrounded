# dekking.npy: per spritepixel het aandeel modelpixels (niet-wit) in zijn 2x2-groep natieve cellen (rij- en kolompaar waaruit geschrapt is).
import numpy as np; from PIL import Image
from modeltoon import r,c,DY,DX
a=np.asarray(Image.open('natief.png')).astype(int); fg=a.min(2)<215
def partner_r(i): return i+1 if i%2==1 else i-1      # rijgroepen (1,2),(3,4),...
def partner_c(i): return i+1 if i%2==0 else i-1      # kolomgroepen (0,1),(2,3),...
D=np.zeros((64,64))
for y in range(64):
    for x in range(64):
        j,i=y-DY,x-DX
        if 0<=j<len(r) and 0<=i<len(c):
            R=[r[j],partner_r(r[j])]; C=[c[i],partner_c(c[i])]
            R=[v for v in R if 0<=v<fg.shape[0]]; C=[v for v in C if 0<=v<fg.shape[1]]
            D[y,x]=fg[np.ix_(R,C)].mean()
np.save('dekking.npy',D)
o=np.load('tango_r5.npy')
print('r5 dekkend maar dekking<.5:',int(((o>0)&(D<.5)).sum()),' r5 leeg maar dekking>.5:',int(((o==0)&(D>.5)).sum()))
