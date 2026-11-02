# Losse controle: PNG-index != 0  <->  '#' in silhouet_bevroren.txt en True in silhouet_bevroren.npy
import os, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); S=os.path.join(H,'../../../../silhouet/')
im=Image.open(os.path.join(H,'../nachtaap.png'))
print('modus',im.mode,'maat',im.size,'transparency',im.info.get('transparency'),'kleuren in palet',len(im.getpalette())//3)
a=np.array(im)!=0
t=np.array([[c=='#' for c in l.rstrip('\n')] for l in open(S+'silhouet_bevroren.txt')][:64])
n=np.load(S+'silhouet_bevroren.npy').astype(bool)
print('pixels',a.sum(),'| diff txt',int((a!=t).sum()),'| diff npy',int((a!=n).sum()))
print('gebruikte indexen',sorted(set(np.array(im).flatten().tolist())))
