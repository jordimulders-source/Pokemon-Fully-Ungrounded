import sys; sys.path.insert(0,'sprite_r14')
from lib import *
import numpy as np
r17=Image.open('sprite_r17/vlieg_r17.png'); r18=Image.open('sprite_r18/vlieg_r18.png')
def lab(img,t):
    c=Image.new('RGB',(img.width,img.height+18),'white'); c.paste(img,(0,18)); ImageDraw.Draw(c).text((4,3),t,fill=(0,0,0)); return c
def rij(tiles,gap=10,bg='white'):
    w=sum(t.width for t in tiles)+gap*(len(tiles)-1); h=max(t.height for t in tiles)
    c=Image.new('RGB',(w,h),bg); x=0
    for t in tiles: c.paste(t,(x,0)); x+=t.width+gap
    return c
box=(4,14,60,62); big=lambda m: onbg(m).crop(box).resize((448,384),Image.NEAREST)
r1=rij([lab(big(r18),'r18 (8x)'),lab(big(r17),'r17')])
# krabbel registreren: schaal 15.25, oorsprong = spritepixel (22,37) (foutloos gematcht)
k=np.array(Image.open('sprite_r17/krabbel_jordi_r17.png').convert('RGB')).astype(int)
red=(k[:,:,0]>180)&(k[:,:,1]<80)&(k[:,:,2]<80); ys,xs=np.nonzero(red); S=15.25
gb=(22,32,54,48); Z=12
def over(m):
    ov=zoom(m,gb,Z,False); d=ImageDraw.Draw(ov)
    for x,y in zip(xs,ys):
        X=(x/S+22-gb[0])*Z; Y=(y/S+37-gb[1])*Z; d.point((X,Y),fill=(255,0,0))
    return ov
r2=rij([lab(over(r17),'r17 + krabbellijn Jordi (12x)'),lab(over(r18),'r18 + krabbellijn (12x)'),lab(zoom(r18,gb,Z,False),'r18 zonder lijn')])
def een(im,col,s=1):
    a=rgba(im); bg=Image.new('RGBA',a.size,col+(255,)); bg.alpha_composite(a); return bg.convert('RGB').resize((64*s,64*s),Image.NEAREST)
t=[]
for s in (1,2):
    for col in ((248,248,240),(40,48,64)):
        t+= [een(r18,col,s),een(r17,col,s)]
r3=lab(rij(t,6,(200,200,200)),'1x en 2x op licht/donker: telkens r18, r17')
rows=[r1,r2,r3]; W=max(r.width for r in rows); H=sum(r.height for r in rows)+20*len(rows)
vel=Image.new('RGB',(W,H),'white'); y=0
for r in rows: vel.paste(r,(0,y)); y+=r.height+20
vel.save('sprite_r18/vel.png')
a=r18.load(); b=r17.load()
dd=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b[x,y]]
print('diff',len(dd),sorted(dd)); print('buiten zones (achterlijf x35-45 y39-45, borststuk x30-34 y37-40):',[p for p in dd if not ((35<=p[0]<=45 and 39<=p[1]<=45) or (30<=p[0]<=34 and 37<=p[1]<=40))])
print('pal gelijk',r18.getpalette()[:48]==r17.getpalette()[:48],r18.info.get('transparency'))
