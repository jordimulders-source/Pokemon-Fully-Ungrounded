# Meetgereedschap eindkeuring gaucho-Ludicolo: modelkleur/-helderheid per spritepixel (MC/ML).
# De kale reductie (../sprite/r1/kaal_vlak.py) is een vlakstemming: spritepixel (x,y) = cel (j,i) van het natieve model
# (figuur 75x91 in ../sprite/r1/kwant.npy / natief.png, 0,68x naar 51x62, geplaatst op X0=6, Y0=1).
# MC = oppervlakte-gewogen gemiddelde modelkleur (figuurpixels) in die cel; ML = helderheid daarvan. Alleen meten, niet tekenen.
import os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R1=os.path.join(H,'..','sprite','r1')
q=np.load(os.path.join(R1,'kwant.npy')); nat=np.asarray(Image.open(os.path.join(R1,'natief.png')).convert('RGB')).astype(float)
ys,xs=np.where(q>0); Y,X=ys.min(),xs.min(); f=q[Y:ys.max()+1,X:xs.max()+1]; n=nat[Y:ys.max()+1,X:xs.max()+1]
Hh,W=f.shape; TW,TH=51,62; X0,Y0=6,1
MC=np.zeros((64,64,3)); MK=np.zeros((64,64),int)
for j in range(TH):
    y0,y1=j*Hh/TH,(j+1)*Hh/TH
    for i in range(TW):
        x0,x1=i*W/TW,(i+1)*W/TW; s=np.zeros(3); A=0; w={}
        for yy in range(int(y0),int(np.ceil(y1))):
            hy=min(y1,yy+1)-max(y0,yy)
            for xx in range(int(x0),int(np.ceil(x1))):
                hx=min(x1,xx+1)-max(x0,xx); k=f[yy,xx]
                if k>0: s+=n[yy,xx]*hx*hy; A+=hx*hy; w[k]=w.get(k,0)+hx*hy
        if A: MC[Y0+j,X0+i]=s/A; MK[Y0+j,X0+i]=max(w,key=w.get)
ML=MC@[0.299,0.587,0.114]
def lum(c): return 0.299*c[0]+0.587*c[1]+0.114*c[2]
BASIS=os.path.join(R1,'ludicolo_gaucho_0.png')
if __name__=='__main__':
    im=Image.open(BASIS); a=np.array(im); pal=im.getpalette()
    for i in range(1,16):
        m=a==i
        if m.sum(): v=ML[m]; print(i,pal[3*i:3*i+3],'L=%.0f'%lum(pal[3*i:3*i+3]),'n=%d ML gem %.0f p15 %.0f p85 %.0f'%(m.sum(),v.mean(),np.percentile(v,15),np.percentile(v,85)))
