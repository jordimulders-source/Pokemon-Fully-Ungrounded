import sys; sys.path.insert(0,'sprite_r14')
from lib import *
r13=Image.open('sprite_r13/vlieg_r13.png')
C=['A_L1','A_L2','B_L1','B_L2']
ims={n:Image.open('sprite_r14/vlieg_r14_%s.png'%n) for n in C}
def lab(img,t):
    c=Image.new('RGB',(img.width,img.height+18),'white'); c.paste(img,(0,18)); ImageDraw.Draw(c).text((4,3),t,fill=(0,0,0)); return c
def rij(tiles,gap=10,bg='white'):
    w=sum(t.width for t in tiles)+gap*(len(tiles)-1); h=max(t.height for t in tiles)
    c=Image.new('RGB',(w,h),bg); x=0
    for t in tiles: c.paste(t,(x,0)); x+=t.width+gap
    return c
box=(4,14,60,62)
r1=rij([lab(onbg(r13).crop(box).resize((448,384),Image.NEAREST),'r13')]+[lab(onbg(ims[n]).crop(box).resize((448,384),Image.NEAREST),'r14 '+n) for n in C])
kb=(6,17,26,40)
r2=rij([lab(zoom(r13,kb,12,False),'kop r13 (12x)'),lab(zoom(ims['A_L1'],kb,12,False),'kop L1 (12x)'),lab(zoom(ims['A_L2'],kb,12,False),'kop L2 (12x)')])
rb=(13,39,46,51)
r3=rij([lab(zoom(r13,rb,12,False),'ringen r13 (12x)'),lab(zoom(ims['A_L1'],rb,12,False),'ringen A (12x)'),lab(zoom(ims['B_L1'],rb,12,False),'ringen B (12x)')])
def een(im,col):
    a=rgba(im); bg=Image.new('RGBA',a.size,col+(255,)); bg.alpha_composite(a); return bg.convert('RGB')
lt=[een(m,(248,248,240)) for m in [r13]+[ims[n] for n in C]]
dk=[een(m,(40,48,64)) for m in [r13]+[ims[n] for n in C]]
r4=lab(rij(lt+dk,6,(200,200,200)),'1x op licht en donker: r13, A_L1, A_L2, B_L1, B_L2')
rows=[r1,r2,r3,r4]
W=max(r.width for r in rows); H=sum(r.height for r in rows)+20*len(rows)
vel=Image.new('RGB',(W,H),'white'); y=0
for r in rows: vel.paste(r,(0,y)); y+=r.height+20
vel.save('sprite_r14/vel.png')
