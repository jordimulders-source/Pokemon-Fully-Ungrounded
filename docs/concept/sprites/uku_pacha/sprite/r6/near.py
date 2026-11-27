from PIL import Image; import numpy as np, math, sys
N=np.asarray(Image.open('../../model/r2_natief.png').convert('RGB')).astype(int)
F=64/92
PAL={'K':(16,20,28),'n':(36,50,76),'d':(66,78,102),'h':(130,164,200),'s':(82,102,132),'m':(108,130,158),'b':(112,150,172),'l':(119,175,186),'p':(156,212,212),'w':(194,235,230),'B':(75,108,148),'D':(44,73,111),'Y':(226,196,72),'P':(132,96,148),'W':(244,248,248)}
def cells(i,j):
  x0=5+i/F; x1=5+(i+1)/F; y0=7+(j-2)/F; y1=7+(j-1)/F
  return [(N[cy,cx],(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))) for cy in range(int(y0),math.ceil(y1)) for cx in range(int(x0),math.ceil(x1))]
def near(i,j):
  c=cells(i,j); acc={}
  for col,a in c:
    if col.mean()>245: k='.'
    else: k=min(PAL,key=lambda k:sum((np.array(PAL[k])-col)**2))
    acc[k]=acc.get(k,0)+a
  return max(acc,key=acc.get), acc
if __name__=='__main__':
  x0,x1,y0,y1=map(int,sys.argv[1:5])
  R=[l.rstrip() for l in open('raster_af.txt')][:64]
  for y in range(y0,y1): print('%2d '%y+R[y][x0:x1]+'   '+''.join(near(x,y)[0] for x in range(x0,x1)))
