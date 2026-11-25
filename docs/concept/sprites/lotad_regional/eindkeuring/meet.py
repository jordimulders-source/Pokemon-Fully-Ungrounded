# Meetgereedschap eindkeuring: modelhelderheid per spritepixel (ML) en materiaalkaart (fm) uit de kale reductie van r2.
# Spritepixel (x,y) = natief blok 2x2 op (1+2*(x-10+37), 1+2*(y-22+11)) van r2/natief.png (fase OY=1,OX=1; plaats() offset).
import sys, os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R2=os.path.join(H,'..','sprite','r2')
sys.path.insert(0,R2); _cwd=os.getcwd(); os.chdir(R2)
from half2t import reduceer, plaats
o,mat,oogb=reduceer(1,1); (_,fm,_),_=plaats(o,mat,oogb)
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); os.chdir(_cwd)
Ln=nat@[0.299,0.587,0.114]
ML=np.zeros((64,64))
for y in range(64):
    for x in range(64):
        ny=1+2*(y-22+11); nx=1+2*(x-10+37)
        if 0<=ny<Ln.shape[0]-1 and 0<=nx<Ln.shape[1]-1: ML[y,x]=Ln[ny:ny+2,nx:nx+2].mean()
def randkaart(s):
    fig=s>0; pad=np.pad(fig,1)
    return fig&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
