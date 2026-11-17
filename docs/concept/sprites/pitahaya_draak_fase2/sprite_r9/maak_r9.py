# Pitahaya-draak fase 2, r9 op r8A/r8B. Jordi: "veel beter, maar het zwart van de mondhoek moet dan roze worden" ·
# "zodat de kleur consistent is" · (op de vraag V links of mondhoek achterin:) "de mondhoek".
# Hoofd (r9A/r9B): zwarte bovenrand van de V (9,44) (10,45) (11,46) -> r, dezelfde selout als de onderrand van de V
#   ((10,47) r, (9,48) r): de lipband rondom de insnijding heeft dan één kleur.
# Variant achter (r9A_achter, op r8A): zwart in de mondhoek achterin (17,43) -> r, (18,43) -> p (onderkant bovenlip, zoals (14-16,43) r
#   en de mondhoek (17,44) r); de kaaklijn (14-16,44) blijft lijn. De V blijft zwart.
import numpy as np; from PIL import Image
N='.KdrpPgGhHwWsvx'
JOBS=[('pitahaya2_r8A.png','pitahaya2_r9A.png',[(9,44,3),(10,45,3),(11,46,3)],'V-bovenrand zwart -> selout r (lipband)'),
      ('pitahaya2_r8B.png','pitahaya2_r9B.png',[(9,44,3),(10,45,3),(11,46,3)],'V-bovenrand zwart -> selout r (lipband)'),
      ('pitahaya2_r8A.png','pitahaya2_r9A_achter.png',[(17,43,3),(18,43,4)],'mondhoek achterin zwart -> roze (17,43) r zoals (14-16,43); (18,43) p zoals buren (18,42)/(19,43), r gaf dambord met (19,42)')]
for bron,uit,px,why in JOBS:
    R=Image.open(bron); r8=np.asarray(R).astype(int); o=r8.copy(); log=[]
    for x,y,c in px: assert o[y,x]==1; log.append((x,y,'K',N[c],why)); o[y,x]=c
    p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(R.getpalette()); p.save(uit,transparency=0)
    d=set((x,y) for y,x in zip(*np.where(o!=r8))); assert d==set((x,y) for x,y,c in px); assert ((o>0)==(r8>0)).all()
    assert all(2<=x<=22 and 40<=y<=56 for x,y in d)
    for y in range(41,50):
        for x in range(6,20):
            q=o[y:y+2,x:x+2]
            if (x,y) in ((16,43),): continue          # lijn-tegen-vulling bij de mondhoek, bestond al (keuring_r5)
            assert not (q[0,0]==q[1,1]!=q[0,1]==q[1,0] and 0 not in q), (uit,'dambord',x,y)
    # bek dicht: figuurpixel naast transparant is lijn/selout/tand
    for y in range(41,52):
        for x in range(6,16):
            if o[y,x] and any(o[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): assert o[y,x] in (1,2,3,11),(uit,x,y)
    # wig/plooi (v/x) grenst nergens direct aan lichtroze p/P
    for y in range(42,48):
        for x in range(8,16):
            if o[y,x] in (13,14): assert all(o[y+dy,x+dx] not in (4,5) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))),(uit,x,y)
    print(uit,'gewijzigd',len(d),'(buiten de bekzone 0, silhouet gelijk)')
    for y in range(42,49): print(' ',y,''.join(N[o[y,x]] for x in range(7,20)))
    open(uit[:-4]+'_afwijkingen.txt','w').write('\n'.join('\t'.join(map(str,l)) for l in log)+'\n')
