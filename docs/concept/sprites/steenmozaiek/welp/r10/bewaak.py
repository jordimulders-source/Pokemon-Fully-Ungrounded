# Bewaking r10: buiten de kopzone (array x<=16 en y<=22; in 64x64: x<=23, y<=40) moet de pixeldiff met r9 0 zijn. Per onderdeel de diff.
import numpy as np
r9=np.load('../r9/welp_r9.npy'); a=np.load('welp_r10.npy')
z=np.zeros_like(a,bool); z[:23,:17]=True
d=(a!=r9)
print('diff buiten zone:',int(d[~z].sum()),'| binnen zone:',int(d[z].sum()),'| silhouet-diff:',int(((a>0)!=(r9>0)).sum()))
delen={'band (x4-15,y1-7)':(4,1,16,8),'ver oog (x3-5,y8-11)':(3,8,6,12),'oog (x9-15,y8-12)':(9,8,16,13),
       'snuit/neus (x0-9,y11-16)':(0,11,10,17),'bek+tanden (x3-12,y15-22 zonder tong)':None,'tong (x4-8,y18-22)':(4,18,9,23)}
tong=np.zeros_like(z); tong[18:23,4:9]=True
for k,b in delen.items():
    m=np.zeros_like(z)
    if b: m[b[1]:b[3],b[0]:b[2]]=True
    else: m[15:23,3:13]=True; m&=~tong
    print('%-40s %3d'%(k,int((d&m).sum())))
F=np.load('FIN10.npy'); print('kleuren gebruikt:',len(np.unique(a)),'(incl. transparant)')
assert int(d[~z].sum())==0
