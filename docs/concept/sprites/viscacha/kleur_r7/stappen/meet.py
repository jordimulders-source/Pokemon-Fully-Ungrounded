# meet.py: per spritepixel modelmaten -> meting.npz (dekking, donker-fractie, gem. kleur niet-donker) + onderlaag.txt
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/stappen')
from tl import *
from scipy import ndimage as nd
fg=np.abs(A-255).sum(2)>40
dk=LUM<75
cov=np.zeros((64,64)); dkf=np.zeros((64,64)); col=np.full((64,64,3),255.)
for y in range(64):
  for x in range(64):
    a,b=mbox(x,y); c,d=mbox(x+1,y+1)
    sl=(slice(max(0,int(round(b))),max(0,int(round(d)))),slice(max(0,int(round(a))),max(0,int(round(c)))))
    f=fg[sl]
    if f.size==0: continue
    cov[y,x]=f.mean(); dkf[y,x]=(dk[sl]&f).sum()/max(1,f.size)
    nn=f&~dk[sl]
    if nn.sum()>3: col[y,x]=A[sl][nn].mean(0)
np.savez(D+'stappen/meting.npz',cov=cov,dkf=dkf,col=col)
K='3456789ABCF'
rows=[]
for y in range(64):
  s=''
  for x in range(64):
    if cov[y,x]<0.12: s+='.'; continue
    if dkf[y,x]>=0.28: s+='1'; continue
    s+=min(K,key=lambda k:sum((col[y,x,i]-PAL[int(k,16)][i])**2 for i in range(3)))
  rows.append(s)
open(D+'onderlaag.txt','w').write('\n'.join(rows)+'\n')
print('\n'.join(rows))
