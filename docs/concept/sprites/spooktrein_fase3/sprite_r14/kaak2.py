# Koeienvanger uit de onderlaag (ijskomeet-methode) in r13-coordinaten; groen bevroren; Jordi's schets alleen ter vergelijking.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r14')
from onderlaag import *
G={2,3,4,5,6,13}; IJ={1,7,8,9,10,11,12}
def kaak(r,DREMPEL=80,AANDEEL=0.3,zone=(0,25,45,59)):
    T,L,W,Gr=onderlaag(DREMPEL,AANDEEL)
    im=Image.open(D+'sprite_r13/sprite.png'); P=np.array(im.getpalette()[:14*3]).reshape(14,3)
    a=r.copy(); x0,x1,y0,y1=zone
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if a[y,x] in G: continue
            if y<=47 and x>=9: continue          # band onder de grijns rechts blijft r13
            if W[y,x]>0.5 or Gr[y,x]>0.5: a[y,x]=0 if (W[y,x]>0.5 and r[y,x]==0 or W[y,x]>0.6) else a[y,x]; continue
            a[y,x]=1 if L[y,x] and lum(T[y,x])<60 else kwant(T[y,x],P,[1,7,8,9,10,11,12])
    # buitenlijn: ijzer naast transparant zwart, behalve linksboven (lichtkant: donkere roest)
    b=a.copy()
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if a[y,x] in IJ and a[y,x]!=1:
                for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                    Y,X=y+dy,x+dx
                    if 0<=Y<64 and 0<=X<64 and a[Y,X]==0: b[y,x]=9 if (dx==-1 and y<52) else 1; break
    return b
