# Monocle-ring van het rechteroog uit het model (natief, zwarte ring rond (104,63)), verkleind met factor F
# rond het oogmidden (39,18) in de sprite. F=2.5 = zelfde schaal als de rest; F=2.0 = net groot genoeg voor het Rime-oog.
import numpy as np; from PIL import Image
def ring(F=2.0, cx=104, cy=63, sx=39, sy=18, thr=1.5):
    a=np.asarray(Image.open('natief_stok.png').convert('L')).astype(int)
    cnt={}
    for y in range(cy-10,cy+11):
        for x in range(cx-10,cx+11):
            d=((x-cx)**2+(y-cy)**2)**.5
            if a[y,x]<60 and 5<=d<=8.6:
                k=(int(np.floor(sy+(y-cy)/F+0.5)), int(np.floor(sx+(x-cx)/F+0.5)))
                cnt[k]=cnt.get(k,0)+1
    return sorted(k for k,v in cnt.items() if v>=thr)
if __name__=='__main__':
    for F in (2.5,2.0):
        r=ring(F); ys=[k[0] for k in r]; xs=[k[1] for k in r]
        print(F,len(r))
        for y in range(min(ys),max(ys)+1): print(''.join('#' if (y,x) in r else '.' for x in range(min(xs),max(xs)+1)), y)
