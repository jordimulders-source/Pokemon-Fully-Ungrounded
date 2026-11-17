# Vruchtvlees/tand-fractie per spritepixel (lichtgrijs/wit binnen de figuur, niet de achtergrond) + zwartfractie.
# Gebruik: python3 vlees.py MODEL X0 Y0 X1 Y1
import sys,numpy as np; from PIL import Image; from box import win
M=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); x0,y0,x1,y1=map(int,sys.argv[2:6])
l=M@[.299,.587,.114]; s=M.max(2)-M.min(2); w=(l>225)&(s<30)
BG=np.zeros_like(w); BG[0]=w[0]; BG[-1]=w[-1]; BG[:,0]=w[:,0]; BG[:,-1]=w[:,-1]
while True:
    p=np.pad(BG,1); n=(p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]|BG)&w
    if (n==BG).all(): break
    BG=n
K=np.zeros(M.shape[:2]); K[(l>150)&(s<45)&~BG]=1; K[l<55]=2; K[BG]=3
print('    '+''.join('%-6d'%x for x in range(x0,x1)))
for Y in range(y0,y1):
    r='%2d  '%Y
    for X in range(x0,x1):
        k=win(K[...,None].repeat(3,2),X,Y)[:,0]
        r+='%d/%d/%d '%(min(9,10*(k==1).mean()),min(9,10*(k==2).mean()),min(9,10*(k==3).mean()))
    print(r)
