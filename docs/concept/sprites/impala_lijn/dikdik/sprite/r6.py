# r6 = r5 + reparaties eindkeuring (BIJNA) + kleurvariant r6_licht (zelfde pixels, alleen palet).
# Lokaal = absoluut - (10,6). Diff 0 buiten de genoemde pixels (bewezen).
import json, numpy as np
from collections import Counter
from PIL import Image
src=json.load(open('r5/grid.json')); OX,OY=src['OX'],src['OY']; R=src['grid']
g=[list(r) for r in R]; H=len(g); W=len(g[0]); log=[]; toegestaan=set()
def put(z,ax,ay,c,why):   # absolute coordinaten
    x,y=ax-OX,ay-OY; toegestaan.add((x,y))
    if g[y][x]!=c: log.append((z,ax,ay,g[y][x],c,why)); g[y][x]=c
# 1 linkeroor linkerrand
put('1 oorrand',12,15,'D','D loopt door tot (13,16); zwart vanaf (13,17)')
# 2 hals/borst linkerrand
put('2 borstrand',25,38,'D','selout lichtkant, geen om-en-om')
put('2 borstrand',28,45,'0','onderkant borst zwart, geen om-en-om')
# 3 linkeroor tinten uit de kale reductie
for ax,ay in [(14,11),(13,12),(14,12),(15,12),(13,13),(16,13),(13,14),(16,14),(17,14),(13,15),(14,16),(16,16),(16,17)]:
    put('3 oor',ax,ay,'M','tint kale reductie')
put('3 oor',17,15,'S','tint kale reductie')
# 4 kuif bovenop: strengen M als doorlopende lijntjes (kale reductie M op (21,17),(23,17),(27,17),(20-21,18),(25-27,18),(20,19),(24-26,19));
#   S-pixels van de kale reductie (22,17),(26,17) zouden losse spikkels van 1 px worden -> M, zodat elke streng >=3 px is; D (24,17) blijft lijn
for ax,ay in [(21,17),(22,17),(23,17),(26,17),(27,17),(20,18),(21,18),(25,18),(26,18),(27,18),(20,19),(24,19),(25,19),(26,19)]:
    put('4 kuif',ax,ay,'M','streng uit kale reductie/model')
# KAN: lichtkant van staarttopje en oortopje
put('KAN toppen',50,29,'D','staarttopje lichtkant: selout')
put('KAN toppen',13,9,'D','oortopje lichtkant: selout')
# KAN: speerschachten linkerlijn in donkere houttint w (outline base van het hout) i.p.v. lijf-D
for lx,ly in [(12,7),(11,8),(10,9),(10,10),(22,9),(22,10),(21,11),(20,12),(19,13),(18,14),(17,15)]:
    put('KAN schacht',lx+OX,ly+OY,'w','linkerlijn schacht in donker hout')
buiten=sum(1 for y in range(H) for x in range(W) if g[y][x]!=R[y][x] and (x,y) not in toegestaan)
print('diff buiten genoemde pixels:',buiten,'| per zone:',dict(Counter(z for z,*_ in log)),'totaal',len(log))
BASIS={'.':(0,0,0),'0':(24,16,20),'D':(66,34,18),'S':(108,58,26),'M':(160,92,40),'L':(194,120,56),'C':(244,221,190),'c':(212,174,132),
     'N':(106,76,64),'n':(140,110,94),'H':(132,102,70),'h':(184,148,106),'I':(62,66,78),'J':(86,92,104),'K':(110,116,128),'w':(92,68,44)}
LICHT=dict(BASIS); LICHT.update({'D':(104,54,26),'S':(154,84,36),'M':(200,120,52),'L':(234,160,86),
     'I':(58,62,74),'J':(90,96,108),'K':(122,128,140),'w':(100,74,48)})
lum=lambda c:0.299*c[0]+0.587*c[1]+0.114*c[2]
ORDER=list(BASIS)
for naam,PAL in [('dikdik_r6',BASIS),('dikdik_r6_licht',LICHT)]:
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
    pal=[]; [pal.extend(PAL[k]) for k in ORDER]
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(f'r6/{naam}.png',transparency=0)
    Image.open(f'r6/{naam}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'r6/{naam}_8x.png')
    print(naam,'lum D S M L:',[round(lum(PAL[k])) for k in 'DSML'],'ijzer I J K:',[round(lum(PAL[k])) for k in 'IJK'],'zwart',round(lum(PAL['0'])))
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g]},open('r6/grid.json','w'),indent=0)
with open('r6/log.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
# keuzevel: beide op 8x en 1x naast elkaar + Eevee/Vulpix _gba op 1x
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def gba(n):
    im=Image.open(G+n+'/anim_front_gba.png').crop((0,0,64,64)); im.info['transparency']=0; return im.convert('RGBA')
A=Image.open('r6/dikdik_r6.png').convert('RGBA'); B=Image.open('r6/dikdik_r6_licht.png').convert('RGBA')
V=Image.new('RGBA',(512*2+30,512+110),(236,236,236,255))
for i,s in enumerate([A,B]): t=s.resize((512,512),Image.NEAREST); V.paste(t,(10+i*522,10),t)
x=10
for s in [A,B,gba('eevee'),gba('vulpix')]:
    for bg in [(248,248,248,255),(40,40,48,255)]:
        t=Image.new('RGBA',(72,72),bg); t.paste(s,(4,4),s); V.paste(t,(x,530)); x+=80
V.save('r6/keuze.png')
