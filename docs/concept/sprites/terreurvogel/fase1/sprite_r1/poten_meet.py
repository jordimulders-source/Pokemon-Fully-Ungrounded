# Meting pootgroep: per spritepixel % oranje (R-G>55, L>110) en % donker (L<85) in het model
import numpy as np; from lib import *
ORA=(GR==6)&(R-G>55)&(L>110); DK=(GR==6)&(L<85)
covO=np.zeros((64,64)); covD=np.zeros((64,64)); cel=np.zeros((64,64)); covP=np.zeros((64,64))
for j in range(Y0*SUB,Y1*SUB):
    ny=j//SUB; Y=int(np.floor(OY+((j+0.5)/SUB-Y0)*S))
    for i in range(X0*SUB,X1*SUB):
        nx=i//SUB; X=int(np.floor(OX+((i+0.5)/SUB-X0)*S))
        cel[Y,X]+=1; covO[Y,X]+=ORA[ny,nx]; covD[Y,X]+=DK[ny,nx]; covP[Y,X]+=GR[ny,nx]==6
fO=covO/np.maximum(cel,1); fD=covD/np.maximum(cel,1); fP=covP/np.maximum(cel,1)
if __name__=='__main__':
    Sx=np.load('r1.npy'); hx='0123456789ABCDEF'
    for y in range(54,63):
        print(y,' '.join('%d:%d/%d%s'%(x,int(100*fO[y,x]),int(100*fD[y,x]),'#' if Sx[y,x]==1 else hx[Sx[y,x]]) for x in range(18,44) if covP[y,x]>0))
