# Pitahaya-draak fase 2, r6 op r5. Jordi: "kan dat roze in de bek ook een andere kleur? een donkerdere tint van wit/grijs
# wat we nu aan het doen zijn? dan ziet dat er natuurlijker uit".
# Roze BINNEN de bek (verre lip) -> donkergrijs v (155,154,159). Opbouw naar Gen 3 (Exploud: donkere lijn waar tong/plooi
# overlapt): wig wordt grijs w (191, de modeltoon van de wig), verre lip v, tong W/w. Lipbanden buiten blijven roze.
# --B: ook de twee twijfelpixels (9,45) en (10,47) (waar de verre lip in de buitenste lipband overgaat) -> v.
import sys,numpy as np; from PIL import Image
B='--B' in sys.argv; UIT='pitahaya2_r6B.png' if B else 'pitahaya2_r6.png'
R=Image.open('pitahaya2_r5.png'); r5=np.asarray(R).astype(int); pal=R.getpalette(); o=r5.copy(); log=[]
N={0:'.',1:'K',2:'d',3:'r',4:'p',5:'P',10:'w',11:'W',12:'s',13:'v'}; I={v:k for k,v in N.items()}
def zet(X,Y,c,reden):
    if o[Y,X]!=I[c]: log.append((X,Y,N[o[Y,X]],c,reden)); o[Y,X]=I[c]
for X,Y in ((10,45),(10,46),(11,46),(12,45),(13,45)): zet(X,Y,'v','verre lip (roze binnen de bek) -> donkergrijs')
for X,Y in ((10,43),(11,43),(10,44),(12,44),(13,44),(11,45)): zet(X,Y,'w','wig v -> w (modeltoon wig 187), zodat de verre lip de donkerste is')
# KEURING_r5 punt 2 (bovenlip trap 7-4-3, naar Croconaw/Gyarados): lijn zakt al na de tweede tand. Wijkt af van het model
# (blok (10,42): 3 zwart onderin; (10,43)/(11,43): 0-1 zwart) -- keurdersreparatie, op Jordi's vrijgave om naar Gen 3 te kijken.
for X,Y in ((10,43),(11,43)): zet(X,Y,'K','keuring_r5 punt 2: kaaklijn zakt naar rij 43 (trap 7-4-3; model: geen zwart, wig)')
for X,Y in ((10,42),(11,42)): zet(X,Y,'r','keuring_r5 punt 2: roze bovenkaak boven de gezakte lijn (tint als (14-16,43); model: '+('3 zwart onderin' if X==10 else '1 zwart')+')')
if B:
    for X,Y in ((9,45),(10,47)): zet(X,Y,'v','twijfel: aansluiting verre lip op buitenste lipband -> donkergrijs')
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
diff=list(zip(*np.where(o!=r5)))
BEK=lambda y,x: 9<=x<=13 and 42<=y<=47
assert all(BEK(y,x) for y,x in diff); assert ((o>0)==(r5>0)).all()
# dambord-check (2x2 met twee tinten om en om) en losse pixels in de bekzone
for y in range(42,52):
    for x in range(7,18):
        q=o[y:y+2,x:x+2]
        assert not (q[0,0]==q[1,1]!=q[0,1]==q[1,0] and q[0,0] in (10,11,13) and q[0,1] in (10,11,13)), ('dambord',x,y)
# wig sluit: elke wigpixel heeft alleen wig/pit/K/v als 4-buren
WIG={(10,44),(11,44),(12,44),(13,44),(11,45)}
for X,Y in WIG:
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(X+dx,Y+dy); v=o[n[1],n[0]]
        assert n in WIG or v in (1,13) or (n==(9,44)), ('wig open',X,Y,n,v)
print(UIT,'gewijzigd t.o.v. r5',len(diff),'(alle binnen x9-13,y42-47; buiten 0; silhouet gelijk; wig gesloten)')
open(UIT[:-4]+'_afwijkingen.txt','w').write('\n'.join('\t'.join(map(str,l)) for l in log)+'\n')
a=o; Nn='.KdrpPgGhHwWsv'
for y in range(42,50): print(y,''.join(Nn[a[y,x]] for x in range(6,20)))
