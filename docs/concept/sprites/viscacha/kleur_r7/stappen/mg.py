# mg.py X0 Y0 X1 Y1 z out : model met raster en coordinaten
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r7/stappen')
from tl import *
x0,y0,x1,y1,z=map(int,sys.argv[1:6]); grid(model(x0,y0,x1,y1,z),x0,y0,z).save(sys.argv[6])
