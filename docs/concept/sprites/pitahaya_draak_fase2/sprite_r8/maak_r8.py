# Pitahaya-draak fase 2, r8 op r7A en r7B. Jordi: "wacht, de vorm van de bek klopt ook niet. Ik heb vier pixels ingestipt,
# wat als die weggehaald worden om de binnenkant wat diagonaler te maken? Zoals in het model" · "en dan de rest netjes bijkleuren".
# Stippen (eigen meting op feedback/jordi_r7_vier_pixels.png, 1 spritepx = 11,6 schermpx, geijkt op pit (11,44)):
#   (9,45) (9,46) (9,47) (10,46) -> transparant (Jordi's silhouetwijziging).
# Bijkleuren (randregel Gen 3): nieuwe rand dicht met 1 px lijn.
#   bovenkant V (onderkant bovenkaak, schaduwkant): (9,44) r->K, (10,45) v->K, punt (11,46) v->K
#     (model: zwarte lijn van de tweede tand schuin naar rechtsonder, natief nx 29-30 ny 91-95; Croconaw: bekrand onder de bovenkaak zwart)
#   onderkant V (bovenkant lipband onderkaak, lichtkant): (10,47) r blijft (selout), (9,48) p->r (selout; lichte tint niet op de rand)
import numpy as np; from PIL import Image
WEG=[(9,45),(9,46),(9,47),(10,46)]
ZET=[(9,44,1,'bovenrand V: lijn zwart (schaduwkant)'),(10,45,1,'bovenrand V: lijn zwart'),(11,46,1,'punt V: lijn zwart'),
     (9,48,3,'onderrand V: selout r (lipband)'),
     (10,48,11,'pit van de rand af: modelpit ligt precies op de grens X10|X11 (blok X10 rechterkolom, X11 linkerkolom 3 pitpx)'),
     (11,48,12,'pit 1 px naar rechts, zelfde modelpit (component 913), niet meer tegen de nieuwe rand')]
N='.KdrpPgGhHwWsvx'
for v in 'AB':
    R=Image.open(f'pitahaya2_r7{v}.png'); r7=np.asarray(R).astype(int); o=r7.copy(); log=[]
    for x,y in WEG: log.append((x,y,N[o[y,x]],'.','Jordi: weghalen (transparant)')); o[y,x]=0
    for x,y,c,why in ZET:
        if o[y,x]!=c: log.append((x,y,N[o[y,x]],N[c],why)); o[y,x]=c
    p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(R.getpalette()); p.save(f'pitahaya2_r8{v}.png',transparency=0)
    d=list(zip(*np.where(o!=r7)))
    assert all(2<=x<=22 and 40<=y<=56 for y,x in d)
    sil=sorted((x,y) for y,x in zip(*np.where((o>0)!=(r7>0)))); assert sil==sorted(WEG),sil
    # rand dicht: elke figuurpixel naast transparant in de bekzone is lijn (K) of selout (d/r)
    for y in range(41,52):
        for x in range(6,16):
            if o[y,x] and any(o[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))):
                assert o[y,x] in (1,2,3,11), ('open rand',x,y,N[o[y,x]])   # 11: tand (4,43)/(8,43)
    # dambord
    for y in range(41,52):
        for x in range(6,14):   # (16,43)/(17,44) lijn-tegen-vulling, bestond al (keuring_r5)
            q=o[y:y+2,x:x+2]; assert not (q[0,0]==q[1,1]!=q[0,1]==q[1,0] and 0 not in q), (v,'dambord',x,y)
    print(f'r8{v}: gewijzigd {len(d)} (alle in de bekzone; buiten 0), silhouet alleen de 4 gestipte px')
    for y in range(42,52): print(' ',y,''.join(N[o[y,x]] for x in range(5,18)))
    open(f'pitahaya2_r8{v}_afwijkingen.txt','w').write('\n'.join('\t'.join(map(str,l)) for l in log)+'\n')
