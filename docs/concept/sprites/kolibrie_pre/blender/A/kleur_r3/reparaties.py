"""r3 = r2-raster + benoemde reparaties uit KEURING.md (r2). Elke pixel met de hand gekozen."""
r=[list(l.rstrip('\n')) for l in open('../kleur_r2/raster.txt')][:64]
E={
 # gaap: open rand dicht met omlijningskleur (vorm gelijk)
 (15,18):'1',(16,19):'1',
 # 4 kap-banding: E alleen onderaan (30,22),(30,23),(31,23)
 (29,19):'B',(30,19):'B',(29,20):'B',(30,20):'B',(29,21):'B',(30,21):'B',(29,22):'B',
 # 3 kop-over-rug: één taps lijntje (29,26)(28,26)(27,27)
 (30,25):'3',
 # 5 vleugel: lichte binnenrand weg, één vlekje linksboven (34-35,28-29)
 (36,28):'B',(35,29):'4',(33,30):'B',(32,31):'B',(32,32):'B',
 # 7 rugcurve x41 y29-32: trap in kleur zachter
 (41,32):'E',
 # 15 staart: lob in schaduw, alleen top licht
 (41,36):'3',(42,36):'3',(42,37):'3',(43,37):'2',(42,38):'2',(42,39):'2',(43,40):'2',(42,40):'2',
 # 14 pootjes: nabije poot C/D, verre poot 9 (donker warm), teentjes, klauwpunt (30,45)
 (26,43):'1',(27,43):'1',(28,43):'C',(29,43):'D',(30,43):'1',(31,43):'D',(32,43):'9',(33,43):'1',(34,43):'1',(35,43):'1',
 (27,44):'D',(28,44):'1',(29,44):'D',(30,44):'9',(31,44):'1',(32,44):'9',
 (30,45):'1',
}
for (x,y),c in E.items():
    assert r[y][x]!='.', (x,y)
    r[y][x]=c
open('raster.txt','w').write('\n'.join(''.join(l) for l in r)+'\n')
print(len(E),'pixels gezet')
