"""Kleurronde 2, stap 1: onderlaag voor het 3/4-lijf (drie windingen als tori, licht linksboven,
iets van boven bekeken). Alleen een schets-onderlaag: het raster wordt daarna met de hand bijgewerkt."""
import math, sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
PHI=math.radians(20)
L=(-0.50,0.30,0.80); n=math.sqrt(sum(v*v for v in L)); L=tuple(v/n for v in L)
# (cx, Rm, r, z0)
# (cx, Rm, r, rz, z0)
COILS=[(29.5,19.5,8.5,6.4,6.4),(29.0,13.2,8.0,6.0,16.8),(29.5,7.4,7.0,5.4,26.4)]
GY=54.0   # schermrij van de grond onder het midden
SS=4
def proj(X,Y,Z): return X, GY - Z*math.cos(PHI) + Y*math.sin(PHI), Y*math.cos(PHI)+Z*math.sin(PHI)
def render():
    zb={}
    for ci,(cx,Rm,r,rz,z0) in enumerate(COILS):
        for ia in range(1400):
            a=2*math.pi*ia/1400
            for ib in range(240):
                b=2*math.pi*ib/240
                sb=math.sin(b)
                if ci==0 and sb<0:      # onderste winding zakt uit onder zijn gewicht: brede, platte voet
                    R=Rm+r*math.cos(b)+2.2*(-sb)**1.5; Zb=z0+rz*0.78*sb
                else:
                    R=Rm+r*math.cos(b); Zb=z0+rz*sb
                X=cx+R*math.cos(a); Y=R*math.sin(a); Z=Zb
                nx,ny,nz=math.cos(b)/r*math.cos(a),math.cos(b)/r*math.sin(a),math.sin(b)/rz
                nn=math.sqrt(nx*nx+ny*ny+nz*nz); nx,ny,nz=nx/nn,ny/nn,nz/nn
                if ny*math.cos(PHI)+nz*math.sin(PHI)<-0.05: continue
                sx,sy,dep=proj(X,Y,Z)
                k=(int(sx*SS),int(sy*SS))
                if k not in zb or zb[k][0]<dep:
                    zb[k]=(dep,ci,nx*L[0]+ny*L[1]+nz*L[2],b)
        # gat van de bovenste winding: schijf (lijf loopt naar binnen)
        if ci==len(COILS)-1:
            for ix in range(-int(Rm*SS),int(Rm*SS)+1):
                for iy in range(-int(Rm*SS),int(Rm*SS)+1):
                    X=cx+ix/SS; Y=iy/SS
                    if X*0==0 and (ix/SS)**2+Y**2<=Rm**2:
                        Z=z0+rz*0.9
                        sx,sy,dep=proj(X,Y,Z); k=(int(sx*SS),int(sy*SS))
                        if k not in zb or zb[k][0]<dep: zb[k]=(dep,ci,0.75,1.4)
    px={}
    for x in range(64):
        for y in range(64):
            k=(x*SS+SS//2,y*SS+SS//2)
            if k in zb: px[(x,y)]=zb[k]
    return px
if __name__=='__main__':
    px=render()
    im=Image.new('RGB',(64,64),(255,255,255))
    for (x,y),(d,ci,l,b) in px.items():
        v=int(80+170*max(0,min(1,(l+0.3)/1.3))); im.putpixel((x,y),(v,v-10*ci,v-20*ci))
    im.resize((384,384),Image.NEAREST).save(sys.argv[1])
    print(len(px))
