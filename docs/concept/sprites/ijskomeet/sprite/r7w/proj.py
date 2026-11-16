# projectie model -> spriteraster (zelfde als r6: sprite(i,j) = natief 3i+11.., 3j-4..)
import numpy as np; from PIL import Image
A=np.asarray(Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')).astype(float)
OX,OY=15,-6
cx=np.load('natief_cx.npy'); cy=np.load('natief_cy.npy'); P=5.12
def box(i,j):
    x0=cx[0]+(3*i+OX)*P-P/2; y0=cy[0]+(3*j+OY)*P-P/2
    return x0,y0,x0+3*P,y0+3*P
def model_s(s=12):
    # model hergesampled zodat 1 spritepixel = s px
    x0,y0,_,_=box(0,0); w=64*3*P
    im=Image.fromarray(A.astype('uint8')).crop((int(round(x0)),int(round(y0)),int(round(x0+w)),int(round(y0+w))))
    return im.resize((64*s,64*s),Image.BILINEAR)
