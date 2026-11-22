# Eigen klassen op het natieve raster (r10/natief.png): 0 leeg, 1 lijn, 2 huid (roze), 3 huls (beige/creme/geel/oker), 4 streep (magenta)
import numpy as np; from PIL import Image
n=np.asarray(Image.open('../r10/natief.png').convert('RGB')).astype(int)
R,G,B=n[...,0],n[...,1],n[...,2]; lum=.3*R+.59*G+.11*B
k=np.zeros(R.shape,int)
bg=n.min(2)>=236
line=lum<105
beige=(G>=0.68*R)&(B<=G+12)          # huls: perzik/creme/geel
mag=(R<235)&(B>=0.55*R)&(G<0.35*R)   # magentastreep
k[:]=2; k[beige]=3; k[mag&~beige]=4; k[line]=1; k[bg]=0
np.save('klas.npy',k)
F,OX,OY=2.4,76.6,14.6
def cov(r,c):
    j,i=r-1,c-17; x0,x1=OX+i*F,OX+(i+1)*F; y0,y1=OY+j*F,OY+(j+1)*F; w=np.zeros(5)
    for yy in range(int(np.floor(y0)),int(np.ceil(y1))):
        wy=min(y1,yy+1)-max(y0,yy)
        for xx in range(int(np.floor(x0)),int(np.ceil(x1))):
            wx=min(x1,xx+1)-max(x0,xx)
            if wx>0 and wy>0: w[k[yy,xx]]+=wx*wy
    return w/w.sum()
if __name__=='__main__':
    import sys
    r0,r1,c0,c1=map(int,sys.argv[1:5])
    for nm,ix in (('lijn',1),('huid',2),('huls',3),('streep',4),('leeg',0)):
        print('==',nm); print('     '+''.join('%4d'%c for c in range(c0,c1)))
        for r in range(r0,r1): print('%3d  '%r+''.join('%4d'%round(100*cov(r,c)[ix]) for c in range(c0,c1)))
    # dominante klasse
    print('== dominant (. lijn# huid h huls k streep M)')
    for r in range(r0,r1):
        print('%3d  '%r+''.join('.#hkM'[cov(r,c).argmax()] for c in range(c0,c1)))
    col=np.array([[255,255,255],[60,0,30],[240,110,160],[230,200,160],[200,40,160]],'uint8')
    Image.fromarray(col[k]).resize((800,800),Image.NEAREST).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/86835790-8242-560c-8a0b-487fe7ec68a2/scratchpad/klas.png')
