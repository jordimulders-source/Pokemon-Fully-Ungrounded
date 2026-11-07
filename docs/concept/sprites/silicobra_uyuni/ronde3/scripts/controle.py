# Ronde 3: pixeldiff t.o.v. ronde 2 per zone, randen, losse pixels, rechte stukken in de zakomtrek.
from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
g=[l.rstrip('\n') for l in open(B+'ronde3/silicobra_uyuni_raster.txt')][:64]
r=[l.rstrip('\n') for l in open(B+'ronde2/silicobra_uyuni_raster.txt')][:64]
def zone(x,y):
    if y<=18 and x<=24: return 'kuif links'
    if 31<=y<=43 and 18<=x<=42: return 'pekelzak'
    return 'bevroren (oog, gezicht, korst, voet, krul)'
cnt={}
for y in range(64):
    for x in range(64):
        if g[y][x]!=r[y][x]:
            k=zone(x,y); a=('alpha erbij' if r[y][x]=='.' else 'alpha eraf' if g[y][x]=='.' else 'kleur')
            cnt.setdefault(k,{}); cnt[k][a]=cnt[k].get(a,0)+1
print('diff t.o.v. ronde 2:',cnt,'totaal',sum(sum(v.values()) for v in cnt.values()))
n=Image.open(B+'ronde3/silicobra_uyuni.png'); N=list(n.get_flattened_data())
print('kleuren',len(set(N)),'transparency',n.info.get('transparency'),'pixels',sum(v!=0 for v in N))
T=lambda x,y: not(0<=x<64 and 0<=y<64) or g[y][x]=='.'
rim=set('OKhetsgd')
print('open randen:',[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x]!='.' and g[y][x] not in rim and any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
print('losse pixels:',[(x,y) for y in range(64) for x in range(64) if g[y][x]!='.' and all(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
# rechterrand zak: x van de laatste niet-transparante pixel vóór de lucht, rij 32-41
print('rechterrand zak per rij:',{y:max(x for x in range(18,42) if g[y][x]!='.' and (T(x+1,y))) for y in range(32,42)})
# scheiding zak/krul: zakpixel (qrst) naast krulpixel?
krul=[(x,y) for y in range(36,44) for x in range(33,50) if g[y][x] in 'qrst' and any(g[y+b][x+a] in 'bdeKO' and x+a>=35 and y+b<=41 for a,b in((1,0),(0,1),(1,1),(1,-1)))]
print('zakpixels die de krul raken (rij<=41):',krul)
