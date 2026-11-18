# Meetgereedschap r3: model per spritepixel (venster uit de r2-geometrie) als gemiddelde, als 'donkerste 25%' en als mediaan.
# Gebruik: python3 box.py MODEL.png X0 Y0 X1 Y1 Z UIT.png
import sys,numpy as np; from PIL import Image
geo=np.load('../sprite_r2/kaal_info.npz')['geo']; S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
P=3.998; PH=3.25
mx=lambda X: PH+P*(bx0-S+OX+S*(X-X0+xmin)); my=lambda Y: PH+P*(by0-S+OY+S*(Y-Y0+ymin))
def win(M,X,Y): return M[int(round(my(Y))):int(round(my(Y+1))),int(round(mx(X))):int(round(mx(X+1)))].reshape(-1,3)
if __name__=='__main__':
    M=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); x0,y0,x1,y1,Z=map(int,sys.argv[2:7])
    w,h=x1-x0,y1-y0; out=np.zeros((h,3*w+4,3))+200
    for Y in range(y0,y1):
        for X in range(x0,x1):
            b=win(M,X,Y); l=b@[.299,.587,.114]; o=np.argsort(l)
            out[Y-y0,X-x0]=b.mean(0); out[Y-y0,w+2+X-x0]=b[o[:max(1,len(o)//4)]].mean(0); out[Y-y0,2*w+4+X-x0]=b[o[len(o)//2]]
    Image.fromarray(out.astype('uint8')).resize(((3*w+4)*Z,h*Z),Image.NEAREST).save(sys.argv[7])
