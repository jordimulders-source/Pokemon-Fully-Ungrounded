# Ronde 5: A t.o.v. ronde 4 per zone; B t.o.v. A; alpha; randen; losse pixels.
from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/'
rd=lambda p:[l.rstrip('\n') for l in open(B+p)][:64]
r4=rd('ronde4/silicobra_uyuni_raster.txt'); A=rd('ronde5/silicobra_uyuni_raster.txt'); K=rd('ronde5/silicobra_uyuni_kuiflijn_raster.txt')
def zone(x,y): return 'nek (rij 31-44)' if 31<=y<=44 else 'kop en rest'
def diff(a,b,z):
    c={}
    for y in range(64):
        for x in range(64):
            if a[y][x]!=b[y][x]:
                t='alpha' if '.' in (a[y][x],b[y][x]) else 'kleur'; k=z(x,y); c.setdefault(k,{}); c[k][t]=c[k].get(t,0)+1
    return c
print('A t.o.v. ronde 4:',diff(r4,A,zone))
print('B t.o.v. A:',diff(A,K,lambda x,y:'kuiflijn' if y<=31 else 'nek'))
o=list(Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/silicobra/anim_front.png').get_flattened_data())
print('B-lijnpixels allemaal binnen de oude kopomtrek:',all(o[y*64+x]!=0 for y in range(64) for x in range(64) if A[y][x]!=K[y][x]))
for naam,g in (('A',A),('B',K)):
    T=lambda x,y: not(0<=x<64 and 0<=y<64) or g[y][x]=='.'
    rim=set('OKhetsgd')
    print(naam,'open randen:',[(x,y) for y in range(64) for x in range(64) if g[y][x]!='.' and g[y][x] not in rim and any(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))],
          'losse pixels:',[(x,y) for y in range(64) for x in range(64) if g[y][x]!='.' and all(T(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))])
for f in ('silicobra_uyuni.png','silicobra_uyuni_kuiflijn.png'):
    n=Image.open(B+'ronde5/'+f); print(f,n.mode,n.size,'kleuren',len(set(n.get_flattened_data())),'transparency',n.info.get('transparency'))
