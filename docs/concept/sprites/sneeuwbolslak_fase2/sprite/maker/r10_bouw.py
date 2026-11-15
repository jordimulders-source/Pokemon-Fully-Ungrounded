# r10: mond als één glimlachlijn van de snuitpunt naar de lijn onder de wang. Basis raster_r9.txt (bol r9 blijft).
# A = lijn in d; B = lijn in # met d aan de lichtkant (snuitkant). Vanuit sneeuwbolslak_fase2/: python3 sprite/maker/r10_bouw.py
O=[l.rstrip('\n') for l in open('sprite/maker/raster_r9.txt')]
# weg: korte schuine streep + losse pixels (vulling zoals de buren: boven de mond licht, eronder kaak b)
WEG={(9,47):'c',(8,48):'c',(7,49):'b',(8,50):'b',(9,50):'b',(10,50):'b',(11,50):'b',(12,50):'b',(13,50):'b',(17,51):'a',(18,51):'a',(14,52):'a'}  # (14,52) a: anders loopt de mond recht door in de flappernaad (diagonaal 5 px)
# mondlijn: trappen 2-3-3-3-3, taps aan de snuitpunt; sluit via (19,50)(20,49)(20,48) aan op de bestaande lijn
LIJN=[(6,48),(7,48),(8,49),(9,49),(10,49),(11,50),(12,50),(13,50),(14,51),(15,51),(16,51),(17,50),(18,50)]
TAPS=(5,48)
for naam,kleur,licht in (('A','d','d'),('B','#','d')):
    R=[list(r) for r in O]
    for (x,y),c in WEG.items(): R[y][x]=c
    R[TAPS[1]][TAPS[0]]='a'
    for i,(x,y) in enumerate(LIJN):
        assert R[y][x] not in '.', (x,y); R[y][x]=licht if i<2 else kleur
    open(f'sprite/maker/raster_r10{naam}.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
    ch=[(x,y) for y in range(64) for x in range(64) if R[y][x]!=O[y][x]]
    print(naam,'gewijzigd',len(ch),'buiten kop',[p for p in ch if not (p[0]<=21 and 40<=p[1]<=55)])
