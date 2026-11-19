# r7: losse pixels op Jordi's punten, op r6/picapau.png (canvas-coordinaten). Niets hertekend.
import numpy as np; from PIL import Image
src=Image.open('../r6/picapau.png'); a=np.array(src); r6=a.copy(); L={}
def zet(z,l):
    for x,y,v in l:
        assert a[y,x]!=v,(z,x,y); L.setdefault(z,[]).append((x,y,int(a[y,x]),v)); a[y,x]=v
zet('2 kop links ronder',[(21,22,13),(21,23,2),(16,26,13),(17,26,2)])   # rand rij 21-27: 24,21,19,18,17,16,16 (stappen 3,2,1,1,1,0)
zet('2 bruine pixel naast snavel',[(15,32,0)])   # stak links uit naast de snavelonderkant, boven de verre wang
zet('3 stekel onder rechteroor',[(33,25,0),(32,25,1)])                   # onderrand loopt 1 px verder diagonaal door
zet('4 oog rond',[(25,27,1),(26,27,1),(27,27,1),(24,28,1),(28,28,1),(25,28,15),(25,29,1)])  # 3/5/5/5/3, glans 1 omhoog naar linksboven
zet('5 snavelpunt scherper',[(15,29,1),(15,30,0),(16,30,1)])
Image.fromarray(a,'P').save('picapau.png',transparency=0) if False else None
p=Image.fromarray(a,'P'); p.putpalette(src.getpalette()); p.save('picapau.png',transparency=0)
for z,l in L.items(): print('%-28s %d px'%(z,len(l)),[(x,y) for x,y,_,_ in l])
print('totaal',sum(len(l) for l in L.values()),' diff check',int((a!=r6).sum()))
