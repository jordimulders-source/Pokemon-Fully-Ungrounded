# polar.py: slagpennen waaieren uit vanaf C; per hoek het gemiddelde modellicht langs de straal (r 7..24 spritepx)
# -> minima = donkere scheidingen tussen pennen, maxima = lichte schachten. Uitvoer: hoeken in graden (0 = rechts, -90 = omhoog)
import numpy as np; from PIL import Image
from geom import model_box
m=np.asarray(Image.open('../../MODEL.png').convert('RGB')).astype(float); L=m@[.299,.587,.114]; bg=m.min(2)>225
C=(33.0,23.0)
def mp(sx,sy):
    a,b,c,d=model_box(sx,sy,sx+1,sy+1); return a,b   # modelcoord van spritepunt (sx,sy) (continu)
def prof(r0=7,r1=24,ths=np.arange(-80,8,0.5)):
    out=[]
    for th in ths:
        t=np.radians(th); vals=[]
        for r in np.arange(r0,r1,0.1):
            sx=C[0]+r*np.cos(t); sy=C[1]+r*np.sin(t); mx,my=mp(sx,sy); ix,iy=int(mx),int(my)
            if 0<=ix<1024 and 0<=iy<1024 and not bg[iy,ix]: vals.append(L[iy,ix])
        out.append((th,np.mean(vals) if len(vals)>20 else np.nan, np.mean(np.array(vals)<45) if vals else 0, np.mean(np.array(vals)>140) if vals else 0))
    return out
if __name__=='__main__':
    for th,mean,dk,lt in prof():
        print('%6.1f %6.1f dark %.2f light %.2f %s %s'%(th,mean,dk,lt,'#'*int(dk*40),'+'*int(lt*40)))
