# Model (natief) op spriteschaal 0,744 (BOX) en uitlijning tegen r9-ijzer zoeken.
from PIL import Image; import numpy as np
n=Image.open('model/natief.png').convert('RGB')
def schaal(f=0.744):
    c=n.crop((9,6,95,89)); return c.resize((round(86*f),round(83*f)),Image.BOX)
a=np.array(Image.open('sprite_r9/sprite.png'))
IJ=np.isin(a,[1,7,8,9,10,11,12])
def ijzer(m):
    m=m.astype(int); return (m.sum(2)<600)&~(m[...,1]>m[...,0]+20)
if __name__=='__main__':
    best=[]
    for f in [0.72,0.744,0.76,0.78]:
        s=np.array(schaal(f)); h,w=s.shape[:2]
        for dy in range(-4,6):
            for dx in range(-4,4):
                M=np.zeros((64,64),bool)
                for y in range(h):
                    for x in range(w):
                        Y,X=y+dy,x+dx
                        if 0<=Y<64 and 0<=X<64: M[Y,X]=ijzer(s[y:y+1,x:x+1])[0,0]
                iou=(M&IJ).sum()/(M|IJ).sum(); best.append((iou,f,dx,dy))
    best.sort(); print(best[-5:])
def model64():
    s=schaal(0.744); b=Image.new('RGB',(64,64),(255,255,255)); b.paste(s,(0,2)); return b
