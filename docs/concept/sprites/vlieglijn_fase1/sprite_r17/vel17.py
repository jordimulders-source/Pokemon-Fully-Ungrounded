import sys; sys.path.insert(0,'sprite_r14')
from lib import *
r16=Image.open('sprite_r16/vlieg_r16_O2_P1.png'); r17=Image.open('sprite_r17/vlieg_r17.png')
def lab(img,t):
    c=Image.new('RGB',(img.width,img.height+18),'white'); c.paste(img,(0,18)); ImageDraw.Draw(c).text((4,3),t,fill=(0,0,0)); return c
def rij(tiles,gap=10,bg='white'):
    w=sum(t.width for t in tiles)+gap*(len(tiles)-1); h=max(t.height for t in tiles)
    c=Image.new('RGB',(w,h),bg); x=0
    for t in tiles: c.paste(t,(x,0)); x+=t.width+gap
    return c
box=(4,14,60,62); big=lambda m: onbg(m).crop(box).resize((448,384),Image.NEAREST)
r1=rij([lab(big(r17),'r17 (8x)'),lab(big(r16),'r16 O2_P1')])
pb=(14,32,50,47)
r2=rij([lab(zoom(r17,pb,12,False),'onderrand r17 (12x)'),lab(zoom(r16,pb,12,False),'r16')])
def een(im,col):
    a=rgba(im); bg=Image.new('RGBA',a.size,col+(255,)); bg.alpha_composite(a); return bg.convert('RGB')
r3=lab(rij([een(m,(248,248,240)) for m in (r17,r16)]+[een(m,(40,48,64)) for m in (r17,r16)],6,(200,200,200)),'1x licht/donker: r17, r16')
rows=[r1,r2,r3]; W=max(r.width for r in rows); H=sum(r.height for r in rows)+20*len(rows)
vel=Image.new('RGB',(W,H),'white'); y=0
for r in rows: vel.paste(r,(0,y)); y+=r.height+20
vel.save('sprite_r17/vel.png')
a=r17.load(); b=r16.load()
d=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b[x,y]]
print('diff',len(d),'buiten zone x21-41 y36-42:',[p for p in d if not (21<=p[0]<=41 and 36<=p[1]<=42)])
print('pal gelijk',r17.getpalette()[:48]==r16.getpalette()[:48],'transp',r17.info.get('transparency'))
