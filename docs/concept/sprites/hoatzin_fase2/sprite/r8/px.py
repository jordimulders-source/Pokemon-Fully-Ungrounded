# Modelmeting per spritepixel (canvascoördinaten): gemiddelde helderheid, p15 en max van het model in die cel
import sys, numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); L=N.mean(2); Z=np.load('zones_nat.npy')
ys,xs=np.where(Z!='.'); x0,y0=xs.min(),ys.min(); s=(ys.max()+1-y0)/63; X0,Y0=6,1
def cel(cx,cy):
    a=y0+(cy-Y0)*s; b=x0+(cx-X0)*s
    blk=L[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]; zb=Z[int(a):int(np.ceil(a+s)),int(b):int(np.ceil(b+s))]
    m=zb!='.'
    return blk[m] if m.any() else np.array([255.])
x1,x2,y1,y2=map(int,sys.argv[1:5])
S=np.asarray(Image.open(sys.argv[5] if len(sys.argv)>5 else 'hoatzin.png'))
print('     '+' '.join('%4d'%x for x in range(x1,x2+1)))
for y in range(y1,y2+1):
    print('%3d  '%y+' '.join('%4d'%int(np.percentile(cel(x,y),float(__import__('os').environ.get('PC',50)))) for x in range(x1,x2+1)),'  ',''.join('.' if v==0 else '0123456789abcdef'[v] for v in S[y,x1:x2+1]))
