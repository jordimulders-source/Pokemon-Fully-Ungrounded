# schaal.py: r9 (model + alle goedgekeurde bovenlagen r1-r9) op dezelfde natieve schaal als de kale 52-reductie leggen
# r9-pixel (c,r) dekt natief-uitsnede x=(c-10)*1.397.., y=r*1.397..; nieuwe pixel (i,j) dekt i*1.6923..; k = 1.6923/1.397
import numpy as np, sys
OH=int(sys.argv[1]) if len(sys.argv)>1 else 52
r9=np.load('../sprite_r9/bokser.npy'); k=(88/OH)/(88/63)
OW=int(round(60/(88/OH)))
out=np.zeros((OH,OW),int)
for j in range(OH):
    for i in range(OW):
        c=np.zeros(9); x0,x1=10+i*k,10+(i+1)*k; y0,y1=j*k,(j+1)*k
        for y in range(int(y0),int(np.ceil(y1))):
            wy=min(y1,y+1)-max(y0,y)
            for x in range(int(x0),int(np.ceil(x1))):
                if 0<=y<64 and 0<=x<64: c[r9[y,x]]+=wy*(min(x1,x+1)-max(x0,x))
        c/=c.sum()
        if c[0]>=0.5: continue
        if c[1]>=0.3: out[j,i]=1; continue
        c[0]=0;c[1]=0; out[j,i]=int(np.argmax(c))
np.save(f'r9_{OH}.npy',out)
for j,r in enumerate(out): print('%2d '%j+''.join(str(v) if v else '.' for v in r))
