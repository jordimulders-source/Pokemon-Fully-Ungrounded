# vel.png: model (spriteschaal) | r2 | r3 op 8x, daaronder per gerepareerde zone 16x: model | r2 | r3
import os, json; import numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); G=json.load(open(os.path.join(H,'../r1/geo_0.80.json')))
def s2m(i,j): return ((i-G['ox'])*G['T']+G['cx'], (j-G['oy'])*G['T']+G['cy'])
model=Image.open(os.path.join(H,'../../model.png')).convert('RGB')
def mcrop(i0,j0,i1,j1,z):
    a=s2m(i0,j0); b=s2m(i1,j1); return model.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1]))).resize(((i1-i0)*z,(j1-j0)*z),Image.LANCZOS)
def spr(p,i0,j0,i1,j1,z):
    a=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',a.size,(200,230,200,255)); bg.alpha_composite(a)
    return bg.crop((i0,j0,i1,j1)).resize(((i1-i0)*z,(j1-j0)*z),Image.NEAREST).convert('RGB')
P=[None,os.path.join(H,'../r2/zandloper_fase2_r2.png'),os.path.join(H,'zandloper_fase2_r3.png')]
ZON=[('1 lichte zone',20,22,40,34),('2+3 glas/hals',11,44,37,58),('4 haak ?',5,19,15,29),('5 linkerarm',11,28,25,37),('5 vuist',41,29,55,40),('6 kappen',11,41,37,58)]
z=16; rows=[]
for naam,i0,j0,i1,j1 in ZON:
    ims=[mcrop(i0,j0,i1,j1,z) if p is None else spr(p,i0,j0,i1,j1,z) for p in P]
    w=sum(im.size[0] for im in ims)+2*12; h=ims[0].size[1]+22
    r=Image.new('RGB',(w,h),(255,255,255)); d=ImageDraw.Draw(r); d.text((4,4),naam+': model | r2 | r3',fill=(0,0,0)); x=0
    for im in ims: r.paste(im,(x,22)); x+=im.size[0]+12
    rows.append(r)
top=Image.new('RGB',(3*520,512+26),(255,255,255)); d=ImageDraw.Draw(top)
for k,(p,t) in enumerate(zip(P,['model (spriteschaal)','r2','r3'])):
    top.paste(mcrop(0,0,64,64,8) if p is None else spr(p,0,0,64,64,8),(k*520,26)); d.text((k*520+4,6),t,fill=(0,0,0))
# zones in twee kolommen onder elkaar
W=max(top.size[0],max(r.size[0] for r in rows[0::2])+max(r.size[0] for r in rows[1::2])+20)
hs=[max(rows[k].size[1],rows[k+1].size[1] if k+1<len(rows) else 0) for k in range(0,len(rows),2)]
out=Image.new('RGB',(W,top.size[1]+sum(hs)+10*len(hs)),(255,255,255)); out.paste(top,(0,0)); y=top.size[1]+10
c2=max(r.size[0] for r in rows[0::2])+20
for n,k in enumerate(range(0,len(rows),2)):
    out.paste(rows[k],(0,y))
    if k+1<len(rows): out.paste(rows[k+1],(c2,y))
    y+=hs[n]+10
out.save(os.path.join(H,'vel.png')); print(out.size)
