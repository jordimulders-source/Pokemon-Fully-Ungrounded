# Meetgereedschap eindkeuring gaucho-Lombre: modelkleur/-helderheid per spritepixel (ML).
# Spritepixel (x,y) -> natieve modelpixel via de geschrapte rijen/kolommen uit ../sprite/r1/kaal_meta.npy
# (kale reductie = elke spritepixel is één natieve modelpixel; natief raster 10,24 px, ../sprite/r1/natief.png).
import os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R1=os.path.join(H,'..','sprite','r1')
meta=np.load(os.path.join(R1,'kaal_meta.npy')).tolist()
OFF0,OFF1,Y0,X0=meta[:4]; i1=meta.index(-1); i2=meta.index(-1,i1+1)
wr=set(meta[i1+1:i2]); wk=set(meta[i2+1:])
rows=[r for r in range(74) if r not in wr]; cols=[c for c in range(54) if c not in wk]
nat=np.asarray(Image.open(os.path.join(R1,'natief.png')).convert('RGB')).astype(float)
MC=np.zeros((64,64,3))
for y in range(64):
    for x in range(64):
        fy=y-Y0; fx=x-X0
        if 0<=fy<len(rows) and 0<=fx<len(cols): MC[y,x]=nat[OFF0+rows[fy],OFF1+cols[fx]]
ML=MC@[0.299,0.587,0.114]
def lum(c): return 0.299*c[0]+0.587*c[1]+0.114*c[2]
if __name__=='__main__':
    a=np.array(Image.open(os.path.join(H,'..','sprite','r3','lombre_gaucho_r3_A.png')))
    pal=Image.open(os.path.join(H,'..','sprite','r3','lombre_gaucho_r3_A.png')).getpalette()
    for i in range(1,16):
        m=a==i
        if m.sum(): v=ML[m]; print(i,pal[3*i:3*i+3],'L=%.0f'%lum(pal[3*i:3*i+3]),'n=%d ML gem %.0f p15 %.0f p85 %.0f'%(m.sum(),v.mean(),np.percentile(v,15),np.percentile(v,85)))
