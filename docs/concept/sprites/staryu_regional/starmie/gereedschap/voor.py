# voor.py: voorste ster in het natieve model (99x99) = figuur ∩ veelhoek. De veelhoekranden liggen alleen
# langs de grens voorste ster / achterste koekpunt, gemeten op het natieve raster (zie NOTITIES);
# elders begrenst de modelfiguur zelf. Tips en inkepingen gemeten op natief.png.
import numpy as np; from PIL import Image, ImageDraw
NATIEF='gereedschap/natief.png'
POLY=[(44.8,-1),(51.0,-1),(59.0,35.0),(100,34.5),(100,41.2),(71.5,55.0),(75.1,100),(21.1,100),(26.5,55.0),(-1,39.3),(-1,34.5),(40.0,34.5)]
TIPS_M={'top':(48.5,12),'r':(86,42),'br':(72,84),'bl':(26,84),'l':(12,41)}
def natief(): return np.asarray(Image.open(NATIEF).convert('RGB')).astype(int)
def vul_gaten(m):
    H,W=m.shape; buiten=np.zeros_like(m); st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    st=[(y,x) for y,x in st if not m[y,x]]
    for y,x in st: buiten[y,x]=True
    while st:
        y,x=st.pop()
        for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
            if 0<=yy<H and 0<=xx<W and not m[yy,xx] and not buiten[yy,xx]: buiten[yy,xx]=True; st.append((yy,xx))
    return ~buiten
def figuur(a): return vul_gaten(a.min(2)<215)
def poly_mask(W=99,H=99,sub=4):
    im=Image.new('L',(W*sub,H*sub),0); ImageDraw.Draw(im).polygon([(x*sub,y*sub) for x,y in POLY],fill=255)
    m=np.asarray(im.resize((W,H),Image.BOX))>=128
    return m
def voor_mask(a=None):
    a=natief() if a is None else a
    return figuur(a)&poly_mask()
