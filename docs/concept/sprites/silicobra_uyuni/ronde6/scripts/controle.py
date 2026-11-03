# Ronde 6: diff t.o.v. 5A per zone; overlay-check gezichtslijn tegen het origineel; randen, losse pixels.
from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
rd=lambda p:[l.rstrip('\n') for l in open(B+p)][:64]
A=rd('ronde5/silicobra_uyuni_raster.txt'); g=rd('ronde6/silicobra_uyuni_raster.txt')
o=list(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/silicobra/anim_front.png').get_flattened_data())
def zone(x,y):
    if y<=30: return 'gezichtslijn (kop)'
    if 31<=y<=35: return 'bovenkant band'
    return 'bevroren rest'
c={}
for y in range(64):
    for x in range(64):
        if A[y][x]!=g[y][x]:
            t='alpha' if '.' in (A[y][x],g[y][x]) else 'kleur'; k=zone(x,y); c.setdefault(k,{}); c[k][t]=c[k].get(t,0)+1
print('diff t.o.v. 5A:',c)
kop=[(x,y,A[y][x],g[y][x],'0123456789ABCDEF'[o[y*64+x]]) for y in range(31) for x in range(64) if A[y][x]!=g[y][x]]
print('kop-wijzigingen (x,y,5A,r6,index origineel):',kop)
print('onderkant band (rij 36-44) gelijk aan 5A:',all(A[y]==g[y] for y in range(36,64)))
T=lambda x,y: not(0<=x<64 and 0<=y<64) or g[y][x]=='.'
rim=set('OKhetsgd')
print('open randen:',[(x,y) for y in range(64) for x in range(64) if g[y][x]!='.' and g[y][x] not in rim and any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))],'losse pixels:',[(x,y) for y in range(64) for x in range(64) if g[y][x]!='.' and all(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
n=Image.open(B+'ronde6/silicobra_uyuni.png'); print(n.mode,n.size,'kleuren',len(set(n.get_flattened_data())),'transparency',n.info.get('transparency'))
