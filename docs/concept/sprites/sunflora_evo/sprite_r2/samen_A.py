# Variant A: r1-hoofd exact + Sunflora-lijf op 1x, alleen knippen/verschuiven/draaien (rot90). Niets getekend.
# Lagen (achter -> voor): voeten, romp (armen+lijfje), hoofd.
# Hangvoeten: Sunflora-rechtervoet 90 graden rechtsom (steel boven-rechts) hangt links,
#             Sunflora-linkervoet 90 graden linksom (steel boven-links) hangt rechts.
import sys, numpy as np; from PIL import Image; from pal import PAL
RY,RX=int(sys.argv[1]),int(sys.argv[2])     # positie romp (bovenrij, linkerkolom)
FY=int(sys.argv[3]); OUT=sys.argv[4]; SP=int(sys.argv[5]) if len(sys.argv)>5 else 0   # voeten SP px naar buiten
kop=np.load('kop_r1.npy'); romp=np.load('romp.npy')
trim=lambda a: a[np.any(a,1)][:,np.any(a,0)]
lvoet=trim(np.rot90(np.load('rv.npy'),-1)); rvoet=trim(np.rot90(np.load('lv.npy'),1))
C=np.zeros((64,64),'uint8'); bron={}
def leg(a,y,x,naam):
    for j in range(a.shape[0]):
        for i in range(a.shape[1]):
            if a[j,i] and 0<=y+j<64 and 0<=x+i<64: C[y+j,x+i]=a[j,i]
            elif a[j,i]: bron.setdefault(naam+' valt buiten 64x64',[]).append((y+j,x+i))
cx=RX+18          # lijfjesmidden (Sunflora kol 30)
leg(lvoet,FY,cx-lvoet.shape[1]-SP,'linkervoet'); leg(rvoet,FY,cx+1+SP,'rechtervoet')
leg(romp,RY,RX,'romp')
C=np.where(kop>0,kop,C)
for k,v in bron.items(): print(k,len(v),'px')
np.save(OUT+'.npy',C)
im=Image.fromarray(C,'P'); im.putpalette([v for c in PAL for v in c]); im.save(OUT+'.png',transparency=0)
Image.open(OUT+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(OUT+'_8x.png')
