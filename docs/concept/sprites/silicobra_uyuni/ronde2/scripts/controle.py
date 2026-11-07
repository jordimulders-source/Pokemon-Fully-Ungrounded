# Ronde 2: alpha-diff t.o.v. ronde 1 per zone, randen, losse pixels, rechte naden in de korst.
from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
n=Image.open(B+'ronde2/silicobra_uyuni.png'); r1=Image.open(B+'ronde1/silicobra_uyuni.png')
N=list(n.get_flattened_data()); R=list(r1.get_flattened_data())
g=[l.rstrip('\n') for l in open(B+'ronde2/silicobra_uyuni_raster.txt')]
def zone(x,y):
    if 19<=y<=29 and 22<=x<=31: return 'oog'
    if y<=31 and x>=19: return 'korst/kuif'
    if 31<=y<=43 and 18<=x<=42: return 'pekelzak'
    return 'rest (gezicht, voet, krul)'
cnt={}
for i in range(4096):
    x,y=i%64,i//64
    a,c=N[i]!=0,R[i]!=0
    if a!=c: k=(zone(x,y),'erbij' if a else 'eraf'); cnt[k]=cnt.get(k,0)+1
print('alpha-diff t.o.v. ronde 1:',cnt or 'geen')
# kleurdiff per zone (alleen info)
cd={}
for i in range(4096):
    x,y=i%64,i//64
    if g[y][x]!=open(B+'ronde1/silicobra_uyuni_raster.txt').read().split('\n')[y][x]:
        cd[zone(x,y)]=cd.get(zone(x,y),0)+1
print('gewijzigde pixels (kleur of alpha) per zone:',cd)
print('kleuren:',len(set(N)),'transparency',n.info.get('transparency'),'pixels',sum(v!=0 for v in N))
T=lambda x,y: not(0<=x<64 and 0<=y<64) or g[y][x]=='.'
rim=set('OKhetsgd')
print('open randen:',[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x]!='.' and g[y][x] not in rim and any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
print('losse pixels:',[(x,y) for y in range(64) for x in range(64) if g[y][x]!='.' and all(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
# rechte naden (d/e) >=3 px in de korst, binnen de omlijning, buiten het oog
def inside(x,y): return zone(x,y)=='korst/kuif' and not any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
runs=[]
for y in range(13,32):
    x=19
    while x<64:
        if inside(x,y) and g[y][x] in 'de':
            s=x
            while x<64 and inside(x,y) and g[y][x] in 'de': x+=1
            if x-s>=3: runs.append(('hor',s,y,x-s))
        x+=1
for x in range(19,46):
    y=13
    while y<32:
        if inside(x,y) and g[y][x] in 'de':
            s=y
            while y<32 and inside(x,y) and g[y][x] in 'de': y+=1
            if y-s>=3: runs.append(('ver',x,s,y-s))
        y+=1
print('rechte naden >=3 px:',runs)
