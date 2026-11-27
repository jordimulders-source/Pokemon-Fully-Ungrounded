# Ronde 7: alleen de MANEN (keelfranje + nekmanen + kam) opnieuw als losse lokken, opgebouwd zoals Growlithe/Arcanine.
# Start: r6/grid.json (oog B). Rastercoordinaten (beeld x = raster x + 6). Buiten de manenzone: pixeldiff 0 (bewezen onderaan).
# Lijnen (d) en omtrek (0) liggen op de gemeten modellijnen van model A3 (zie r7/NOTITIES.md, tabel "lijnen").
# Opbouw per lok (Arcanine/Growlithe): eigen omtrek, lichtkant selout d, schaduwkant zwart 0; binnenlijn d (donkerste eigen
# tint) waar lok over lok valt; licht l aan de lichtkant (links/boven), m aan de schaduwkant en in de schaduw onder kop/hals.
import json, sys, numpy as np
from PIL import Image
sys.path.insert(0,'.')
J=json.load(open('r6/grid.json')); R6=[list(r) for r in J['grid']]; kaal=J['kaal']; g=[r[:] for r in R6]
EDIT={  # rij: (begin-x, tekens)  '?' = laten zoals r6
 25:(14,'DdmmD0'),
 26:(14,'Ddmmdm0d'),
 27:(13,'Dmdlmdmmmdlllmd00'),
 28:(13,'MMdmmdmmmmmddlll0'),
 29:(12,'MMMdlmdmmmdllmmmdd0'),
 30:(13,'MMdlmdllmdmddlllmm00'),
 31:( 9,'0mm0MMdllmdlldllm000000'),
 32:( 9,'dlm0MMdllmdlmdddd0'),
 33:( 9,'dlm0MMdllmdlmdlllm0'),
 34:( 9,'dlm0MMdllmdlmdlllm0'),
 35:( 8,'dlldm0Mdllmdlmdlllm0'),
 36:( 8,'dlldm0MMdlmdlmdllm0'),
 37:( 9,'dldmm0Mdlmdldlllm0'),
 38:( 9,'dldmm0Mdlmdldllmm0'),
 39:( 9,'dlldmm0MMdlmdllm0'),
 40:( 9,'dlldmmm0Mdlmdllm0'),
 41:(10,'0lldmmmmdlm0lm0'),
 42:(10,'0lldmmmmmdm0m0'),
 43:(11,'0lmmmmmmmd?0'),
 44:(11,'00mdmdmmm0'),
 45:(13,'00m0mmdm0'),
 46:(15,'0DD0mm0'),
}
for y,(x0,s) in EDIT.items():
    for i,c in enumerate(s):
        if c!='?': g[y][x0+i]=c
H,W=len(g),len(g[0])
# ---- bewijs: manenzone = haarpixels van r6 (l/m/d, rij 23-47, x<=32) plus 1 ring eromheen; alles daarbuiten diff 0
HAAR={(x,y) for y in range(23,48) for x in range(0,33) if R6[y][x] in 'lmd'}
ZONE={(x+a,y+b) for x,y in HAAR for a in(-1,0,1) for b in(-1,0,1)}
diff={(x,y) for y in range(H) for x in range(W) if g[y][x]!=R6[y][x]}
buiten=diff-ZONE
# ---- uitvoer
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D8AC30'),'m':hx('#B08824'),'d':hx('#7C5A10'),'A':hx('#4A4A52'),'3':hx('#8A8A92'),'4':hx('#C8C8CC'),
     'W':hx('#FFFFFF'),'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL); OX=(64-W)//2; OY=64-H
img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
im=Image.fromarray(img,'P'); im.putpalette(pal); im.save('r7/kudu_r7.png',transparency=0)
Image.open('r7/kudu_r7.png').convert('RGBA').resize((512,512),Image.NEAREST).save('r7/kudu_r7_8x.png')
json.dump({'grid':[''.join(r) for r in g],'kaal':kaal},open('r7/grid.json','w'))
with open('r7/telling.txt','w') as f:
    f.write('Pixels anders dan r6: %d, waarvan buiten de manenzone: %d %s\n'%(len(diff),len(buiten),sorted(buiten)))
    f.write('Manenzone: %d px (r6-haar %d + ring)\n'%(len(ZONE),len(HAAR)))
    f.write('Kleuren in de sprite (incl. transparant): %d\n'%len(set(c for r in g for c in r)))
print(open('r7/telling.txt').read())
if '-v' in sys.argv:
    for y in range(20,49): print('%2d '%y+''.join(g[y][:40]))
