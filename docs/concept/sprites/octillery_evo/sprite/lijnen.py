# lijnen.py: skelet van de donkere modellijnen -> spritecellen (lijnkaart.npy: aantal skeletpixels per cel)
import cfg,numpy as np
from skimage.morphology import skeletonize
c=cfg.model(); L=c.mean(2); fg=cfg.fgmask(c)
dk=(L<62)&fg
sk=skeletonize(dk)
n=np.zeros((64,64))
for y in range(cfg.TOP,64):
  for x in range(cfg.LEFT,cfg.LEFT+cfg.W):
    sl=cfg.cell(x,y); n[y,x]=sk[sl].sum()
np.save('lijnkaart.npy',n)
A=np.load('A.npy') if False else None
for y in range(23,64): print('%2d '%y+''.join('.' if n[y,x]==0 else str(min(9,int(n[y,x]))) for x in range(64)))
