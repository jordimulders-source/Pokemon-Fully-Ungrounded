# Kale reductie v2: exact 3x3 natieve pixels per spritepixel, kleuren = 15 kleuren uit het model (k-means-centra van natief.png).
# Lijnregel: >=2 pixels lum<LINE in het blok -> omlijning (ijskomeet-les); oogzwart als de donkerste < 30.
# Anders: gemiddelde van de dekkende pixels -> dichtstbijzijnde vlakkleur.
import sys; from PIL import Image; import numpy as np
H=lambda s: np.array([int(s[i:i+2],16) for i in (0,2,4)])
PALHEX=['000000','4a0f25','240b10','821b48','be307a','ec3175','f076a8','f598be','d0269a','9a2662','f8e080','dca695','f7e2d9','e6cdac','b6895e','ffffff']
PAL=np.array([H(h) for h in PALHEX])
n=np.asarray(Image.open('natief.png')).astype(int)
lum=(0.3*n[...,0]+0.59*n[...,1]+0.11*n[...,2])
def reduce(px=1,py=1,ALPHA=4,LINE=48,OPQ=225):
    opq=n.min(2)<OPQ
    x0=77-px; y0=15-py; W=(146-x0)//3+1; Hh=(163-y0)//3+1
    out=np.zeros((Hh,W),'uint8')
    for j in range(Hh):
        for i in range(W):
            sl=(slice(y0+3*j,y0+3*j+3),slice(x0+3*i,x0+3*i+3))
            b=n[sl]; o=opq[sl]; L=lum[sl]
            if o.sum()<ALPHA: continue
            dk=(L<LINE)&o
            if dk.sum()>=2:
                out[j,i]=2 if L[dk].min()<30 else 1
            else:
                m=b[o].mean(0); d=((PAL[3:15]-m)**2).sum(1); out[j,i]=3+d.argmin()
    return out
def save(idx,path):
    im=Image.fromarray(idx,'P'); pal=PAL.flatten().tolist(); im.putpalette(pal+[0]*(768-len(pal))); im.save(path,transparency=0); return im
if __name__=='__main__':
    px,py=int(sys.argv[1]),int(sys.argv[2]); a=reduce(px,py); np.save('kaal.npy',a); save(a,'kaal.png'); print(a.shape)
