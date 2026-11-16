# Projectie natief.png -> spriteraster (koeienvanger: model 1 rij hoger, trein 2 px rechts, 0,744x), zoals sprite_r16/eind_moet.py foot().
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
F=0.744
N=np.array(Image.open(D+'model/natief.png').convert('RGB')).astype(float)
LUM=0.3*N[...,0]+0.59*N[...,1]+0.11*N[...,2]
def s2n(X,Y,DY=-1): return 9+(X-2)/F, 6+(Y-2-DY)/F
def n2s(nx,ny,DY=-1): return 2+(nx-9)*F, 2+DY+(ny-6)*F
