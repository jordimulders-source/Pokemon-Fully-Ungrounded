# r4: lijnkaart van de goud/tan strengen in de kop (zoals ../r3/lijnkaart.py voor roze): natieve pixels van klasse tan 3 of
# goud 14 in ../r3/natief_q_dg.png, componenten >= 3 natieve px, per spritepixel geteld (middelpunt-regel).
import numpy as np; from PIL import Image
from scipy import ndimage
q=np.asarray(Image.open('../r3/natief_q_dg.png')).astype(int)
S=12/5.12; OX=(106-4.25)/5.12-0.5; OY=(120-4.25)/5.12-0.5
m=np.isin(q,[3,14]); lab,n=ndimage.label(m,np.ones((3,3)))
gr=np.bincount(lab.ravel()); m&=gr[lab]>=3
k=np.zeros((64,64),int)
for y,x in zip(*np.where(m)):
    i=int(np.floor((x+0.5-OX)/S)); j=int(np.floor((y+0.5-OY)/S))
    if 0<=i<64 and 0<=j<64: k[j,i]+=1
np.save('kaart_goud.npy',k)
if __name__=='__main__':
    for y in range(3,31): print('%2d'%y,''.join(str(min(9,v)) if v else '.' for v in k[y,:26]))
