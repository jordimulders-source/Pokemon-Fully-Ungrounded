import sys; sys.path.insert(0,'sprite_r14')
from lib import *
r15=Image.open('sprite_r15/vlieg_r15_A_L2.png')
C=['O1_P1','O1_P2','O2_P1','O2_P2']; ims={n:Image.open('sprite_r16/vlieg_r16_%s.png'%n) for n in C}
def lab(img,t):
    c=Image.new('RGB',(img.width,img.height+18),'white'); c.paste(img,(0,18)); ImageDraw.Draw(c).text((4,3),t,fill=(0,0,0)); return c
def rij(tiles,gap=10,bg='white'):
    w=sum(t.width for t in tiles)+gap*(len(tiles)-1); h=max(t.height for t in tiles)
    c=Image.new('RGB',(w,h),bg); x=0
    for t in tiles: c.paste(t,(x,0)); x+=t.width+gap
    return c
box=(4,14,60,62); big=lambda m: onbg(m).crop(box).resize((448,384),Image.NEAREST)
r1=rij([lab(big(r15),'r15 (8x)')]+[lab(big(ims[n]),'r16 '+n) for n in C])
kb=(6,22,24,38)
r2=rij([lab(zoom(r15,kb,12,False),'kop r15 (12x)'),lab(zoom(ims['O1_P1'],kb,12,False),'kop O1'),lab(zoom(ims['O2_P1'],kb,12,False),'kop O2')])
pb=(14,32,50,46)
r3=rij([lab(zoom(r15,pb,12,False),'onderrand r15 (12x)'),lab(zoom(ims['O1_P1'],pb,12,False),'P1'),lab(zoom(ims['O1_P2'],pb,12,False),'P2')])
def een(im,col):
    a=rgba(im); bg=Image.new('RGBA',a.size,col+(255,)); bg.alpha_composite(a); return bg.convert('RGB')
ms=[r15]+[ims[n] for n in C]
r4=lab(rij([een(m,(248,248,240)) for m in ms]+[een(m,(40,48,64)) for m in ms],6,(200,200,200)),'1x licht/donker: r15, O1_P1, O1_P2, O2_P1, O2_P2')
rows=[r1,r2,r3,r4]; W=max(r.width for r in rows); H=sum(r.height for r in rows)+20*len(rows)
vel=Image.new('RGB',(W,H),'white'); y=0
for r in rows: vel.paste(r,(0,y)); y+=r.height+20
vel.save('sprite_r16/vel.png')
# diff-bewijs t.o.v. r15 (index 7 van r15 telt als 3: paletsamenvoeging)
a15=r15.load()
for n in C:
    a=ims[n].load(); d=[]
    for x in range(64):
        for y in range(64):
            o=a15[x,y]; o=3 if o==7 else o
            if a[x,y]!=o: d.append((x,y))
    oog=[p for p in d if 8<=p[0]<=22 and 27<=p[1]<=35]
    rand=[p for p in d if 21<=p[0]<=41 and 37<=p[1]<=41]
    buiten=[p for p in d if p not in oog and p not in rand]
    print(n,'diff',len(d),'oog',len(oog),'onderrand/aanzet',len(rand),'BUITEN',buiten)
print('samengevoegd 7->3:',sum(1 for x in range(64) for y in range(64) if a15[x,y]==7),'px (kabels, donkere kant)')
