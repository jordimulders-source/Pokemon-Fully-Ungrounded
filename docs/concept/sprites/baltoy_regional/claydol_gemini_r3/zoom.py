import sys,numpy as np; from PIL import Image
from bouw import rgb, S
from kaal3 import kaal
S0,A,*_=kaal()
def zoom(y0,y1,x0,x1,s=12,pad=None):
    a=rgb(S[y0:y1,x0:x1],(200,220,200)).resize(((x1-x0)*s,(y1-y0)*s),0)
    m=Image.fromarray(A[y0:y1,x0:x1].astype('uint8')).resize(a.size,0)
    c=Image.new('RGB',(a.width*2+10,a.height),'white'); c.paste(a,(0,0)); c.paste(m,(a.width+10,0))
    if pad: c.save(pad)
    return c
if __name__=='__main__':
    y0,y1,x0,x1=map(int,sys.argv[1:5]); zoom(y0,y1,x0,x1,int(sys.argv[5]),sys.argv[6])
