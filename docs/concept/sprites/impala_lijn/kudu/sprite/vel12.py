# Ronde 12: r12/kudu_r12.png (+_8x), r12/vel.png (r12 | r10 B6a op 8x; 1x op licht en donker naast de impala), r12/telling.txt
import r12, r12_check as C, r8lib as L, json
from PIL import Image, ImageDraw
G,B=r12.G,r12.B6A
L.png(G,'r12/kudu_r12.png'); L.rgba8(G).resize((512,512),0).save('r12/kudu_r12_8x.png')
json.dump({'grid':G},open('r12/grid.json','w'))
with open('r12/telling.txt','w') as f:
    f.write('Rechte lijnstukken >3 px (0/d/K naast manen- of franjevulling): B6a %s | r12 %s\n'%(C.rechte(B),C.rechte(G) or 'geen'))
    f.write('Pixels anders dan B6a: %d; buiten manen+franje+halsstrook+1 px rand: %d %s; oogvlak K4: %d\n'%(len(C.diff),len(C.diff-C.ZONE),sorted(C.diff-C.ZONE),len(C.diff&C.OOG)))
    f.write('Tintvlakjes <3 px (l/m/L/M/D, 8-verbonden) rond de wijzigingen: B6a %s | r12 %s\n'%(C.clusters(B,C.OMG) or 'geen',C.clusters(G,C.OMG) or 'geen'))
    f.write('Kleuren incl. transparant: %d\n'%len({c for r in G for c in r}))
    for p in sorted(r12.LOG,key=lambda p:(p[1],p[0])):
        a,b,w=r12.LOG[p]; f.write('  (%d,%d) %s -> %s  %s\n'%(p[0],p[1],a,b,w))
imp=Image.open('../../impala/af/impala.png').convert('RGBA')
Z8=512; V=Image.new('RGB',(2*Z8+30,Z8+200),'white'); d=ImageDraw.Draw(V)
for i,(t,g) in enumerate([('r12 (8x)',G),('r10 B6a (8x)',B)]):
    V.paste(L.rgba8(g).resize((Z8,Z8),0),(10+i*(Z8+10),24)); d.text((10+i*(Z8+10),6),t,fill=(0,0,0))
y=Z8+50; d.text((10,y-16),'1x op licht en donker: r12 | r10 B6a | impala (af)',fill=(0,0,0))
for j,bg in enumerate([(255,255,255),(40,44,52)]):
    x=10+j*330; V.paste(Image.new('RGB',(310,130),bg),(x,y))
    for k,g in enumerate([G,B]): V.paste(L.rgba8(g,bg),(x+10+k*95,y+40))
    bgim=Image.new('RGBA',imp.size,bg+(255,)); bgim.alpha_composite(imp); V.paste(bgim.convert('RGB'),(x+10+2*95,y+40))
V.save('r12/vel.png'); print(open('r12/telling.txt').read())
