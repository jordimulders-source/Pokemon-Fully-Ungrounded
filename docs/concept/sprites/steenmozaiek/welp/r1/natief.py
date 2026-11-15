# Gemini-raster terughalen: pitch 5,12 px, fase 4,1 (randsterkte-fit, x en y). Cel = mediaan van het binnenste 3x3. Niets getekend.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')).astype(int)
P,PH=5.12,4.1; n=int((1024-PH)/P)
out=np.zeros((n,n,3),'uint8')
for j in range(n):
  for i in range(n):
    cy,cx=int(round(PH+P*(j+.5))),int(round(PH+P*(i+.5)))
    out[j,i]=np.median(a[cy-1:cy+2,cx-1:cx+2].reshape(-1,3),0)
m=out.min(2)<225; yy,xx=np.where(m); print('natief',n,'bbox',xx.min(),xx.max(),yy.min(),yy.max(),'w',xx.max()-xx.min()+1,'h',yy.max()-yy.min()+1)
Image.fromarray(out).save('natief.png'); Image.fromarray(out).resize((n*5,n*5),Image.NEAREST).save('natief_5x.png')
