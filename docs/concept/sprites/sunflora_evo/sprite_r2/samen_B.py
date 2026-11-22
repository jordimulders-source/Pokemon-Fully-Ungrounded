# Variant B: r1-hoofd exact + Sunflora-lijf exact 2x verkleind met een vaste 2x2-regel, geen handreparaties.
# Regel per 2x2-blok: <2 gevulde pixels -> leeg; >=2 lijnpixels (zwart 1 / donkergroen b) -> lijn wint
# (zwart als er zwart in zit, anders b); anders de meest voorkomende vulkleur (bij gelijkspel de lichtste).
# Delen eerst draaien zoals in A (hele pixels), dan verkleinen, dan verschuiven.
import sys, numpy as np; from PIL import Image; from pal import PAL
RY,RX,FY,SP=map(int,sys.argv[1:5]); OUT=sys.argv[5]
def half(a):
    h,w=(a.shape[0]+1)//2,(a.shape[1]+1)//2; a=np.pad(a,((0,2*h-a.shape[0]),(0,2*w-a.shape[1]))); o=np.zeros((h,w),'uint8')
    for j in range(h):
        for i in range(w):
            b=a[2*j:2*j+2,2*i:2*i+2].ravel(); f=b[b>0]
            if len(f)<2: continue
            d=f[np.isin(f,[1,11])]
            if len(d)>=2: o[j,i]=1 if (d==1).any() else 11; continue
            v=f[~np.isin(f,[1,11])]; u,c=np.unique(v,return_counts=True); o[j,i]=u[c==c.max()].max()
    return o
trim=lambda a: a[np.any(a,1)][:,np.any(a,0)]
kop=np.load('kop_r1.npy'); romp=half(np.load('romp.npy'))
lvoet=trim(half(trim(np.rot90(np.load('rv.npy'),-1)))); rvoet=trim(half(trim(np.rot90(np.load('lv.npy'),1))))
C=np.zeros((64,64),'uint8')
def leg(a,y,x):
    for j in range(a.shape[0]):
        for i in range(a.shape[1]):
            if a[j,i] and 0<=y+j<64 and 0<=x+i<64: C[y+j,x+i]=a[j,i]
cx=RX+9
leg(lvoet,FY,cx-lvoet.shape[1]-SP); leg(rvoet,FY,cx+1+SP); leg(romp,RY,RX)
C=np.where(kop>0,kop,C); np.save(OUT+'.npy',C)
im=Image.fromarray(C,'P'); im.putpalette([v for c in PAL for v in c]); im.save(OUT+'.png',transparency=0)
Image.open(OUT+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(OUT+'_8x.png')
ch='.123456789abcdef'
for nm,a in (('romp/2',romp),('voet L/2',lvoet),('voet R/2',rvoet)): print(nm); [print(''.join(ch[v] for v in r)) for r in a]
