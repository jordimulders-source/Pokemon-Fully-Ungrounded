import sys,numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/'
A2=Image.open(R+'icoon/onderdelen/a2.png'); a2=np.array(A2); c=a2.copy()
V8=np.array(Image.open(R+'icoon/maker/icon_v8.png'))
E={}  # (x,y): index   (hex chars)
def put(y,xs,s):
    for x,ch in zip(xs,s): E[(x,y)]=int(ch,16) if ch!='.' else 0
ZONE={}
def zone(n,*cells):
    for c_ in cells: ZONE[c_]=n
# oren
put(10,[7],'7'); put(11,[7],'7')
put(10,[13,14],'7e'); put(11,[13,14],'7e'); put(12,[13,14],'7e'); put(13,[12],'7')
# kop: voorhoofd-highlight, ooglid, oog
put(15,[11,12,13,14,15],'7766f'); put(16,[12],'6')
put(15,[9,10],'66')
put(16,[9,10,11],'f3f')
put(17,[8,9,10],'fff')
# wangpluk
put(16,[5,6],'98'); put(17,[5,6],'88')
# nekpluk (getand: punten licht)
put(16,[13,14,15],'899'); put(17,[11,12],'98'); put(18,[11,12],'88'); put(19,[12,13],'89')
# snuit onderkant: geen bruine strook
put(19,[7,8,9,10,11],'7777e')
# snorharen: 1 px, schuin naar links
put(19,[4,5,6],'eee'); put(20,[2,3],'ee'); put(21,[5,6],'ee'); put(22,[4],'e')
put(19,[3],'.')
# pluk-omlijning onder
put(17,[13],'e'); put(18,[13],'e'); put(19,[14],'e')
# bef
put(20,[10,11,12,13],'3377'); put(21,[11],'3')
# rug-highlight
put(18,[17,18],'33')
# dijlijn
put(20,[20],'e'); put(21,[19],'e'); put(22,[18],'e'); put(23,[18],'e'); put(24,[18],'e'); put(25,[18],'e')
# voorpoot tegen borst/buik, buik
put(22,[13,14,15],'e7e'); put(23,[15,16,17],'e33')
# opgeheven poot: rond, bruin binnen (1 px erbij op 12,23)
put(22,[11,12],'e6'); put(23,[10,11,12],'e6e'); put(24,[9,10,11],'eee')
for (x,y),v in E.items(): c[y,x]=v
# staart bevroren
def mask(spec):
    m=np.zeros((32,32),bool)
    for (a,b),x0 in spec: m[a:b+1,x0:]=True
    return m
T1=mask([((10,16),22),((17,17),24),((18,20),25),((21,22),24),((23,24),25)])&(a2>0)
c[T1]=a2[T1]
# omlijning: randpixels donker, boven 15 / onder 14 (geel en snorhaar-tips uitgezonderd)
mm=c>0; pad=np.pad(mm,1); edge=mm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
yy,_=np.nonzero(mm); mid=(yy.min()+yy.max())/2
for y,x in zip(*np.nonzero(edge)):
    if T1[y,x] or c[y,x] in (8,9,1): continue
    c[y,x]=15 if y<mid else 14
# frame 2
nt=c.copy(); nt[T1]=0
f2=np.zeros_like(c); f2[1:24]=nt[0:23]; f2[24:]=nt[24:]
T2=mask([((10,16),20),((17,17),24),((18,20),25),((21,22),24)])
v2=V8[32:64]
for y in range(31):
    for x in range(32):
        if T2[y,x] and v2[y,x]: f2[y+1,x]=v2[y,x]
out=np.vstack([c,f2])
im=Image.fromarray(out,'P'); im.putpalette(A2.getpalette()); im.save(sys.argv[1],transparency=0)
im.resize((256,512),Image.NEAREST).save(sys.argv[1].replace('.png','_8x.png'),transparency=0)
d=(c!=a2)
Z={'oren':(slice(8,14),slice(5,17)),'kop+oog+wang (rij 14-19, x0-12)':(slice(14,20),slice(0,13)),'nekpluk (x11-15, rij 16-19)':None}
print('totaal anders frame 1:',int(d.sum()),'staart:',int((d&T1).sum()))
print('veranderd:',sorted([(int(x),int(y),int(a2[y,x]),int(c[y,x])) for y,x in zip(*np.nonzero(d))],key=lambda t:(t[1],t[0])))
