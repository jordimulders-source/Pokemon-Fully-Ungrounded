# ronde 3: alleen de keurdersreparaties; draait op raster.txt van r2. Indexen: 1=o 4=b 5=c 8=k 9=m A=n
R=[list(l.ljust(64,'.')) for l in open('../kleur_r2/raster.txt').read().split('\n')[:64]]
def px(x,y,ch): R[y][x]=ch
# 1. rechterbovenarm (horizontaal deel) zwart: bovenrand n, midden m, onderrand k; omlijning blijft
for y in range(33,38):
    for x in range(40,49):
        if R[y][x] in 'abcd':
            top = R[y-1][x]=='o'; bot = R[y+1][x]=='o'
            R[y][x] = 'n' if top else 'k' if bot else 'm'
px(39,36,'m')   # naad tussen elleboog en arm dicht (zie rapport)
# 2. kin/hals rechts van het strikje grijs, scheidingslijn op x36
for y in range(27,34):
    for x in range(37,41):
        if R[y][x] in 'nmkp':
            R[y][x] = 'c' if R[y][x+1]=='o' else 'b'
    if R[y][36] in 'nmkp': R[y][36]='o'
# 3. linkersnorkrul: kleine dichte krul in o, rest grijs
for (x,y),ch in {(28,19):'c',(29,19):'o',(30,19):'b',(31,19):'b',(28,20):'o',(29,20):'c',(30,20):'o',(31,20):'b',(28,21):'c',(29,21):'o',(30,21):'o'}.items(): px(x,y,ch)
# 4. kaarten: schaduwkant donker
for x,y in [(4,37),(4,38),(5,39),(6,40),(7,41),(8,42),(9,43),(53,23),(53,24),(52,25),(52,26),(51,27)]: px(x,y,'o')
for x,y in [(7,34),(8,34),(6,35),(5,36)]: px(x,y,'c')
# 5. mondlijn y24 x29-35 -> o
for x in range(29,36):
    if R[24][x]=='m': R[24][x]='o'
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
