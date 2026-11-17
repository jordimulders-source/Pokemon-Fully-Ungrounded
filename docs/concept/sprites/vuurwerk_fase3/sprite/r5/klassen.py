# r5 stap 1: klassekaart op volle modelresolutie (1024x1024). Elke modelpixel krijgt de klasse van zijn natieve pixel
# (../r3/natief_q_dg.png, pitch 5,12; natieve pixel k beslaat modelx [(k+0.5)*5.12+4.25, (k+1.5)*5.12+4.25)).
# Groepen (componenten >= 3 natieve px, zoals de lijnkaart van r3): roze vlam (6-12), rood (10-11, de pupil), bruine lijn (1,2),
# goud/tan (3,14). Opgeslagen als bitmaskers in klassen.npz.
import numpy as np; from PIL import Image
from scipy import ndimage
q=np.asarray(Image.open('../r3/natief_q_dg.png')).astype(int)
def comp(m):
    lab,n=ndimage.label(m,np.ones((3,3))); gr=np.bincount(lab.ravel()); return m&(gr[lab]>=3)
G={'roze':comp(np.isin(q,[6,7,8,9,10,11,12])),'rood':np.isin(q,[10,11]),'bruin':comp(np.isin(q,[1,2])),'goud':comp(np.isin(q,[3,14]))}
k=np.clip(np.floor((np.arange(1024)-4.25)/5.12-0.5).astype(int),0,None)
ky=np.clip(k,0,q.shape[0]-1); kx=np.clip(k,0,q.shape[1]-1)
out={n:np.packbits(m[ky][:,kx]) for n,m in G.items()}
np.savez_compressed('klassen.npz',**out); print({n:int(m.sum()) for n,m in G.items()})
