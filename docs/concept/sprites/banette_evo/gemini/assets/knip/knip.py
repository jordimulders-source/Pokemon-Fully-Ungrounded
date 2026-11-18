# Jordi's werkwijze: hoofd langs zijn gele lijn knippen en 1,8x schalen; armen los van de kruizen
# en zo draaien/schalen dat ze van het kruis naar de zijkant van het hoofd (mondhoogte) lopen.
import sys; from PIL import Image, ImageDraw; import numpy as np
S=float(sys.argv[3]); DY=int(sys.argv[4]); INSET=float(sys.argv[1]); OUT=sys.argv[2]
B=Image.open('../hoofdarmen_groter/bron.png').convert('RGB'); a=np.asarray(B).astype(int); nw=a.min(2)<235
ov=lambda pts:[(150+x/2,180+y/2) for x,y in pts]            # overlay.png -> bron
dp=lambda pts:[(x*0.512,150+y*0.512) for x,y in pts]       # bron_grid (weergave) -> bron
head_poly=ov([(480,108),(600,185),(800,50),(920,70),(1000,140),(1104,265),(1104,380),(1000,380),(930,360),(930,540),(900,640),(880,760),(910,990),(640,990),(570,820),(530,765),(420,680),(370,580),(370,500),(330,500),(300,550),(340,560),(345,610),(320,650),(260,660),(215,620),(220,565),(255,545),(260,450),(305,390),(312,300),(320,200),(380,140)])
armL=dp([(440,100),(560,230),(600,330),(640,480),(620,560),(530,590),(490,470),(450,380),(430,300),(430,180)])
armR=dp([(1180,770),(1170,600),(1290,560),(1380,420),(1400,250),(1480,90),(1545,85),(1545,400),(1500,480),(1440,600),(1320,710)])
def mask(poly):
    m=Image.new('L',B.size,0); ImageDraw.Draw(m).polygon(poly,fill=255); return (np.asarray(m)>0)
mh=mask(head_poly)&nw; mL=mask(armL)&nw&~mh; mR=mask(armR)&nw&~mh
bg=a.copy(); bg[mh|mL|mR]=255
out=Image.fromarray(bg.astype('uint8'))
# hoofd schalen
ys,xs=np.where(mh); bb=(xs.min(),ys.min(),xs.max()+1,ys.max()+1); cx=(bb[0]+bb[2])/2; cy=(bb[1]+bb[3])/2
def T(x,y): return (cx+(x-cx)*S, cy+(y-cy)*S+DY)
hm=Image.fromarray((mh*255).astype('uint8')).crop(bb); hd=B.crop(bb)
W,H=int(hd.width*S),int(hd.height*S); hd=hd.resize((W,H),Image.NEAREST); hm=hm.resize((W,H),Image.NEAREST)
hx,hy=int(cx-W/2),int(cy-H/2)+DY
big=np.zeros(B.size[::-1],bool); big[hy:hy+H,hx:hx+W]=np.asarray(hm)>0
# mondhoogte (bron y~467) na schalen; rand van het hoofd op die rij
my=int(T(0,467)[1]); row=np.where(big[my])[0]; rx=row.max()
fx=T(340,467)[0]  # linkerrand gezicht op mondhoogte (bron x~340, binnen Jordi's lijn)
lx=fx
def place(m,tip,base,newbase):
    t=np.array(tip,float); b=np.array(base,float); nb=np.array(newbase,float)
    v0=b-t; v1=nb-t; s=np.linalg.norm(v1)/np.linalg.norm(v0); ang=np.arctan2(v1[1],v1[0])-np.arctan2(v0[1],v0[0])
    c,sn=np.cos(ang)*s,np.sin(ang)*s
    # inverse map: voor elke doelpixel p: src = t + R^-1 (p-t)/... 
    inv=np.array([[c,sn],[-sn,c]])/(s*s)
    H_,W_=m.shape; yy,xx=np.mgrid[0:H_,0:W_]
    px=xx-t[0]; py=yy-t[1]
    sx=t[0]+inv[0,0]*px+inv[0,1]*py; sy=t[1]+inv[1,0]*px+inv[1,1]*py
    sxi=np.round(sx).astype(int); syi=np.round(sy).astype(int)
    ok=(sxi>=0)&(sxi<W_)&(syi>=0)&(syi<H_)
    sel=np.zeros_like(m); sel[ok]=m[syi[ok],sxi[ok]]
    o=np.asarray(out).copy(); o[sel]=a[syi[sel],sxi[sel]]; return Image.fromarray(o.astype('uint8')), s
out,sL=place(mL,(230,252),(292,416),(lx+INSET,my))
out,sR=place(mR,(768,227),(625,508),(rx-INSET,my))
out.paste(hd,(hx,hy),hm)
out.save(OUT); print('schaal armen',round(sL,2),round(sR,2),'mondrij',my,lx,rx)
