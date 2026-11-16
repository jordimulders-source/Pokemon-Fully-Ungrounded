# Mond + neus: varianten met andere bemonsteringsfase en/of lipregel; score = kleurafstand tot het LANCZOS-verkleinde model in de zone
import itertools; import numpy as np; from PIL import Image, ImageDraw
from zone import *
r1=np.load('r1_bevroren.npy'); op=r1>0; p=np.pad(op,1); rand=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
Z=np.zeros((64,64),bool); Z[33:47,6:38]=True; Z&=op&~rand
MK=model_klein()
res=[]
for phx,phy in itertools.product([0,1/3,1/2,2/3],repeat=2):
    LZ=lijnkaart(ZW,phx,phy); L9=lijnkaart(D9,phx,phy)-LZ
    for lipr in (False,True):
        o=r1.copy()
        for j,i in zip(*np.where(Z)): o[j,i]=bemonster(i,j,phx,phy,LZ,L9,lipr)
        hoeken(o,Z,vul=lambda y,x:bemonster(x,y,phx,phy,set(),set(),lipr))
        d=np.sqrt(((feat(rgb(o)[Z].astype(float))-feat(MK[...,:3][Z]))**2).sum(1)).mean()
        res.append((d,phx,phy,lipr,o))
res.sort(key=lambda r:r[0])
for d,phx,phy,lipr,o in res[:8]: print('%.1f'%d,'fase x %.2f y %.2f'%(phx,phy),'lipregel' if lipr else '')
d1=[r for r in res if r[1]==0 and r[2]==0 and not r[3]][0][0]; print('fase 0 zonder lipregel (= r1-methode): %.1f'%d1)
np.save('mond_varianten.npy',np.array([r[4] for r in res[:6]])); 
import json; json.dump([(r[0],r[1],r[2],r[3]) for r in res[:6]],open('mond_varianten.json','w'))
# vel: model 12x | r1 12x | top-6 varianten 12x (zone x 4..40, y 30..49)
x0,y0,x1,y1=4,30,40,49; S=12
def crop(rgbarr): return Image.fromarray(rgbarr.astype('uint8')[y0:y1,x0:x1]).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
mk=MK.copy(); mk[...,:3][mk[...,3]==0]=255
tegels=[('model verkleind',crop(mk[...,:3])),('r1',crop(rgb(r1)))]+[('v%d fase %.2f/%.2f%s'%(k+1,r[1],r[2],' lip' if r[3] else ''),crop(rgb(r[4]))) for k,r in enumerate(res[:6])]
m=Image.open('model_natief.png'); w=Image.new('RGBA',m.size,'white'); w.alpha_composite(m)
nx0,ny0=X0+(x0-1)*F,Y0+(y0-17)*F; nat=w.convert('RGB').crop((int(nx0),int(ny0),int(nx0+(x1-x0)*F),int(ny0+(y1-y0)*F)))
tegels.insert(0,('model natief',nat.resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)))
tw,th=tegels[0][1].size; v=Image.new('RGB',(3*(tw+10),3*(th+24)),'white'); dr=ImageDraw.Draw(v)
for k,(t,im) in enumerate(tegels):
    X,Y=(k%3)*(tw+10),(k//3)*(th+24); v.paste(im,(X,Y+20)); dr.text((X+4,Y+4),t,fill=(0,0,0))
v.save('mondvel_r2.png')
