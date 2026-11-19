# Close-up van het natieve model op het spriteraster (12 px per spritepixel, rasterlijnen), voor kop/oog/neus-metingen.
import sys; from px import *
X0,X1,Y0,Y1,OUT=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
K=12; im=Image.new('RGB',((X1-X0)*K,(Y1-Y0)*K)); P=im.load()
for Y in range((Y1-Y0)*K):
  for X in range((X1-X0)*K):
    x=X0+X/K; y=Y0+Y/K
    a,_,b,_=cell(int(x),int(y)); nx=a+(x-int(x))*s; ny=b+(y-int(y))*s
    v=N[min(N.shape[0]-1,int(ny)),min(N.shape[1]-1,int(nx))]
    if X%K==0 or Y%K==0: v=v*0.8
    P[X,Y]=tuple(int(c) for c in v)
im.save(OUT)
