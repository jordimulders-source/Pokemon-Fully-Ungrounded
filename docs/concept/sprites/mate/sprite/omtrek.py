# Per spriterij: linker/rechter rand van het model (subpixel, uit het 1024-model) naast de sprite-rand. Gebruik: omtrek.py sprite y0 y1
import sys,numpy as np; from PIL import Image
M=np.asarray(Image.open('../referenties/model.png').convert('RGB')).astype(int); fg=M.min(2)<200
S=np.asarray(Image.open(sys.argv[1]))
o=np.load('r1/kaal.npy'); yy,xx=np.where(o>0); oy0,ox0=yy.min(),xx.min(); hh=yy.max()-oy0+1; ww=xx.max()-ox0+1
top=63-hh; fx=(64-ww)//2; s=1.75; NY0,NX0=8+0.4,16+0.6
def m2s_x(mx): return ((mx+1)/10.24-NX0)/s+fx-ox0
def s2m_y(sy): return ((NY0+(sy-top+oy0)*s)*10.24-1.0)
for sy in range(int(sys.argv[2]),int(sys.argv[3])+1):
    ys=[int(s2m_y(sy+f)) for f in (0.25,0.5,0.75)]
    L=[];R=[]
    for y in ys:
        xs=np.where(fg[y])[0]
        # grootste aaneengesloten stuk (lijf), geen losse delen
        L.append(m2s_x(xs.min())); R.append(m2s_x(xs.max()+1))
    xs=np.where(S[sy]>0)[0]
    print(sy,'model L %.1f R %.1f'%(np.mean(L),np.mean(R)),' sprite L %d R %d'%(xs.min(),xs.max()+1) if len(xs) else '')
