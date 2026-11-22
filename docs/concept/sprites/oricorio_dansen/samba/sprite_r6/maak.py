# maak.py r6 (vanaf r5 = r5_ref.png), alleen Jordi's drie punten:
# 1. groen-gele veren linksonder (linkervleugel rij 42-50, kol 7-25): spitse uitwaaierende vingers naar het model
#    (model op het spriteraster gelegd, zie reduceer.py / vel): vinger 2 punt x7, vinger 3 punt x10, blauwe punt B1 omlaag tot rij 50,
#    blauwe punt B2 bij het lijf (x22-24, rij 45-48) zoals het model.
# 2. opgetild been: model-houding (dij naar voren, knie links, onderbeen naar achter/onder, gekrulde teentjes), Baile-opbouw.
# 3. standbeen + voet 1 px naar links.
import numpy as np, sys; from PIL import Image
H='.123456789abcdef'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c!=' ': a[y,x0+i]=H.index(c)
VLEUGEL=[
 (42,9,'.115'),
 (43,7,'444'),
 (44,7,'13333'),
 (44,14,'38666'),
 (45,8,'1'), (45,12,'448778777784'),     # gele veerpunten wijzen schuin omlaag (model) i.p.v. rechte donkere rij
 (46,10,'4222284448849 9a1'.replace(' ','')),
 (47,10,'133333'), (47,16,'999141aa1'),   # vinger 3 langer naar links (punt x10, model); blauwe punten B1/B2
 (48,11,'1444499a11.11'),
 (49,12,'11111a1'),
 (50,17,'1'),
]
# opgetild been, varianten (rij 50-56, kol 22-32); '.' wist, spatie laat staan
BEEN={
 'A':[(50,22,'...dddbbbb1'),   # dij naar voren (donkerroze bovenrand, lichtroze, zwarte onderrand)
      (51,22,'.ddbb11111'),    # knie links
      (52,22,'.dbb1'),
      (53,22,'.dbc1'),   # kort onderbeen omlaag
      (54,22,'.1dbb1'),   # voet krult naar achter
      (55,22,'..1d1b1'),   # twee teentjes (Baile-teenuiteinden: licht/donker met zwart eronder)
      (56,22,'...1.1')],
 'B':[(50,22,'...dddbbbb1'),   # dij naar voren
      (51,22,'..dbb11111'),
      (52,22,'....dd1'),   # Baile-voet van r5 (tenen naar voren)
      (53,22,'..ddbbd1'),
      (54,22,'.dbbbcc1'),
      (55,22,'.1111111'),
      (56,22,'')],
}
def standbeen_links(a):
    m=np.zeros_like(a,bool); m[50:56,32:40]=a[50:56,32:40]>0; m[56:64,:]=a[56:64,:]>0
    o=a.copy(); o[m]=0
    ys,xs=np.where(m); o[ys,xs-1]=a[ys,xs]
    return o
def maak(v):
    a=np.array(Image.open('r5_ref.png')).astype(np.uint8)
    for y,x,s in VLEUGEL: zet(a,y,x,s)
    a=standbeen_links(a)
    a[50:56,22:31]=0   # oude opgetilde been (r5) wissen
    for y,x,s in BEEN[v]: zet(a,y,x,s)
    return a
if __name__=='__main__':
    from render import schrijf
    for v in BEEN:
        a=maak(v); np.save('samba_r6%s.npy'%v.lower(),a); schrijf(a,'variant_%s.png'%v)
        print(v); [print('%02d '%y+''.join(H[c] for c in a[y,5:40])) for y in range(40,62)]
    a=maak('A'); np.save('samba_r6.npy',a); schrijf(a,'samba.png')
    Image.open('samba.png').convert('RGB').resize((512,512),Image.NEAREST).save('samba_8x.png')
