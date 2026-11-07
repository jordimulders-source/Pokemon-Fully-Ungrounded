# Stap 2 (Jordi, 6 nov): "het hoofd moet iets groter, de benen net wat korter en de voeten net wat
# groter, hij moet minder op een mens en meer op een hitmon lijken, handen dus ook iets groter".
# Per lichaamsdeel op het grote masker van model v3; daarna weer naar 64x64.
# C = A + aanpassingen, D = B (gedrongen romp) + aanpassingen.
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
import silhouet as S1   # hergebruikt masker (met dichte enkel), inkorten(), los(), vel-hulpjes
KOP,HAND,VOET,BEEN=1.15,1.30,1.22,0.09   # factoren; BEEN = deel van de beenlengte eraf
M=S1.M; H,W=M.shape
a=np.asarray(S1.SRC0).astype(int)
yy,xx=np.mgrid[0:H,0:W].astype(float)
blue=(a[...,2]-a[...,0]>50)

def warp(part,fx,fy):  # fx,fy: bron-coordinaten per doelpixel
    return nd.map_coordinates(part.astype(float),[fy,fx],order=1)>0.5
def schaal(part,c,s): return warp(part,c[0]+(xx-c[0])/s,c[1]+(yy-c[1])/s)
def schuif(part,v):   return warp(part,xx-v[0],yy-v[1])
def schijf(c,r):      return (xx-c[0])**2+(yy-c[1])**2<r*r

def been(M,heup,enkel,voet,k):
    """been tussen t0 en de enkel inkorten met k px; voet (los masker) schuift k mee."""
    heup=np.array(heup,float); enkel=np.array(enkel,float)
    L=np.linalg.norm(enkel-heup); u=(enkel-heup)/L
    t=(xx-heup[0])*u[0]+(yy-heup[1])*u[1]; p=np.abs(-(xx-heup[0])*u[1]+(yy-heup[1])*u[0])
    t0=0.35*L
    zone=M&(t>t0)&(p<95)&~voet
    ts=np.where(t<t0,t,np.where(t<L-k,t0+(t-t0)*(L-t0)/(L-k-t0),t+k))
    d=ts-t
    nieuw=warp(zone,xx+d*u[0],yy+d*u[1])&(t>t0-2)
    vt=schuif(voet,-k*u)
    return (M&~zone&~voet)|nieuw, vt, -k*u

def bewerk(M):
    M=M.copy()
    # voeten (blauw + klauwen eromheen)
    Lv=M&nd.binary_dilation(blue&(xx<200)&(yy<200),iterations=30)&(xx<175)&(yy<200)
    Rv=M&nd.binary_dilation(blue&(xx>580)&(yy<230),iterations=30)&(yy<215)&(xx>595)
    # benen korter (de voet schuift mee)
    M,Lv,dl=been(M,(490,335),(145,130),Lv,BEEN*480)
    M,Rv,dr=been(M,(585,355),(668,182),Rv,BEEN*330)
    # voeten groter rond hun eigen midden (na de verschuiving)
    M|=schaal(Lv,np.array([90,110])+dl,VOET)|schaal(Rv,np.array([662,128])+dr,VOET)
    # handen groter (steunhand: onderkant blijft op de grond; vuist rond zijn midden)
    h=M&schijf((440,961),44); M|=schaal(h,(440,997),HAND)
    v=M&schijf((652,332),44); M|=schaal(v,(652,332),HAND)
    # kop groter, vanuit de nek (waar kop, romp en steunarm samenkomen)
    kop=M&(((xx<395)&(yy>540))|schijf((265,635),125))&(yy<760)&~((xx>395))
    M|=schaal(kop,(385,610),KOP)
    return nd.binary_fill_holes(M)

def naar64(M):  # opnieuw passend maken (63 hoog, horizontaal in het midden)
    ys,xs=np.nonzero(M); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    s=63/(y1-y0+1); w=(x1-x0+1)*s
    if w>62: s=62/(x1-x0+1); 
    ox=(64-(x1-x0+1)*s)/2; oy=63-(y1-y0+1)*s
    out=np.zeros((64,64))
    gx=((xs-x0)*s+ox).astype(int); gy=((ys-y0)*s+oy).astype(int)
    np.add.at(out,(gy,gx),1)
    return S1.los(out*s*s>=0.5)

Mc=bewerk(M); C=naar64(Mc); D=naar64(S1.inkorten(Mc,45))
for n,g in (('C',C),('D',D)):
    Image.fromarray((~g*255).astype('uint8')).save(f'silhouet_{n}_1x.png')
    open(f'silhouet_{n}.txt','w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in g)+'\n')
    print(n,int(g.sum()))
Image.fromarray((Mc*255).astype('uint8')).save('masker_stap2_groot.png')

# vel: model | A | C | D (8x) + 1x/2x eronder
Z=8; A=np.array([[c=='#' for c in r] for r in open('silhouet_A.txt').read().split()])
B=np.array([[c=='#' for c in r] for r in open('silhouet_B.txt').read().split()])
pan=[S1.crop,S1.raster(S1.groot(A)),S1.raster(S1.groot(C)),S1.raster(S1.groot(D))]
tit=['model v3 (bron)','A: vorige ronde (puur model)','C: A + kop/handen/voeten groter, benen korter','D: idem op B (romp gedrongener)']
V=Image.new('RGB',(4*522+10,512+40+140),'white'); d=ImageDraw.Draw(V)
for i,(p,t) in enumerate(zip(pan,tit)):
    V.paste(p,(10+i*522,30)); d.text((10+i*522,10),t,fill='black')
for i,g in enumerate((A,C,D)):
    s=Image.fromarray(np.where(g,40,255).astype('uint8'))
    V.paste(s,(10+(1+i)*522,552)); V.paste(s.resize((128,128)),(90+(1+i)*522,552))
V.save('vel_stap2.png')
