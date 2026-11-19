# Kale reductie natief -> sprite, exact 3x3 natieve pixels per spritepixel.
# Regels: dekking >= ALPHA van 9; >=2 lijnpixels (lum<72) in blok -> donkerste lijnkleur (ijskomeet-les: dunne lijnen blijven);
# anders gemiddelde van de dekkende pixels -> dichtstbijzijnde kleur uit het model (natieve kleuren met >=3 pixels).
import sys; from PIL import Image; import numpy as np
n=np.asarray(Image.open('natief.png')).astype(int)
lum=(0.3*n[...,0]+0.59*n[...,1]+0.11*n[...,2])
opq=n.min(2)<228
cols,cnt=np.unique(n[opq].reshape(-1,3),axis=0,return_counts=True)
PAL=cols[cnt>=3]
def reduce(px,py,ALPHA=4,LINE=72):
    x0=77-px; y0=15-py
    W=(146-x0)//3+1; H=(163-y0)//3+1
    out=np.zeros((H,W,4),'uint8')
    for j in range(H):
        for i in range(W):
            b=n[y0+3*j:y0+3*j+3, x0+3*i:x0+3*i+3]; o=opq[y0+3*j:y0+3*j+3, x0+3*i:x0+3*i+3]; L=lum[y0+3*j:y0+3*j+3, x0+3*i:x0+3*i+3]
            if o.sum()<ALPHA: continue
            dk=(L<LINE)&o
            if dk.sum()>=2:
                c=b[dk][np.argmin(L[dk])]
            else:
                m=b[o].mean(0); c=PAL[((PAL-m)**2).sum(1).argmin()]
            out[j,i,:3]=c; out[j,i,3]=255
    return out
if __name__=='__main__':
    px,py=int(sys.argv[1]),int(sys.argv[2])
    o=reduce(px,py); Image.fromarray(o).save('kaal_%d%d.png'%(px,py)); print(o.shape)
