# sub.py x0 y0 x1 y1 [n] : per spritecel n x n submonsters van het model (gebiedsgemiddelde per subcel)
# K zwart, d donkerrood, m mid, l licht, h hooglicht, y/Y/W geel donker/mid/licht, . achtergrond
import cfg,sys,numpy as np
c=cfg.model(); x0,y0,x1,y1=map(int,sys.argv[1:5]); n=int(sys.argv[5]) if len(sys.argv)>5 else 2
def cl(p):
    L=p.mean()
    if p.min()>235: return '.'
    if p[0]>150 and p[1]>120 and p[2]<p[1]-25: return 'W' if L>215 else 'Y' if L>165 else 'y'
    return 'K' if L<45 else 'd' if L<72 else 'm' if L<97 else 'l' if L<122 else 'h'
s=cfg.S/n
print('    '+''.join(('%-*d'%(n,x))[:n]+'|' for x in range(x0,x1)))
for y in range(y0,y1):
    for j in range(n):
        row=''
        for x in range(x0,x1):
            for i in range(n):
                bx=cfg.X0+(x-cfg.LEFT)*cfg.S+i*s; by=cfg.Y0+(y-cfg.TOP)*cfg.S+j*s
                blk=c[int(round(by+s*.2)):int(round(by+s*.8))+1,int(round(bx+s*.2)):int(round(bx+s*.8))+1].reshape(-1,3)
                row+=cl(np.median(blk,axis=0))
            row+='|'
        print(('%3d '%y if j==0 else '    ')+row)
