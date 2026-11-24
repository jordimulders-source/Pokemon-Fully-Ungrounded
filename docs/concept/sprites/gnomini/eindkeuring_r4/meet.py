# Eindkeuring r4: kaart, 8x-raster en 1x-vergelijkingsvel
import sys
from PIL import Image, ImageDraw
from collections import Counter
D='docs/concept/sprites/gnomini/'
p=Image.open(D+'sprite_r4/gnomini_A.png'); rgb=p.convert('RGB'); bg=rgb.getpixel((0,0))
cols=[c for c,_ in Counter(rgb.getdata()).most_common()]
sym={bg:'.'}; letters='KmMlLnbBrRpPsS'
names={(24,20,32):'K',(112,95,138):'1',(137,119,170):'2',(184,163,211):'3',(205,183,230):'4',
 (172,72,102):'a',(213,102,136):'b',(244,153,181):'c',(251,184,202):'d',
 (56,109,142):'x',(82,148,197):'y',(122,188,232):'z',(170,216,244):'w'}
for y in range(16,60):
    print('%2d '%y+''.join(names.get(rgb.getpixel((x,y)),'.') for x in range(12,52)))
print('   '+''.join(str(x%10) for x in range(12,52)))
# 8x met raster
S=8; big=rgb.resize((64*S,64*S),Image.NEAREST); d=ImageDraw.Draw(big)
for i in range(0,64):
    c=(120,120,120) if i%8 else (255,0,0)
    d.line([(i*S,0),(i*S,64*S)],fill=c); d.line([(0,i*S),(64*S,i*S)],fill=c)
big.save(D+'eindkeuring_r4/gnomini_A_8x_raster.png')
# vergelijking 1x en 3x
refs=['igglybuff','whismur','azurill','smoochum','jigglypuff']
ims=[rgb]
for r in refs:
    for f in ('front.png','anim_front.png'):
        try:
            im=Image.open('graphics/pokemon/%s/%s'%(r,f)).convert('RGB').crop((0,0,64,64)); ims.append(im); break
        except FileNotFoundError: pass
W=64*len(ims)
vel=Image.new('RGB',(W*3,64*3+64+8),(255,255,255))
for i,im in enumerate(ims):
    vel.paste(im.resize((192,192),Image.NEAREST),(i*192,0))
    vel.paste(im,(i*64,192+8))
vel.save(D+'eindkeuring_r4/vergelijk_1x_3x.png')

# clusters < 3 px per kleur (4-buren), buiten zwart
seen=set(); print('kleine clusters:')
for y in range(64):
  for x in range(64):
    c=rgb.getpixel((x,y))
    if c==bg or c==(24,20,32) or (x,y) in seen: continue
    st=[(x,y)]; cl=[]; seen.add((x,y))
    while st:
      a,b=st.pop(); cl.append((a,b))
      for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(a+dx,b+dy)
        if 0<=n[0]<64 and 0<=n[1]<64 and n not in seen and rgb.getpixel(n)==c:
          seen.add(n); st.append(n)
    if len(cl)<3: print(' ',names[c],cl)
# lichte kleur op buitenrand
print('rand (grenst aan achtergrond) per kleur:')
from collections import defaultdict
r=defaultdict(list)
for y in range(64):
  for x in range(64):
    c=rgb.getpixel((x,y))
    if c==bg: continue
    if any(0<=x+dx<64 and 0<=y+dy<64 and rgb.getpixel((x+dx,y+dy))==bg for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
      r[names[c]].append((x,y))
for k,v in r.items(): print(' ',k,len(v),v if k not in 'K' else '')
