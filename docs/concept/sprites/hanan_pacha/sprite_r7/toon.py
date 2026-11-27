import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'.'); from model_zegt import model, ZONES
PAL=[(152,208,160),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),
 (128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def rgb(o,bg=(240,240,236)):
    a=np.array(PAL,'uint8')[o]; a[o==0]=bg; return Image.fromarray(a)
def modelkaart(o):
    m=o.copy()
    for x0,x1,y0,y1 in ZONES:
        for Y in range(y0,y1+1):
            for X in range(x0,x1+1):
                k,t=model(X,Y)
                if o[Y,X]==0 or k=='.': continue
                m[Y,X]={'L':1,'K':7,'T':t}[k]
    return m
