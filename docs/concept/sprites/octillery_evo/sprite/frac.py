# frac.py x0 y0 x1 y1 : per spritecel: Y/y geel, D/d donker(lijn), P roze, G grijs, '-' rood, ' ' achtergrond
import cfg,numpy as np,sys
c=cfg.model(); L=c.mean(2); sat=c.max(2)-c.min(2); fg=cfg.fgmask(c)
yel=(c[...,0]>150)&(c[...,1]>110)&(c[...,2]<c[...,1]-30)
dark=(L<55)&fg
pink=(c[...,1]>0.5*c[...,0])&~yel&(L>90)&(sat>30)
gray=(sat<40)&(L>=55)&(L<150)
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('   '+''.join(str(x//10) for x in range(x0,x1))); print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
    s='%2d '%y
    for x in range(x0,x1):
        sl=cfg.cell(x,y); f=fg[sl]
        if f.mean()<0.3: s+=' '; continue
        Y,D,Pp,Gg=yel[sl].mean(),dark[sl].mean(),pink[sl].mean(),gray[sl].mean()
        s+= 'Y' if Y>=.4 else 'y' if Y>=.2 else 'D' if D>=.4 else 'G' if Gg>=.4 else 'P' if Pp>=.5 else 'd' if D>=.2 else '-'
    print(s)
