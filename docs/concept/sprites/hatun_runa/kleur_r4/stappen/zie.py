# zie.py X0 Y0 X1 Y1 z out raster : sprite | model, beide met raster
import sys
from tl import *
X0,Y0,X1,Y1,z=map(int,sys.argv[1:6])
a=grid(rimg(sys.argv[7],P+'kleur_r4/normal.pal').crop((X0,Y0,X1,Y1)).resize(((X1-X0)*z,(Y1-Y0)*z),Image.NEAREST),X0,Y0,z)
b=grid(model(X0,Y0,X1,Y1,z),X0,Y0,z)
naast([a,b],sys.argv[6])
