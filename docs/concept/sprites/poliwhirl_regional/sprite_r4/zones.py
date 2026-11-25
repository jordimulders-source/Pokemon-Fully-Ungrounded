# geel/donker per zone: model (pixels in de cellen) vs sprite. python3 zones.py sprite.npy
import sys,numpy as np; from PIL import Image
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
def masks(a):
    a=a/255.0; mx=a.max(-1); mn=a.min(-1); s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0); r,g,b=a[...,0],a[...,1],a[...,2]; d=np.maximum(mx-mn,1e-6)
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))/6
    return (h>=0.1)&(h<=0.2)&(s>0.4)&(mx>0.5),(mx<0.45)&(s<0.6)
M=np.asarray(Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')).astype(float)
MY,MD=masks(M)
o=np.load(sys.argv[1]); P=np.array(PAL,float); P[0]=255
SY,SD=masks(P[o])
Z={'kop':(12,34,0,13),'lijf':(13,32,12,31),'linkerarm':(6,15,12,20),'rechterarm':(30,44,12,21),'linkerbeen+voet':(7,21,30,46),'rechterbeen+voet':(29,44,30,46),'totaal':(0,49,0,46)}
for n,(x0,x1,y0,y1) in Z.items():
    sl=(slice(int(ys[y0]),int(ys[y1+1])),slice(int(xs[x0]),int(xs[x1+1])))
    my,md=MY[sl].sum(),MD[sl].sum(); sy,sd=SY[y0:y1+1,x0:x1+1].sum(),SD[y0:y1+1,x0:x1+1].sum()
    print('%-18s model %.2f   sprite %.2f (%d/%d)'%(n,my/max(md,1),sy/max(sd,1),sy,sd))
# kop zonder oogzone (cols 11-21 en 24-34, rij 0-9)
sl=(slice(int(ys[0]),int(ys[14])),slice(int(xs[12]),int(xs[35])))
mm=np.ones((MY.shape),bool); 
for x0,x1 in ((11,21),(24,34)): mm[int(ys[0]):int(ys[10]),int(xs[x0]):int(xs[x1+1])]=False
my,md=(MY&mm)[sl].sum(),(MD&mm)[sl].sum()
sm=np.ones(o.shape,bool); sm[0:10,11:22]=False; sm[0:10,24:35]=False
sy,sd=(SY&sm)[0:14,12:35].sum(),(SD&sm)[0:14,12:35].sum()
print('kop zonder ogen    model %.2f   sprite %.2f'%(my/md,sy/sd))
mm2=np.ones(MY.shape,bool)
for x0,x1 in ((11,21),(24,34)): mm2[int(ys[0]):int(ys[10]),int(xs[x0]):int(xs[x1+1])]=False
sl=(slice(int(ys[0]),int(ys[47])),slice(int(xs[0]),int(xs[50])))
sm=np.ones(o.shape,bool); sm[0:10,11:22]=False; sm[0:10,24:35]=False
print('totaal zonder ogen model %.2f   sprite %.2f'%((MY&mm2)[sl].sum()/(MD&mm2)[sl].sum(),(SY&sm).sum()/(SD&sm).sum()))
# alleen 'binnen' (zonder omlijningspixels in de sprite / zonder 1-cel rand in het model niet mogelijk): sprite zonder index 1
print('sprite zonder omlijning (index 1) en zonder ogen: %.2f'%((SY&sm).sum()/(SD&sm&(o!=1)).sum()))
