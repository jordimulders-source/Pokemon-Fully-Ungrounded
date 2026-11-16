# Gedeelde functies r2: een zone opnieuw uit het model bemonsteren met een andere fase van het natieve raster (niets getekend).
import json; import numpy as np; from PIL import Image
F=1.5; X0,Y0=11,21                       # natieve linkerboven van het silhouet; sprite (i,j) <-> natief X0+(i-1)*F, Y0+(j-17)*F
P=json.load(open('kaal_palet.json')); COLS=np.array(P['cols'],float); GRP=P['grp']['0']
a=np.asarray(Image.open('model_natief.png').convert('RGBA')).astype(float)
AL=a[...,3]>0; RGB=a[...,:3]; LUM=RGB@[.299,.587,.114]
ZW=AL&(RGB.max(2)<70)                                  # zwarte modellijn
LAB=np.load('label_natief.npy')
D9=AL&~ZW&(LAB==0)&(LUM<80)                            # donkere oudroze binnenlijn
LIP=AL&~ZW&(LAB==0)&((RGB[...,0]-RGB[...,1])>=65)&(LUM>110)   # lipkleur (verzadigd roze)
def feat(X): X=np.atleast_2d(X); return np.c_[X@[.299,.587,.114], 2.0*(X[:,0]-X[:,1]), 2.0*(X[:,2]-X[:,1])]
def dichtst(c,kand): kand=list(kand); return kand[int(np.argmin(((feat(COLS[kand])-feat(c))**2).sum(1)))]
def cellen(i,j,phx,phy):
    sx,sy=X0+(i-1)*F+phx,Y0+(j-17)*F+phy
    for y in range(int(np.floor(sy)),int(np.ceil(sy+F))):
        for x in range(int(np.floor(sx)),int(np.ceil(sx+F))):
            w=max(0,min(sx+F,x+1)-max(sx,x))*max(0,min(sy+F,y+1)-max(sy,y))
            if w>0 and 0<=y<a.shape[0] and 0<=x<a.shape[1]: yield y,x,w
def lijnkaart(mask,phx,phy):
    M=set()
    for y,x in zip(*np.where(mask)):
        M.add((int((y+0.5-Y0-phy)//F)+17,int((x+0.5-X0-phx)//F)+1))
    return M
def bemonster(i,j,phx,phy,LZ,L9,lipregel=False,T=0.4):
    tw=0; zw=0; lip=0; c=np.zeros(3); cw=0; lc=np.zeros(3); lw=0
    for y,x,w in cellen(i,j,phx,phy):
        tw+=w
        if not AL[y,x]: continue
        if ZW[y,x]: zw+=w; continue
        c+=w*RGB[y,x]; cw+=w
        if LIP[y,x]: lip+=w; lc+=w*RGB[y,x]; lw+=w
    if (j,i) in LZ or zw/tw>=T: return 1
    if (j,i) in L9: return 9
    if lipregel and lip/tw>=0.4: return dichtst(lc/lw,[5,7])
    if cw==0: return 1
    return dichtst(c/cw,GRP)
def hoeken(o,zone,lijnen=(1,9),vul=None):
    n=0
    for lijn in lijnen:
        for _ in range(3):
            L=o==lijn
            for y,x in zip(*np.where(L&zone)):
                for dy in (-1,1):
                    for dx in (-1,1):
                        if L[y,x] and L[y+dy,x] and L[y,x+dx] and not L[y+dy,x+dx]:
                            L[y,x]=False; o[y,x]=vul(y,x); n+=1
    return n
def model_klein():   # model verkleind (LANCZOS) op dezelfde plek als de sprite, RGB 64x64
    m=Image.open('model_natief.png').convert('RGBA'); bb=m.getbbox(); mc=m.crop(bb)
    mv=mc.resize((round(mc.width/1.5),round(mc.height/1.5)),Image.LANCZOS)
    o=Image.new('RGBA',(64,64),(255,255,255,255)); o.alpha_composite(mv,(1,17)); return np.asarray(o).astype(float)
def opslaan(o,naam,s=8):
    im=Image.fromarray(o.astype(np.uint8),'P'); im.putpalette(sum(P['cols'],[])); im.save(naam,transparency=0)
    rgb=COLS.astype('uint8')[o]; rgb[o==0]=255; Image.fromarray(rgb).resize((64*s,64*s),Image.NEAREST).save(naam.replace('.png',f'_{s}x.png'))
def rgb(o): r=COLS.astype('uint8')[o].copy(); r[o==0]=255; return r
