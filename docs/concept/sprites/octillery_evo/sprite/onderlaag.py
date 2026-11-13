import cfg,numpy as np,sys
c=cfg.model(); fg=cfg.fgmask(c); L=c.mean(2)
def kleur(m):  # gemiddelde niet-lijn kleur -> index
    r,g,b=m; l=m.mean(); sat=m.max()-m.min()
    if g>0.68*r and r>110 and b<g-25: return 12 if l>175 else 11 if l>125 else 10
    if sat<32: return 13 if l>80 else 14
    if g/r>0.54 and l>95: return 9 if l>165 else 8 if l>128 else 7
    return 2 if l<62 else 3 if l<80 else 4 if l<100 else 5 if l<122 else 6
if __name__=="__main__":
  a=np.zeros((64,64),int); dark=np.zeros((64,64))
  for y in range(cfg.TOP,64):
    for x in range(cfg.LEFT,cfg.LEFT+cfg.W):
      sl=cfg.cell(x,y); f=fg[sl]
      if f.mean()<0.45: continue
      d=(L[sl]<48)&f; dark[y,x]=d.sum()/f.sum()
      nd=f&~d
      a[y,x]=kleur(c[sl][nd].mean(0)) if nd.sum()>3 else 1
      if dark[y,x]>=0.4: a[y,x]=1
  np.save('dark.npy',dark)
  cfg.write(a,sys.argv[1]); print('px',(a>0).sum())
  