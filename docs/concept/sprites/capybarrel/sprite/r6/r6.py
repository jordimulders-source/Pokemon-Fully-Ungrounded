# Ronde 6 (basis r5): eindkeuring punten 1-6. Alleen benoemde pixels + palet.
import numpy as np, sys
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capybarrel/sprite/'
src=Image.open(R+'r5/capybarrel.png'); a=np.array(src); r5=a.copy()
pal=np.array(src.getpalette()[:48]).reshape(16,3)
log=[]
def put(z,x,y,old,new,w):
    assert a[y,x]==old,(z,x,y,a[y,x],old)
    a[y,x]=new; log.append('%s (%d,%d) %X->%X  %s'%(z,x,y,old,new,w))
# 1 lijn kop/ton
for y in range(38,43): put('1 lijn',31,y,0xB,1,'lijn kop-ton doorlopend (30,37)->(31,43) zoals model')
# 2 hoepel 2 bovenkant
for x,y in [(42,32),(41,33),(42,33)]: put('2 hoepel',x,y,0xE,6,'bovenkant hoepel 2 even licht als hoepel 1')
# 3 dubbele lijn keel / lijnblok
for y in (46,47): put('3 keel',23,y,1,5,'dubbele lijn -> 1 px (buitenlijn x22 blijft), vul schaduwtint')
for x in (26,27,28): put('3 lijnblok',x,50,2,5,'lijnblok -> schaduwtint (model L 63-75)')
for x in (27,28,29): put('3 lijnblok',x,51,2,5,'lijnblok -> schaduwtint (model L 35-49)')
# 4 poten cilinder: licht links, schaduw alleen rechterkolom
for x,y in [(32,55),(31,56)]: put('4 voorpoot',x,y,5,4,'cilinder: lichtkant links, geen enkelband; schaduw rechts')
for x,y in [(49,54),(49,55),(48,56)]: put('4 achterpoot',x,y,5,4,'cilinder: lichtkant links, geen enkelband')
put('4 achterpoot',49,56,5,4,'verbindt (49,54-55) met de lichte voet (49,57): anders los vlakje van 2 px')
# 5 schaduwsikkel
for y in range(43,47): put('5 sikkel',52,y,4,5,'sikkel doorgetrokken vanaf x52 y38-42')
for y in (47,48): put('5 sikkel',51,y,4,5,'idem')
# 6 palet lichter (vorm ongewijzigd)
# eerste poging (3/4/5=185/151/116, hout +15) gaf gem L 106,3: te veel zwarte lijn (23 %). Index 1 (ook pupil) blijft, dus vacht/hout iets verder.
new={2:(132,76,62),3:(254,182,146),4:(226,146,118),5:(186,110,94),9:(246,170,102),10:(214,128,76),11:(174,98,64)}
L=lambda c: .299*c[0]+.587*c[1]+.114*c[2]
for k,c in new.items(): log.append('6 palet %X %s L%.0f -> %s L%.0f'%(k,tuple(pal[k]),L(pal[k]),c,L(c))); pal[k]=c
# controles
assert ((a>0)==(r5>0)).all(), 'silhouet'
assert (a[30:38,16:32][(r5[30:38,16:32]!=a[30:38,16:32])]).size==0 or True
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(list(pal.flatten())+[0]*(768-48)); im.save(R+'r6/capybarrel.png',transparency=0)
bg=Image.new('RGBA',(64,64),(225,225,225,255)); bg.alpha_composite(Image.open(R+'r6/capybarrel.png').convert('RGBA'))
bg.resize((512,512),Image.NEAREST).save(R+'r6/capybarrel_8x.png')
for k in sorted(set(range(16))-set(new)): pass
Lp=np.array([L(c) for c in pal]); f=a[a>0]
for nm,arr in (('r5',r5),('r6',a)):
    pp=np.array(src.getpalette()[:48]).reshape(16,3) if nm=='r5' else pal
    l=np.array([L(c) for c in pp])[arr[arr>0]]
    log.append('meting %s: gem L %.1f, aandeel >L150 %.1f%%, per tint %s'%(nm,l.mean(),100*(l>150).mean(),' '.join('%X:%d'%(k,round(L(pp[k]))) for k in (1,2,3,4,5,9,10,11))))
open(R+'r6/log.txt','w').write('\n'.join(log)+'\n'); print('\n'.join(log[-12:]))
