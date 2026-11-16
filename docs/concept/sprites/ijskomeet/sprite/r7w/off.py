import sys; sys.path.insert(0,'.'); sys.path.insert(0,'r6w')
import numpy as np; from PIL import Image
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); L=np.pad((n.mean(2)<60).astype(float),30)
def Fof(ox,oy):
    F=np.zeros((64,64))
    for j in range(64):
      for i in range(64):
        F[j,i]=L[3*j+oy+30:3*j+oy+33,3*i+ox+30:3*i+ox+33].mean()
    return F
if __name__=='__main__':
    import p6
    o=p6.from_txt(sys.argv[1]); seam=np.isin(o,[p6.CH.index(c) for c in sys.argv[2]])
    reg=np.zeros((64,64),bool); reg[20:62,0:36]=True; ins=reg&(o>=0)
    res=[]
    for oy in range(-10,6):
      for ox in range(2,22):
        F=Fof(ox,oy); sc=(F*seam*ins).sum()/(seam*ins).sum()-(F*(~seam)*ins).sum()/((~seam)*ins).sum()
        res.append((round(sc,3),ox,oy))
    res.sort(reverse=True); print(res[:5])
