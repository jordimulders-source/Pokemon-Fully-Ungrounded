# Per spritepixel de dominante modelklasse + aandeel: Z zwart, B achtergrond, W wit/grijs (vlees, tand, oog), L lichtroze,
# R middenroze, D donkerroze, g/G groen donker/licht, Y geel. Gebruik: python3 klas.py MODEL X0 Y0 X1 Y1
import sys,numpy as np; from PIL import Image; from box import win
M=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); x0,y0,x1,y1=map(int,sys.argv[2:6])
_l=M@[.299,.587,.114]; _s=M.max(2)-M.min(2); _w=(_l>225)&(_s<30)
BG=np.zeros_like(_w); BG[0]=_w[0]; BG[-1]=_w[-1]; BG[:,0]=_w[:,0]; BG[:,-1]=_w[:,-1]
while True:
    p=np.pad(BG,1); n=(p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]|BG)&_w
    if (n==BG).all(): break
    BG=n
M=M.copy(); M[BG]=[999,999,999]
def kl(p):
    r,g,b=p; l=.299*r+.587*g+.114*b; s=max(p)-min(p)
    if l<55: return 'Z'
    if r>900: return 'B'
    if s<45: return 'W'
    if r>g+40 and r>b:   # roze
        return 'L' if l>130 else ('R' if l>85 else 'D')
    if g>=r and g>b: return 'G' if l>120 else 'g'
    if r>=g and g>b+40: return 'Y'
    return '?'
print('    '+''.join('%-6d'%x for x in range(x0,x1)))
for Y in range(y0,y1):
    s='%2d  '%Y
    for X in range(x0,x1):
        w=win(M,X,Y); c={}
        for p in w: k=kl(p); c[k]=c.get(k,0)+1
        it=sorted(c.items(),key=lambda t:-t[1]); n=len(w)
        a=it[0]; b=it[1] if len(it)>1 else ('-',0)
        s+='%s%d%s%d '%(a[0],min(9,10*a[1]//n),b[0],min(9,10*b[1]//n))
    print(s)
