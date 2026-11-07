# Zet raster.txt om naar nachtaap.png + normal.pal en controleert alles.
# Draaien: python3 bouw.py  (vanuit deze map of met absoluut pad)
import os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.dirname(HERE)
SILF=os.path.join(HERE,'../../../silhouet/silhouet_bevroren.txt')
SIL=[l.rstrip('\n') for l in open(SILF)][:64]
ORDER='.kdsblmnwrijcetf'
PAL={'.':(152,208,160),'k':(28,20,36),'d':(50,34,78),'s':(69,48,106),'b':(94,68,136),'l':(130,104,180),
 'm':(158,138,204),'n':(206,194,236),'w':(248,248,248),'r':(122,20,48),'i':(200,36,60),'j':(240,106,112),
 'c':(240,224,196),'e':(208,182,150),'t':(146,114,92),'f':(226,200,160)}
OUTLINE=set('kdt')
g=[['.']*64 for _ in range(64)]
for n,line in enumerate(open(os.path.join(HERE,'raster.txt'))):
    line=line.split('#')[0].strip()
    if not line: continue
    y,x,s=line.split(); y=int(y); x=int(x)
    for i,ch in enumerate(s):
        assert ch in PAL,(n+1,ch)
        g[y][x+i]=ch
open(os.path.join(HERE,'raster_grid.txt'),'w').write('\n'.join(''.join(r) for r in g)+'\n')
# 1. alpha-diff
err=[(x,y) for y in range(64) for x in range(64) if (g[y][x]!='.')!=(SIL[y][x]=='#')]
print('alpha-diff t.o.v. bevroren silhouet:',len(err),err[:30])
npx=sum(c!='.' for r in g for c in r); print('pixels:',npx,'(silhouet',sum(c=='#' for r in SIL for c in r),')')
# 2. open randen: niet-omlijningskleur naast transparant (4-buren)
op=[]
for y in range(64):
    for x in range(64):
        c=g[y][x]
        if c=='.' or c in OUTLINE: continue
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            X,Y=x+dx,y+dy
            if not(0<=X<64 and 0<=Y<64) or g[Y][X]=='.': op.append((x,y,c)); break
print('open randen:',len(op),op[:40])
# 3. losse pixels: geen enkele 8-buur met dezelfde kleur
lone=[]
for y in range(64):
    for x in range(64):
        c=g[y][x]
        if c=='.': continue
        if not any(0<=x+dx<64 and 0<=y+dy<64 and g[y+dy][x+dx]==c for dx in(-1,0,1) for dy in(-1,0,1) if dx or dy):
            lone.append((x,y,c))
print('losse pixels:',len(lone),lone)
from collections import Counter
cnt=Counter(c for r in g for c in r if c!='.'); print('kleuren:',len(cnt),dict(cnt))
print('zwart-aandeel: %.2f'%(cnt['k']/npx))
im=Image.new('P',(64,64)); flat=[]
for ch in ORDER: flat+=PAL[ch]
im.putpalette(flat)
im.putdata([ORDER.index(g[y][x]) for y in range(64) for x in range(64)])
im.save(os.path.join(OUT,'nachtaap.png'),transparency=0)
with open(os.path.join(OUT,'normal.pal'),'w',newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%PAL[ch] for ch in ORDER))
# preview
S=os.environ.get('PREV')
if S:
    rgba=im.convert('RGBA')
    bg=Image.new('RGBA',(64,64),(236,236,230,255)); bg.alpha_composite(rgba)
    big=bg.resize((512,512),Image.NEAREST)
    o=Image.new('RGBA',(512+16+64*3+8+64,512),(236,236,230,255)); o.paste(big,(0,0))
    o.paste(bg.resize((192,192),Image.NEAREST),(528,0)); o.paste(bg,(528,200))
    dk=Image.new('RGBA',(64,64),(40,40,48,255)); dk.alpha_composite(rgba); o.paste(dk,(600,200))
    o.save(S)
