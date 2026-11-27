# Gezicht stap 1: vlakken. Per spritecel de mediaan van de modelpixels die GEEN dunne lijn/oog zijn -> dichtstbijzijnde gezichtstint (3,4,13).
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('../natief_g1.png').convert('RGB')).astype(float); L=lum(a)
MY,MX=np.load('basis_map.npy'); gezn=np.load('../natief_g1_gez.npy'); zone=np.load('gezzone.npy')
from numpy.lib.stride_tricks import sliding_window_view as sw
med=np.median(sw(np.pad(L,2,mode='edge'),(5,5)),axis=(-1,-2)); lijnn=(L<100)&(med-L>18)
# grote licht/donker-vlakken: mediaan 5x5 natief over alleen gezichtspixels (haalt de 1-px lijnen eruit, vlakken blijven)
G=np.where(gezn[...,None],a,np.nan); Gp=np.pad(G,((2,2),(2,2),(0,0)),constant_values=np.nan)
V=sw(Gp,(5,5),axis=(0,1)).reshape(G.shape[0],G.shape[1],3,-1); A=np.nanmedian(V,axis=-1)
o=np.load('romp.npy'); T=np.zeros((64,64),int)
for y in range(64):
  for x in range(64):
    if not zone[y,x]: continue
    b=(slice(MY+3*y,MY+3*y+3),slice(MX+3*x,MX+3*x+3))
    if gezn[b].sum()<3: continue
    T[y,x]=nearest(np.nanmedian(A[b][gezn[b]],0)[None],(2,3,4,13))[0]
np.save('gez_toon.npy',T)
ys,xs=np.where(T>0); print(ys.min(),ys.max(),xs.min(),xs.max())
ch={0:' ',2:'#',3:'=',4:'-',13:'.'}
for y in range(ys.min(),ys.max()+1): print('%2d '%y+''.join(ch[T[y,x]] for x in range(xs.min(),xs.max()+1)))
print('   '+''.join(str(x%10) for x in range(xs.min(),xs.max()+1)))
