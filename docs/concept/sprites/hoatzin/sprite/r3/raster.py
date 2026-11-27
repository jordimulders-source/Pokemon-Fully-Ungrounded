# hulp: modeluitsnede met het spriteraster erover (spritecoordinaten als labels); optioneel sprite-omtrek
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from PIL import ImageDraw
def raster(X0,Y0,X1,Y1,f=3,o=None):
    im=Image.open(MODEL).convert('RGB')
    x0,_,y0,_=cel(X0,Y0); x1,_,y1,_=cel(X1,Y1)
    c=im.crop((int(x0),int(y0),int(x1),int(y1))).resize((int((x1-x0)*f),int((y1-y0)*f)),0)
    d=ImageDraw.Draw(c)
    for X in range(X0,X1+1):
        xx=(cel(X,0)[0]-int(x0))*f; d.line([(xx,0),(xx,c.height)],fill=(255,0,255) if X%5==0 else (255,160,255))
    for Yy in range(Y0,Y1+1):
        yy=(cel(0,Yy)[2]-int(y0))*f; d.line([(0,yy),(c.width,yy)],fill=(255,0,255) if Yy%5==0 else (255,160,255))
    for X in range(X0,X1,5): d.text(((cel(X,0)[0]-int(x0))*f+2,2),str(X),fill=(255,0,0))
    for Yy in range(Y0,Y1,5): d.text((2,(cel(0,Yy)[2]-int(y0))*f+2),str(Yy),fill=(255,0,0))
    return c
if __name__=='__main__':
    X0,Y0,X1,Y1=[int(v) for v in sys.argv[2].split(',')]; f=float(sys.argv[3]) if len(sys.argv)>3 else 3
    raster(X0,Y0,X1,Y1,f).save(sys.argv[1])
