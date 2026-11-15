# raster -> png + controles. gebruik: python3 bouw.py r1_spec rN
import sys, importlib.util, numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/sneeuwbolslak/sprite/'
spec, naam = sys.argv[1], sys.argv[2]
s=importlib.util.spec_from_file_location('s', D+'maker/'+spec+'.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
ref=Image.open(D+'r1_B.png'); S=np.array(Image.open(D+'start46.png'))
a=np.zeros((64,64),np.uint8)
for j in range(37):
    row=['.']*46
    for st,px in m.R.get(j,[]):
        for k,c in enumerate(px):
            assert row[st+k]=='.', ('overlap',j,st+k)
            row[st+k]=c
    assert len(row)==46,(j,len(row))
    for i,c in enumerate(row):
        if c!='.': a[23+j,9+i]=int(c,16)
im=Image.fromarray(a,'P'); im.putpalette(ref.getpalette()); im.save(D+'maker/'+naam+'.png',transparency=0)
# controles
im2=Image.open(D+'maker/'+naam+'.png'); print('mode',im2.mode,'transp',im2.info.get('transparency'),'pal==r1_B',im2.getpalette()[:48]==ref.getpalette()[:48])
print('gebruikte indices',sorted(set(np.unique(a))))
M=a>0; MS=S>0
print('silhouet-diff t.o.v. start46: erbij',int((M&~MS).sum()),'eraf',int((~M&MS).sum()))
for y,x in zip(*np.nonzero(M^MS)): print('  diff',x-9,y-23,'erbij' if M[y,x] else 'eraf')
# randpixels die geen lijntint zijn
P=np.pad(M,1)
open_=[]
for y,x in zip(*np.nonzero(M)):
    nb=[P[y,x+1],P[y+2,x+1],P[y+1,x],P[y+1,x+2]]
    if not all(nb) and a[y,x] not in (1,2,13): open_.append((x-9,y-23,hex(a[y,x])))
print('randpixels niet 1/2:',open_)
# clusters < 3 per index
klein=[]
for v in range(2,16):
    seen=np.zeros_like(M)
    for y0,x0 in zip(*np.nonzero(a==v)):
        if seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; comp=[]
        while st:
            y,x=st.pop(); comp.append((x-9,y-23))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=y+dy,x+dx
                if 0<=yy<64 and 0<=xx<64 and a[yy,xx]==v and not seen[yy,xx]: seen[yy,xx]=1; st.append((yy,xx))
        if len(comp)<3: klein.append((hex(v),comp))
print('clusters <3 px:'); [print('  ',k) for k in klein]
# losse 1 (zwart) zonder rand
