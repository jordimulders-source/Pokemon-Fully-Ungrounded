# r13 = r12 + afrondingsronde (punten 1-4 moet, 5-7 kan). Per pixel, uit model/keuring.
# Draaien vanuit deze map: python3 build.py
from PIL import Image; import numpy as np
im=Image.open('../r12/banette_evo.png'); a=np.array(im); pal=im.getpalette()
Z={}   # zone -> lijst (x,y,nieuw)
# 1 rechterbel: bol met gaatje, X sluit schoon aan
Z['1_belR']=[(50,17,1),(53,17,1),(50,18,2),(53,18,3),(53,19,4),
             (52,23,3)]                       # 2x2-klont (51-52,22-23) -> 1px lijn
# 2 rode helft: highlight-sikkel (15), sikkelschaduw (7), buitenrand bolt
hl=[(34,7),(35,7),(36,7),(33,8),(34,8),(35,8),(32,9),(33,9),(31,10),(32,10),
    (31,11),(30,12),(30,13),(30,14)]                # binnen de selout (7) en niet op de steeknaad (37,7)-(41,11)
Z['2_rood']=[(x,y,15) for x,y in hl]
# schaduw: smal boven (1px y19-25), 2px y26-27, 3px y28-33, onder blijft breed
Z['2_rood']+=[(41,19,6),(41,20,6),(42,21,6),(42,22,6),(42,23,6),(42,24,6),(42,25,6),
              (42,26,6),(42,27,6)]
# rand: y22-25 en y32-33 naar x44, y26-31 blijft x45
Z['2_rood']+=[(44,22,1),(44,23,1),(44,24,1),(44,25,1),(45,22,0),(45,23,0),(45,24,0),(45,25,0),
              (46,22,4),(46,23,4),(46,24,4),(46,25,4),          # lijn grijze X volgt de wig (zoals x47 y19-21)
              (44,32,1),(44,33,1),(45,32,0),(45,33,0),(46,32,0)]
# 3 linkeroog: ring centreert op pupil x19, geel alleen rij 29
Z['3_oogL']=[(20,28,6),(18,30,15),(20,30,15)]
# 4 grijze flappunt
Z['4_flap']=[(11,28,4),(12,28,4),(10,29,4),(11,29,4)]
# kan 6 linkerbel meer metaal, 7 randlicht Shuppet rechts
Z['6_belL']=[(8,34,2),(6,36,2)]
Z['7_shup']=[(58,57,12),(58,58,12),(57,50,12),(57,51,12)]
log=[]
for k,L in Z.items():
    n=0
    for x,y,v in L:
        if a[y,x]!=v: log.append((k,x,y,int(a[y,x]),v)); a[y,x]=v; n+=1
    print(k,n,'px')
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal); out.save('banette_evo.png',transparency=0)
# bewijs: diff buiten zones = 0
r12=np.array(Image.open('../r12/banette_evo.png')); d=np.argwhere(r12!=a)
zone={(x,y) for L in Z.values() for x,y,_ in L}
print('diff totaal',len(d),'buiten zones',sum((x,y) not in zone for y,x in d))
for l in log: print(*l)
