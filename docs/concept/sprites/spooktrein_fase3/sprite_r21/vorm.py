# Vormvergelijking koeienvanger: modelijzer (natief.png, niet wit/groen, >=50% van de voetafdruk) vs sprite-ijzer.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from kv import *
GRS=[2,3,4,5,6,13]
def Fr(M,x,y):
    f=list(foot(x,y)); W=sum(w for w,_,_ in f); return sum(w for w,ny,nx in f if M[ny,nx])/W
IJ=~G&~WIT
MI=np.zeros((64,64),bool); MG=np.zeros((64,64),bool)
for y in range(40,64):
    for x in range(0,40):
        fi=Fr(IJ,x,y); fg=Fr(G,x,y); MI[y,x]=fi>=0.5; MG[y,x]=fg>0.5
def kaart(p,y0=42,y1=62,x0=0,x1=36):
    r=np.array(Image.open(p)).astype(int); SI=(r!=0)&~np.isin(r,GRS)
    for y in range(y0,y1):
        s=''
        for x in range(x0,x1):
            m,sp=MI[y,x],SI[y,x]
            s+= ('=' if m and sp else '+' if sp else '-' if m else ('g' if np.isin(r[y,x],GRS) else '.'))
        print('%2d %s'%(y,s))
    return r,SI
if __name__=='__main__':
    print("= beide ijzer, + alleen sprite (extra), - alleen model (ontbreekt), g groen sprite")
    kaart(sys.argv[1])
