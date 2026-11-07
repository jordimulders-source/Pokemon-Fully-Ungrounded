# Stap 1: silhouet direct uit model v3 naar 64x64 (oppervlak-gemiddelde, drempel 0.5).
# A = puur het model. B = "minder mens" (SPEC): lijf gedrongener = romp ingekort langs zijn as
# (kop en steunarm blijven, heup + benen + vrije arm schuiven richting schouder).
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
M=np.asarray(Image.open('masker_groot.png'))>127; H,W=M.shape
# witte enkel rechts viel weg tegen de achtergrond: lokaal dichtmaken (alleen in dat vak)
v=(slice(120,240),slice(590,755)); M[v]=nd.binary_fill_holes(nd.binary_closing(M[v],iterations=14))|M[v]
SRC=Image.open('../referenties/model_gemini_pose_v3.png').convert('RGB'); SRC0=SRC
x0,y0,x1,y1=6,45,747,996
S=63/(y1-y0+1)            # hoogte 63 px, hand op de onderste rij
OX=(64-(x1-x0+1)*S)/2

def inkorten(M,k):
    # snijlijn dwars door de romp; alles aan de heupkant (benen, heup, vrije arm) schuift k px
    # langs de romp-as naar de schouder. Kop en steunarm blijven exact staan.
    sh=np.array([440.,640.]); hp=np.array([540.,370.])
    u=(hp-sh)/np.linalg.norm(hp-sh)
    yy,xx=np.mgrid[0:H,0:W].astype(float)
    t=(xx-sh[0])*u[0]+(yy-sh[1])*u[1]; tc=100
    boven=M&(t>=tc); onder=M&(t<tc+k)
    sch=nd.shift(boven.astype(float),(-k*u[1],-k*u[0]),order=0)>0.5
    return onder|sch

def naar64(M):
    out=np.zeros((64,64))
    ys,xs=np.mgrid[0:H,0:W]
    gx=((xs-x0)*S+OX); gy=((ys-y0)*S)
    ok=M&(gx>=0)&(gx<64)&(gy>=0)&(gy<64)
    np.add.at(out,(gy[ok].astype(int),gx[ok].astype(int)),1)
    return out/(1/S)**2>=0.5

def los(g):  # losse enkele pixels (ruis van de witte klauwen) weg
    n=nd.convolve(g.astype(int),np.ones((3,3),int),mode='constant')-g
    return g&(n>=2)
A=los(naar64(M)); B=los(naar64(inkorten(M,45)))
# vel: model (uitsnede, 512 hoog) | rode omtrek van A over het model | A 8x | B 8x | A en B 1x
Z=8
bg=Image.new('RGB',(W+800,H+200),(240,240,240)); bg.paste(SRC,(400,0)); SRC=bg
crop=SRC.crop((400+int(x0-OX/S),y0,400+int(x0-OX/S+64/S),int(y0+64/S))).resize((512,512),Image.LANCZOS)
def omtrek(g,base):
    im=base.copy(); px=im.load()
    e=g&~nd.binary_erosion(g)
    for y,x in zip(*np.nonzero(e)):
        for dy in range(Z):
            for dx in range(Z):
                if dy in(0,Z-1) or dx in(0,Z-1): px[x*Z+dx,y*Z+dy]=(220,0,0)
    return im
def groot(g):
    return Image.fromarray(np.where(np.kron(g,np.ones((Z,Z))).astype(bool),40,255).astype('uint8')).convert('RGB')
def raster(im):
    d=ImageDraw.Draw(im)
    for i in range(0,513,Z*8): d.line([(i,0),(i,512)],fill=(200,200,255)); d.line([(0,i),(512,i)],fill=(200,200,255))
    return im
if __name__=='__main__':
    for n,g in (('A',A),('B',B)):
        Image.fromarray((~g*255).astype('uint8')).save(f'silhouet_{n}_1x.png')
        open(f'silhouet_{n}.txt','w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in g)+'\n')
        print(n,'pixels',int(g.sum()),'bbox',np.nonzero(g.any(0))[0][[0,-1]],np.nonzero(g.any(1))[0][[0,-1]])
    
    # vel: model (uitsnede, 512 hoog) | rode omtrek van A over het model | A 8x | B 8x | A en B 1x
    Z=8
    bg=Image.new('RGB',(W+800,H+200),(240,240,240)); bg.paste(SRC,(400,0)); SRC=bg
    crop=SRC.crop((400+int(x0-OX/S),y0,400+int(x0-OX/S+64/S),int(y0+64/S))).resize((512,512),Image.LANCZOS)
    def omtrek(g,base):
        im=base.copy(); px=im.load()
        e=g&~nd.binary_erosion(g)
        for y,x in zip(*np.nonzero(e)):
            for dy in range(Z):
                for dx in range(Z):
                    if dy in(0,Z-1) or dx in(0,Z-1): px[x*Z+dx,y*Z+dy]=(220,0,0)
        return im
    def groot(g):
        return Image.fromarray(np.where(np.kron(g,np.ones((Z,Z))).astype(bool),40,255).astype('uint8')).convert('RGB')
    def raster(im):
        d=ImageDraw.Draw(im)
        for i in range(0,513,Z*8): d.line([(i,0),(i,512)],fill=(200,200,255)); d.line([(0,i),(512,i)],fill=(200,200,255))
        return im
    pan=[crop,omtrek(A,crop),raster(groot(A)),raster(groot(B))]
    titels=['model v3 (bron)','A: omtrek over model','A: direct uit model (8x)','B: lijf gedrongener (8x)']
    V=Image.new('RGB',(4*522+10,512+40+80),'white'); d=ImageDraw.Draw(V)
    for i,(p,t) in enumerate(zip(pan,titels)):
        V.paste(p,(10+i*522,30)); d.text((10+i*522,10),t,fill='black')
    for i,g in enumerate((A,B)):
        s=Image.fromarray(np.where(g,40,255).astype('uint8'))
        V.paste(s,(10+(2+i)*522,552)); V.paste(s.resize((128,128)),(90+(2+i)*522,552))
    V.save('vel_stap1.png')
