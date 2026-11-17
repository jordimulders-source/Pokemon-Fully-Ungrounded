# Hulp r10: per spritepixel het aandeel donkere lijn (lum<125, niet roze) en rood in het model (115%-kopvervorming), als tabel.
import sys, numpy as np; from PIL import Image
AX,AY,R,S=22.0,18.0,7.0,1.15
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float)
lum=M@[0.299,0.587,0.114]; pink=(M[...,0]-M[...,1])>90; line=(lum<125)&~pink; red=(M[...,0]>150)&(M[...,1]<90)&(M[...,2]<90)
def inv(u,v):
    d=AX-u; t=np.clip(d/R,0,1); w=t*t*(3-2*t); s=1+(S-1)*w
    return AX-d/s, AY+(v-AY)/s
def blok(x,y,n=8):
    pts=[inv(x+(i+.5)/n,y+(j+.5)/n) for i in range(n) for j in range(n)]
    idx=[(int(120+12*v),int(106+12*u)) for u,v in pts]
    L=np.mean([line[p] for p in idx]); Rd=np.mean([red[p] for p in idx]); mu=np.median([lum[p] for p in idx])
    return L,Rd,mu
if __name__=='__main__':
    x0,y0,x1,y1=[int(a) for a in sys.argv[1:5]]
    print('lijnaandeel x10 (rood=r):'); print('    '+''.join('%4d'%x for x in range(x0,x1)))
    for y in range(y0,y1):
        row=[]
        for x in range(x0,x1):
            L,Rd,mu=blok(x,y); row.append(('%3dr'%int(Rd*100)) if Rd>0.1 else '%4d'%int(L*100))
        print('%3d '%y+''.join(row))
