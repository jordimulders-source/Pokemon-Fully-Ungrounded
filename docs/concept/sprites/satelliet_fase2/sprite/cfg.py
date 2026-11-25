# r5: model en spriteraster als parameters. Model via omgevingsvariabele SAT_MODEL (standaard ../model.png).
# Alle in r1-r4 gemeten spritecoordinaten zijn op het oude raster (X0=46, Y0=143, s=14,5625 op model.png) gemeten. Lijf, oog en
# antennes staan in de paneelvarianten pixel voor pixel op dezelfde modelplek, dus T() rekent die metingen exact om naar het nieuwe raster.
import os, numpy as np
from PIL import Image
MODEL=os.environ.get('SAT_MODEL','../model.png')
OX0,OY0,OS=46,143,(978-46)/64
_a=np.asarray(Image.open(MODEL).convert('RGB'))
_fg=_a.min(2)<235; _ys,_xs=np.where(_fg)
X0,X1,Y0,Y1=int(_xs.min()),int(_xs.max())+1,int(_ys.min()),int(_ys.max())+1
W=64; s=max((X1-X0)/64,(Y1-Y0)/64); H=int(np.ceil((Y1-Y0)/s))
TOP=7 if MODEL.endswith('/model.png') else (64-H)//2      # r1-r4: 7 px boven; r5: verticaal gecentreerd
F=OS/s                                                     # vergroting t.o.v. r1-r4
def T(x,y):  # oude spritecoordinaat -> nieuwe
    return ((OX0+x*OS-X0)/s,(OY0+y*OS-Y0)/s)
def M(x,y):  # nieuwe spritecoordinaat -> model
    return (X0+x*s,Y0+y*s)
def blok(j,i):
    return int(round(Y0+j*s)),int(round(Y0+(j+1)*s)),int(round(X0+i*s)),int(round(X0+(i+1)*s))
# oogmidden (pixelhoek) en buitenstraal van de witte ring, zoals oog.py ze gebruikt
EYE=(20,24,6.3) if MODEL.endswith('/model.png') else (round((340-X0)/s),round((492.5-Y0)/s),7.0)
def oudrij(y): return int(round(T(0,y)[1]))
def oudkol(x): return int(round(T(x,0)[0]))
