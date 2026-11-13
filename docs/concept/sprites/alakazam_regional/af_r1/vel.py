# vel.py: voor/na op 8x, naast echte Gen 3-sprites op 8x, en 1x/2x op licht en donker -> vel.png
import importlib.util
from PIL import Image, ImageDraw
from gen3 import ref
def ld(p):
    s=importlib.util.spec_from_file_location('p'+str(abs(hash(p))),p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
P0=ld('../lijf_r2/pal.py'); P1=ld('pal.py')
BG=(152,208,160)
def ours(P,f,bg):
    im=P.rgb(P.load(f),bg); return im
voor=ours(P0,'basis_S1.txt',BG); na=ours(P1,'raster.txt',BG)
namen=['alakazam','kadabra','gardevoir','gothitelle','mr_mime','sneasel','umbreon']
refs=[]
for n in namen:
    o,_,_=ref(n); b=Image.new('RGBA',(64,64),BG+(255,)); b.alpha_composite(o); refs.append((n,b.convert('RGB'),o))
K=8; T=512; L=22
W=4*T+5*8; H=3*(T+L)+260
V=Image.new('RGB',(W,H),(255,255,255)); D=ImageDraw.Draw(V)
def tile(im,naam,i,j):
    x=8+i*(T+8); y=j*(T+L); D.text((x,y+4),naam,fill=(0,0,0)); V.paste(im.resize((T,T),0),(x,y+L))
tile(voor,'voor (lijf_r2/opt_S1)',0,0); tile(na,'na (af_r1)',1,0)
tile(refs[0][1],'alakazam (Gen 3)',2,0); tile(refs[1][1],'kadabra (Gen 3)',3,0)
for k,(n,im,_) in enumerate(refs[2:]): tile(im,n+(' (fan, Gen 3-stijl)' if n=='gothitelle' else ' (Gen 3)'),k%4,1+k//4)
tile(na,'na (af_r1)',3,2)
# 1x en 2x op licht en donker
y0=3*(T+L)+10
for row,(bg,lab) in enumerate([((248,248,240),'licht'),((40,40,56),'donker')]):
    yy=y0+row*125; D.text((8,yy),'1x en 1,5x op '+lab,fill=(0,0,0))
    x=8
    alle=[('voor',P0.rgb(P0.load('basis_S1.txt'),bg)),('na',P1.rgb(P1.load('raster.txt'),bg))]
    for n,_,o in refs:
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(o); alle.append((n,b.convert('RGB')))
    for n,im in alle:
        V.paste(im,(x,yy+16)); V.paste(im.resize((128,128),0) if False else im,(x,yy+16)); x+=70
    for n,im in alle[:3]:
        V.paste(im.resize((96,96),0),(x,yy+16)); x+=100
V.save('vel.png'); print(V.size)
