import sys; sys.path.insert(0,'sprite_r14')
from lib import *
r13=Image.open('sprite_r13/vlieg_r13.png'); r14=Image.open('sprite_r14/vlieg_r14_A_L2.png'); r15=Image.open('sprite_r15/vlieg_r15_A_L2.png')
model=Image.open('sprite_r3/model_zelfde_schaal.png').convert('RGB')
def lab(img,t):
    c=Image.new('RGB',(img.width,img.height+18),'white'); c.paste(img,(0,18)); ImageDraw.Draw(c).text((4,3),t,fill=(0,0,0)); return c
def rij(tiles,gap=10,bg='white'):
    w=sum(t.width for t in tiles)+gap*(len(tiles)-1); h=max(t.height for t in tiles)
    c=Image.new('RGB',(w,h),bg); x=0
    for t in tiles: c.paste(t,(x,0)); x+=t.width+gap
    return c
box=(4,14,60,62)
big=lambda m: onbg(m).crop(box).resize((448,384),Image.NEAREST)
r1=rij([lab(big(r15),'r15 A_L2 (8x)'),lab(big(r14),'r14 A_L2'),lab(big(r13),'r13')])
kb=(6,17,26,40)
r2=rij([lab(zoom(m,kb,12,False),t) for m,t in ((r15,'kop r15 (12x)'),(r14,'kop r14'),(r13,'kop r13'))]+[lab(model.crop((0,0,22,24)).resize((264,288),Image.NEAREST),'model (zelfde schaal)')])
ob=(12,22,26,36)
r3=rij([lab(zoom(m,ob,12,False),t) for m,t in ((r15,'rechteroog r15 (12x)'),(r14,'r14'),(r13,'r13'))])
jb=(14,34,54,50)
r4=rij([lab(zoom(m,jb,12,False),t) for m,t in ((r15,'aansluiting poten r15 (12x)'),(r14,'r14'))])
def een(im,col):
    a=rgba(im); bg=Image.new('RGBA',a.size,col+(255,)); bg.alpha_composite(a); return bg.convert('RGB')
r5=lab(rij([een(m,(248,248,240)) for m in (r15,r14,r13)]+[een(m,(40,48,64)) for m in (r15,r14,r13)],6,(200,200,200)),'1x licht/donker: r15, r14, r13')
rows=[r1,r2,r3,r4,r5]
W=max(r.width for r in rows); H=sum(r.height for r in rows)+20*len(rows)
vel=Image.new('RGB',(W,H),'white'); y=0
for r in rows: vel.paste(r,(0,y)); y+=r.height+20
vel.save('sprite_r15/vel.png')
# diff-bewijs t.o.v. r14 A_L2
a=r15.load(); b=r14.load()
d=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b[x,y]]
oog=[p for p in d if 9<=p[0]<=22 and 27<=p[1]<=34]; rest=[p for p in d if p not in oog]
print('diff r14->r15:',len(d),'oog',len(oog),'poten/onderrand',rest)
print('indexen',sorted(set(r15.getdata())),'transp',r15.info.get('transparency'))
