# maak.py r7 (vanaf r6 variant A = r6_ref.png), alleen Jordi's twee punten:
# 1. meest linkse groen-gele tooiveer (rij 15-22, kol 13-21): liggend spits blad naar het model (punt links op x14 rij 19,
#    gele punt x15-18, groen lijf naar rechts onder de gele bladen, bovenrand rij 17, bolle onderrand rij 20-22).
# 2. opgetild been: één vloeiende lijn heup -> dij -> knie -> onderbeen terug/omlaag -> gekrulde teentjes, gelijke dikte.
import numpy as np; from PIL import Image
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
VEER=[
 (15,16,'..'),
 (16,15,'....'),
 (17,15,'55555'),
 (18,14,'566667'),
 (19,13,'.16677'),
 (20,14,'.17223'),
 (21,15,'.133441'),
 (22,17,'111'),
]
BEEN={  # model op 12x gevolgd: dij rij 50-51 van x31 naar x25, knie/voet links op x24, voet rij 52-54, teentjes krullen naar rechts
 'A':[(50,26,'ddbbbb1'),        # dij: donkerroze bovenrand, licht
      (51,24,'ddbbccc1'),       # dij onderhelft (midden), zwart aan de schaduwkant
      (52,24,'dbbc111'),        # knie gaat over in de voet ('vuistje' zoals het model)
      (53,24,'dbbc1'),
      (54,24,'1dbdb1'),         # gekrulde teentjes (Baile-teenuiteinden)
      (55,25,'1111')],
 'B':[(50,26,'ddbbbb1'),        # zelfde dij, daarna dunne scheen (2 px) en teentjes naar rechts
      (51,24,'ddbbccc1'),
      (52,24,'dbc1111'),
      (53,24,'db1'),
      (54,24,'dbbc1'),
      (55,24,'1d1b1'),
      (56,25,'1.1')],
}
def maak(v):
    a=np.array(Image.open('r6_ref.png')).astype(np.uint8)
    for y,x,s in VEER: zet(a,y,x,s)
    if v in BEEN:
        a[50:56,21:32]=0; a[56,21:30]=0
        for y,x,s in BEEN[v]: zet(a,y,x,s)
    return a
if __name__=='__main__':
    from render import schrijf
    for v in BEEN: schrijf(maak(v),'variant_%s.png'%v)
    a=maak('A'); np.save('samba_r7.npy',a); schrijf(a,'samba.png')
    [print('%02d '%y+''.join(H[c] for c in a[y,10:30])) for y in range(13,24)]
