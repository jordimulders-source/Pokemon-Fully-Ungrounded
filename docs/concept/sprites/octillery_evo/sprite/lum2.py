# lum2: per spritecel de mediane helderheid van niet-lijnpixels in een venster van 1,6 cel (zachter)
import cfg,numpy as np
c=cfg.model(); fg=cfg.fgmask(c); L=c.mean(2)
M=np.zeros((64,64)); S=cfg.S
for y in range(cfg.TOP,64):
  for x in range(cfg.LEFT,cfg.LEFT+cfg.W):
    bx=cfg.X0+(x-cfg.LEFT+0.5)*S; by=cfg.Y0+(y-cfg.TOP+0.5)*S; r=0.8*S
    sl=(slice(max(0,int(by-r)),int(by+r)),slice(max(0,int(bx-r)),int(bx+r)))
    f=fg[sl]&(L[sl]>=55)
    if f.sum()>5: M[y,x]=np.median(L[sl][f])
np.save('lum2.npy',M)
