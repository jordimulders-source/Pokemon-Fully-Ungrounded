import numpy as np; from scipy import ndimage as nd
m=np.load('mond_model.npy'); m=nd.binary_closing(m,structure=np.ones((9,9))); m=nd.binary_fill_holes(m)
np.save('mond_vol.npy',m)
S=968/62; cv=np.zeros((64,64))
for j in range(64):
  for i in range(64):
    x0=24+(i-1)*S; y0=1+(j-4)*S
    xa,ya,xb,yb=max(int(round(x0)),0),max(int(round(y0)),0),min(int(round(x0+S)),1024),min(int(round(y0+S)),1024)
    if xb>xa and yb>ya: cv[j,i]=m[ya:yb,xa:xb].mean()
np.save('mond_cov.npy',cv)
for T in [0.5,0.4,0.33]:
  print(T)
  for j in range(30,44): print('%2d'%j,''.join('#' if cv[j,i]>=T else '.' for i in range(12,47)))
