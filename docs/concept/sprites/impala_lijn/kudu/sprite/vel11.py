# Ronde 11: r11/kudu_r11.png (+_8x), r11/vel.png (r11 | r10 B6b op 8x; 1x licht/donker naast de impala), r11/telling.txt
import r11, r8lib as L, vel8, json
from PIL import Image, ImageDraw
G=r11.G; Z=r11.ZONE
L.png(G,'r11/kudu_r11.png'); L.rgba8(G).resize((512,512),0).save('r11/kudu_r11_8x.png')
json.dump({'grid':G},open('r11/grid.json','w'))
B6B=[''.join(r) for r in r11.B6B]
diff={(x,y) for y in range(L.H) for x in range(L.W) if G[y][x]!=vel8.REF[y][x]}
d10={(x,y) for y in range(L.H) for x in range(L.W) if G[y][x]!=B6B[y][x]}
REG={(x,y) for x,y in Z if G[y][x] in 'd0K'}
R10={(x,y) for x,y in Z if B6B[y][x] in 'd0K'}
with open('r11/telling.txt','w') as f:
    f.write('Pixels anders dan r6+K4: %d; buiten manen+nek+halsstrook-zone: %d %s; oogvlak: %d\n'%(len(diff),len(diff-Z),sorted(diff-Z),len(diff&vel8.OOG)))
    f.write('Pixels anders dan r10 B6b: %d\n'%len(d10))
    f.write('Rechte lijnstukken (d/0/K) > 3 px in manen/nek/franje/halsstrook-zone: r11 %s; r10 B6b %s\n'%(L.rechte(G,REG) or 'geen',L.rechte(B6B,R10)))
    f.write('Kleuren incl. transparant: %d\n'%len(set(c for r in G for c in r)))
    for p in sorted(r11.LOG,key=lambda p:(p[1],p[0])):
        if p in d10: f.write('  (%d,%d) %s -> %s  %s\n'%(p[0],p[1],B6B[p[1]][p[0]],G[p[1]][p[0]],r11.LOG[p]))
imp=Image.open('../../impala/af/impala.png').convert('RGBA')
Z8=512; V=Image.new('RGB',(2*Z8+30,Z8+200),'white'); d=ImageDraw.Draw(V)
for i,(t,g) in enumerate([('r11 (8x)',G),('r10 B6b (8x)',B6B)]):
    V.paste(L.rgba8(g).resize((Z8,Z8),0),(10+i*(Z8+10),24)); d.text((10+i*(Z8+10),6),t,fill=(0,0,0))
y=Z8+50; d.text((10,y-16),'1x op licht en donker: r11 | r10 B6b | impala (af)',fill=(0,0,0))
for j,bg in enumerate([(255,255,255),(40,44,52)]):
    x=10+j*330; V.paste(Image.new('RGB',(310,130),bg),(x,y))
    for k,g in enumerate([G,B6B]): V.paste(L.rgba8(g,bg),(x+10+k*95,y+40))
    bgim=Image.new('RGBA',imp.size,bg+(255,)); bgim.alpha_composite(imp); V.paste(bgim.convert('RGB'),(x+10+2*95,y+40))
V.save('r11/vel.png'); print(open('r11/telling.txt').read()[:600])
