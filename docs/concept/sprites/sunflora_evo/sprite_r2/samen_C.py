# Variant C: lijf groter. r1-hoofd exact + Sunflora-lijf vergroot met een vaste regel:
# naaste-buur 1,25x = elke 4e rij en kolom verdubbeld (rijen/kolommen 1,5,9,... ; vast patroon, geen handwerk).
# Delen gedraaid zoals in A (rot90), dan vergroot, dan verschoven. Niets getekend.
import sys, numpy as np; from PIL import Image; from pal import PAL
RY,RX,FY,SP=map(int,sys.argv[1:5]); OUT=sys.argv[5]
def groter(a):
    r=[k for k in range(a.shape[0]) for _ in range(2 if k%4==1 else 1)]
    c=[k for k in range(a.shape[1]) for _ in range(2 if k%4==1 else 1)]
    return a[np.ix_(r,c)]
trim=lambda a: a[np.any(a,1)][:,np.any(a,0)]
kop=np.load('kop_r1.npy'); romp=groter(np.load('romp.npy'))
lvoet=groter(trim(np.rot90(np.load('rv.npy'),-1))); rvoet=groter(trim(np.rot90(np.load('lv.npy'),1)))
print('romp',romp.shape,'voeten',lvoet.shape,rvoet.shape)
C=np.zeros((64,64),'uint8'); weg={}
def leg(a,y,x,n):
    for j in range(a.shape[0]):
        for i in range(a.shape[1]):
            if not a[j,i]: continue
            if 0<=y+j<64 and 0<=x+i<64: C[y+j,x+i]=a[j,i]
            else: weg[n]=weg.get(n,0)+1
cx=RX+round(18*1.25)
leg(lvoet,FY,cx-lvoet.shape[1]-SP,'linkervoet'); leg(rvoet,FY,cx+1+SP,'rechtervoet'); leg(romp,RY,RX,'romp')
print('valt buiten 64x64:',weg)
C=np.where(kop>0,kop,C); np.save(OUT+'.npy',C)
im=Image.fromarray(C,'P'); im.putpalette([v for c in PAL for v in c]); im.save(OUT+'.png',transparency=0)
Image.open(OUT+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(OUT+'_8x.png')
