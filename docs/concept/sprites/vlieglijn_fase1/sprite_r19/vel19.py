import sys; sys.path.insert(0,'sprite_r14')
from lib import *
r18=Image.open('sprite_r18/vlieg_r18.png'); P={n:Image.open('sprite_r19/vlieg_r19_%s.png'%n) for n in ('p1','p2')}
def lab(img,t):
    c=Image.new('RGB',(img.width,img.height+18),'white'); c.paste(img,(0,18)); ImageDraw.Draw(c).text((4,3),t,fill=(0,0,0)); return c
def rij(tiles,gap=10,bg='white'):
    w=sum(t.width for t in tiles)+gap*(len(tiles)-1); h=max(t.height for t in tiles)
    c=Image.new('RGB',(w,h),bg); x=0
    for t in tiles: c.paste(t,(x,0)); x+=t.width+gap
    return c
box=(4,14,60,62); big=lambda m: onbg(m).crop(box).resize((448,384),Image.NEAREST)
r1=rij([lab(big(P['p1']),'r19 p1 (+1)'),lab(big(P['p2']),'r19 p2 (+2)'),lab(big(r18),'r18')])
def een(im,col,s=1):
    a=rgba(im); bg=Image.new('RGBA',a.size,col+(255,)); bg.alpha_composite(a); return bg.convert('RGB').resize((64*s,64*s),Image.NEAREST)
ms=[P['p1'],P['p2'],r18]
r2=lab(rij([een(m,(248,248,240)) for m in ms]+[een(m,(40,48,64)) for m in ms],6,(200,200,200)),'1x licht/donker: p1, p2, r18')
rows=[r1,r2]; W=max(r.width for r in rows); H=sum(r.height for r in rows)+20*len(rows)
vel=Image.new('RGB',(W,H),'white'); y=0
for r in rows: vel.paste(r,(0,y)); y+=r.height+20
vel.save('sprite_r19/vel.png')
def voeten(im):
    a=im.load(); xs=sorted({x for x in range(64) for y in range(50,62) if a[x,y] in (8,14,15)})
    grp=[];
    for x in xs:
        if grp and x-grp[-1][-1]<=1: grp[-1].append(x)
        else: grp.append([x])
    return [(g[0],g[-1]) for g in grp]
b0=r18.load()
for n,im in [('r18',r18)]+list(P.items()):
    v=voeten(im); m=[(a+b)/2 for a,b in v]
    print(n,'voeten',v,'afstand middens',[round(m[i+1]-m[i],1) for i in range(len(m)-1)])
    if n!='r18':
        a=im.load(); d=[(x,y) for x in range(64) for y in range(64) if a[x,y]!=b0[x,y]]
        print('  diff',len(d),'buiten voorpoten (x8-28,y39-57):',[p for p in d if not (8<=p[0]<=28 and 39<=p[1]<=57)])
