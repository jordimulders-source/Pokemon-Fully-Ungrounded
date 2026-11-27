# model -> natief raster: per modelcel (periode 5.70) de mediaan van het middelste 3x3-venster. Niets getekend.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')).astype(float)
PX,FX,PY,FY=5.704,5.16,5.692,3.088
nx=int((a.shape[1]-FX)//PX); ny=int((a.shape[0]-FY)//PY)
o=np.zeros((ny,nx,3),np.uint8)
for j in range(ny):
  cy=int(round(FY+(j+.5)*PY))
  for i in range(nx):
    cx=int(round(FX+(i+.5)*PX))
    o[j,i]=np.median(a[cy-1:cy+2,cx-1:cx+2].reshape(-1,3),0)
Image.fromarray(o).save('natief.png'); print(nx,ny)
Image.fromarray(o).resize((nx*6,ny*6),Image.NEAREST).save('natief_6x.png')
Image.fromarray(o[25:85,60:120]).resize((600,600),Image.NEAREST).save('natief_gezicht_10x.png')
