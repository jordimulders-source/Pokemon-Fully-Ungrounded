FIX=[
 (22,37,'a','linkeroog: modelrand van het gat (lijn 32%) valt in de cel; groen grensde anders direct aan huid'),
 (20,39,'a','linkeroog: onderrand van het gat (lijn 46%, net onder de 50%-grens)'),
 (20,41,'d','neus: 1-px c-gat midden in de neusglans (cluster < 3 px, ruis van de reductie; maakt (20,40) en (19,41) ook geen losse pixels meer)'),
 (20,43,'d','neus: 2x2 zwart blok; modellijn ligt vooral in kolom 19 (zwart 34% tegen 23%); vlakkleur gemeten (L 130 = d)'),
 (20,44,'c','idem, vlakkleur gemeten (L 91 = c)'),
 (26,42,'a','neus: gat in de C-boog rechts tussen (25,41) en (27,43); modellijn 37% in de cel'),
 (19,48,'#','mond: 1-px gat binnen de zwarte linkermondhoek (rondom zwart), cluster < 3 px'),
 (20,52,'b','mond: losse d-pixel (cluster 1 px) linksonder; buren b'),
 (17,53,'#','mond/lijfrand linksonder: zwarte lijfrand (zwart 89%, dekking 44%) onder de dekkingsgrens, anders open rand'),
 (19,60,'#','linkervoet: zwarte onderrand (zwart 100%, dekking 44%) net onder de dekkingsgrens'),
 (20,60,'#','idem'),(21,60,'#','idem'),(22,60,'#','idem'),(23,60,'#','idem (dekking 49%)'),
 (19,56,'a','linkervoet: bovenrand, modellijn (lijn 100%, dekking 18%) onder de dekkingsgrens'),
 (18,57,'a','linkervoet: rand linksboven (dekking 18%), anders open rand'),
 (18,58,'a','linkervoet: linkerpunt grensde open aan de lucht (dekking 90%, rand valt in de cel)'),
]
# Opschoning (regel, geen tekenwerk): losse tintpixels van 1 px (b/c/d of groen) binnen de zones zijn ruis van de
# reductie (Gen 3: geen tintvlakjes < 3 px). Ze krijgen de meest voorkomende tint van hun 4 buren uit dezelfde groep.
def _opschoon(a,Z):
    out=[]
    for y in range(64):
        for x in range(64):
            if not Z[y,x]: continue
            k=a[y,x]
            if k not in (3,4,5,6,7,8): continue
            grp=(3,4,5) if k<=5 else (6,7,8)
            nb=[a[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
            if k in nb: continue
            t=[v for v in nb if v in grp]
            if not t: continue
            n=max(set(t),key=lambda v:(t.count(v),-abs(v-k))); out.append((x,y,'.#abcdGHI'[n],'losse %s-pixel (1 px), meest voorkomende buurtint'%'.#abcdGHI'[k]))
    return out
