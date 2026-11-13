# lumkaart.py x0 x1 y0 y1 : mediaan modelhelderheid per spritecel (. = achtergrond), 3 tekens per cel (/2)
import cfg,numpy as np,sys
c=cfg.model(); L=c.mean(2); fg=cfg.fgmask(c)
x0,x1,y0,y1=map(int,sys.argv[1:5])
print('   '+''.join('%3d'%x for x in range(x0,x1)))
for y in range(y0,y1):
  s='%2d '%y
  for x in range(x0,x1):
    sl=cfg.cell(x,y); f=fg[sl]
    s+= '  .' if f.mean()<.4 else '%3d'%min(99,int(np.median(L[sl][f])//2))
  print(s)
