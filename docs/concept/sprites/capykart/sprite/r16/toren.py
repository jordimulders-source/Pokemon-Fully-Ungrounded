# Toren inkleuren (vorm r15b, alleen indices binnen de blokken). Per kubus: bovenrij = smalle bevel (licht links, contactschaduw
# rechts onder het blok erboven), voorvlak links = midden, zijvlak rechts = donker, linkerrand = gekleurde selout, rechts/onder zwart.
# geel: 9 crème / 3 geel / 6 oranje-hout ; rood: E zalm / C rood / 7 donkerrood ; blauw: 9 crème / A blauw / 8 blauwgrijs ;
# dak: 9 crème (rand) / F licht groen / B donker groen.
T={}
def blok(y0,y1,xl,xf1,xs1,xr,L,M,D,bevel_tot):
    # xl = linker selout-kolom, voorvlak xl+1..xf1, zijvlak xf1+1..xs1, xr = zwarte rechterrand
    for y in range(y0,y1+1):
        T[(xl,y)]=D
        for x in range(xl+1,xf1+1): T[(x,y)]=(L if (y==y0 and x<=bevel_tot) else M)
        for x in range(xf1+1,xs1+1): T[(x,y)]=D
blok(12,17,46,52,56,57,9,3,6,49)     # geel: bevel x47-49, contactschaduw van het dak op x50-52 (midden), zijvlak 6
blok(19,24,45,51,55,56,14,12,7,48)   # rood: bevel x46-48, contactschaduw geel-blok x49-51
blok(26,31,46,52,56,57,9,10,8,49)    # blauw: bevel x47-49, contactschaduw rood-blok x50-52
# dak (rij 2-10): linkervlak F, rechtervlak B; rij net binnen de linkerrand = crème bevel langs de lichte ribbe
for y in range(3,11):
    xs=[x for x in range(44,62) if src[y,x] in (11,15)]
    for x in xs:
        T[(x,y)]=15 if src[y,x]==15 else 11
    if xs: T[(xs[0],y)]=11   # gekleurde selout links
    f=[x for x in xs if src[y,x]==15]
    if f and y>=4: T[(f[0],y)]=9   # lichte ribbe: eerste F-pixel per rij
for (x,y),v in T.items():
    assert src[y,x] not in (0,1), (x,y,src[y,x])
    G[y,x]=v
