# Ronde 4: diff t.o.v. ronde 2 per zone + alpha van de nek t.o.v. de originele Silicobra; randen, losse pixels.
from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
g=[l.rstrip('\n') for l in open(B+'ronde4/silicobra_uyuni_raster.txt')][:64]
r=[l.rstrip('\n') for l in open(B+'ronde2/silicobra_uyuni_raster.txt')][:64]
o=list(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/silicobra/anim_front.png').get_flattened_data())
def zone(x,y):
    if (x,y)==(19,15): return 'streepje (19,15)'
    if 31<=y<=44 and 16<=x<=42 and not (y==31 and x>=35): return 'nek'
    return 'bevroren'
cnt={}
for y in range(64):
    for x in range(64):
        if g[y][x]!=r[y][x]:
            k=zone(x,y); a='alpha erbij' if r[y][x]=='.' else 'alpha eraf' if g[y][x]=='.' else 'kleur'
            cnt.setdefault(k,{}); cnt[k][a]=cnt[k].get(a,0)+1
print('diff t.o.v. ronde 2:',cnt)
# nek-alpha t.o.v. origineel, rij 31-44
ad={}
for y in range(31,45):
    for x in range(14,42):
        a=g[y][x]!='.'; b=o[y*64+x]!=0
        if a!=b: ad.setdefault(y,[]).append((x,'+' if a else '-'))
print('nek-alpha t.o.v. origineel (rij: px):',ad)
# afstand nek/krul: lucht tussen band en krul per rij 36-41
for y in range(36,42):
    row=g[y]; xs=[x for x in range(30,50) if row[x]=='.']
    print('rij',y,'lucht x:',[x for x in xs if x<45])
n=Image.open(B+'ronde4/silicobra_uyuni.png'); N=list(n.get_flattened_data())
print('kleuren',len(set(N)),'transparency',n.info.get('transparency'),'pixels',sum(v!=0 for v in N))
T=lambda x,y: not(0<=x<64 and 0<=y<64) or g[y][x]=='.'
rim=set('OKhetsgd')
print('open randen:',[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x]!='.' and g[y][x] not in rim and any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
print('losse pixels:',[(x,y) for y in range(64) for x in range(64) if g[y][x]!='.' and all(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
print('omlijning kuif links (rij 13-18):',{y:min(x for x in range(64) if g[y][x]!='.') for y in range(13,19)})
