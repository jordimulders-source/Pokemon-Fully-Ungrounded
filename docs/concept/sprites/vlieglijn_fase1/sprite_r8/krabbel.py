# registratie krabbel (285x241) op het 64x64-raster: kleurfit tegen kandidaten; geel/rood naar spritepixels
import numpy as np; from PIL import Image
k=np.asarray(Image.open('../sprite_r7/krabbel_jordi.png').convert('RGB')).astype(float)
R,G,B=k[...,0],k[...,1],k[...,2]; geel=(R>180)&(G>160)&(B<90); rood=(R>170)&(G<80)&(B<80)
PAL=[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[3:19]]; P=np.array(PAL,float); P[0]=(255,255,255)
H,W=k.shape[:2]; yy,xx=np.mgrid[0:H,0:W]; m=~geel&~rood
kand={'r7_A':'../sprite_r7/vlieg_r7_A.txt','r7_B':'../sprite_r7/vlieg_r7_B.txt','r5 B':'../sprite_r5/vlieg_r5_B.txt','r9 natief':'../sprite_r6/r9_nat_idx.txt'}
for n,p in kand.items():
    img=P[np.loadtxt(p,dtype=int)]; best=(9e9,)
    for s in np.arange(4.96,5.08,0.02):
      for ox in np.arange(2.5,3.4,0.1):
        for oy in np.arange(14.5,15.4,0.1):
            sx=(xx/s+ox).astype(int); sy=(yy/s+oy).astype(int); ok=m&(sx<64)&(sy<64)&(sy>=40)
            e=np.abs(img[sy[ok],sx[ok]]-k[ok]).sum(1).mean()
            if e<best[0]: best=(e,s,ox,oy)
    print(f'{n:10s} fout {best[0]:.1f}  schaal {best[1]:.2f} offset ({best[2]:.1f},{best[3]:.1f})')
s,ox,oy=5.02,2.9,14.9
for nm,mk in (('geel',geel),('rood',rood)):
    ys,xs=np.where(mk); px={}
    for y,x in zip(ys,xs): q=(int(x/s+ox),int(y/s+oy)); px[q]=px.get(q,0)+1
    print(nm,sorted(q for q,c in px.items() if c>=3))
