# ---- 1. Berg (achterwand rechts): was effen 7 -> diepe koele schaduw 14,
#         met een lichter facet 15 linksboven (diagonale grens, volgt de rotswand).
for y in range(9,49):
    xs=[x for x in range(41,64) if a[y,x]==1]
    if not xs: continue
    x=min(xs)-1
    while a[y,x]==7:
        # model: bovenste deel van de wand lichter (15), diagonale slagschaduw van de
        # terrassen (14) die naar onder breder wordt; smalle strook onderaan geheel 14.
        a[y,x]=14 if (y>=37 or x < 47+(y-12)*0.42) else 15
        x-=1
# ---- 2. Kistje (gebroken ruïneblok naast de middelste gevel), belijnd als de gevel:
#         bovenkant selout 7 (bestond al), onderkant en rechterkant donkere lijn 2.
R(38,14,46,14,[6,4],2)
R(47,11,47,14,[3,4],2)
P(3,[(37,12),(38,12)])            # lichte linkerkop
P(5,[(44,13),(45,13),(46,13),(45,12),(46,12)])  # schaduwkant voorvlak
# ---- 3. Grote rechter schaduwvlakken (was één effen 6-vlak).
# S1 = voeg over het rechtervlak van het onderste blok (bestaande 7-pixels).
S1={44:52,45:51,46:51,47:50,48:50,49:49,50:48,51:47,52:47,53:47,54:46,55:46,56:45,57:45,58:44,59:44,60:44}
def onder_S1(x,y): return x in S1 and y>S1[x]
def boven_rand(x,y):  # boven de bovenrand van het onderste blok = middelste terras (M)
    rand={40:40,41:40,42:39,43:39,44:39,45:39,46:39,47:38,48:38,49:38,50:38,51:37,52:37,53:37,54:36,55:36,56:36,57:36,58:36}
    return x in rand and y<rand[x]
for y in range(28,61):
    for x in range(40,62):
        if a[y,x]!=6: continue
        s=x+y
        if boven_rand(x,y):                 # M: middelste terras, rechterzijde
            if s<=74: a[y,x]=5
            elif s>=84: a[y,x]=15
        elif onder_S1(x,y):                # D: onderste rij stenen
            if s<=98 and x<=46: a[y,x]=5
            elif s>=106: a[y,x]=15
        else:                               # U: bovenste rij stenen van het onderste blok
            if s<=91: a[y,x]=5
            elif s>=101: a[y,x]=15
# voegen in schaduwvlakken: eigen donkerste tint i.p.v. warme 7
for y in range(36,61):
    for x in range(44,62):
        if a[y,x]==7: a[y,x]=14
# berg ook onder de kroonrand (rij 11 was nog 7)
R(48,11,53,11,7,15)
# ---- 4. Mos: meer, 3 tinten (8 licht boven/links, 9 midden, 13 schaduw en hangende plukjes)
# kroon rechtsboven
P(8,[(52,10),(53,10)]); P(9,[(54,10),(53,11)]); P(13,[(54,11),(54,12)])
# middelste terras rechts (bovenrand) + plukjes over de rand
P(8,[(50,26),(51,26),(46,27),(47,27)]); P(9,[(52,26),(48,27),(49,27),(50,27)])
P(13,[(51,27),(52,27),(48,28),(50,28),(51,28),(50,29)])
# bovenste terras links (gevelterras)
P(8,[(28,17),(29,17),(30,17),(31,17),(32,17)]); P(9,[(33,17),(34,17),(30,18),(31,18),(33,18)])
P(13,[(32,18),(31,19),(32,19)])
# terras linksboven (bovenvlak), model: mos op de linkerrand
P(8,[(15,28),(16,28),(17,28)]); P(9,[(18,28),(16,29),(17,29)]); P(13,[(17,30),(18,29)])
# dak van het gezichtsgebouw: links en rechts
P(8,[(13,33),(14,33),(15,33)]); P(9,[(16,33),(14,34),(15,34)]); P(13,[(15,35),(16,34)])
P(8,[(26,33),(27,33),(27,34)]); P(9,[(28,33),(28,34),(29,34),(26,34)]); P(13,[(28,35),(29,35),(29,36)])
# linkervleugel
P(8,[(6,39),(7,39),(6,40)]); P(9,[(8,39),(7,40),(8,40),(6,41)]); P(13,[(7,41),(6,42)])
P(8,[(3,52),(4,52)]); P(9,[(5,52),(3,53)]); P(13,[(4,53),(3,54)])
# onderste blok: bovenvlak en over de hoek
P(8,[(46,40),(47,40),(46,41),(44,42),(45,42)]); P(9,[(48,40),(47,41),(48,41)])
P(13,[(48,42),(47,43),(44,44),(45,44),(46,44),(45,45),(46,45),(45,46),(46,46),(46,47),(49,42),(49,43),(48,43),(47,44)])
P(9,[(38,45),(39,45)]); P(13,[(38,46)])
# rechterflank onderste blok (model: mos rechts)
P(9,[(55,49),(56,49),(57,49)]); P(13,[(56,50),(57,50),(57,51)])
# ---- 5. Lichte voorvlakken: tintverdeling binnen elk vlak (licht linksboven, schaduw rechtsonder,
#         slagschaduw onder overstekken).
R(13,37,24,37,4,5); R(19,38,21,38,4,5)           # slagschaduw dak op de gezichtsmuur
R(26,38,29,38,4,5); R(27,39,29,39,4,5)
R(19,46,21,46,4,5); R(20,45,22,45,3,4)           # latei: rechts verder van het licht
R(14,48,15,48,4,5)                               # slagschaduw latei op linkerstijl
R(4,50,6,50,4,5); R(5,49,6,49,4,5)               # linkervleugel, steen midden
R(8,52,9,52,4,3); R(8,53,8,53,4,3)               # steen naast de deur: licht linksboven
R(9,56,11,56,4,5); R(9,57,10,57,4,5)             #   en schaduw rechtsonder
R(10,50,11,51,4,5)
R(29,58,31,60,4,5); R(30,57,31,57,4,5)           # rechterdeel gezichtsgebouw, onderste steen
R(41,49,41,51,4,5); R(40,57,41,59,4,5)           # voorvlak onderste blok
R(34,33,36,34,4,3); R(38,39,39,41,4,5)           # middelste terras, voorvlak rechts
R(20,35,25,35,4,5)                               # dakrand gezichtsgebouw, rechts
R(22,25,25,26,4,5); R(35,25,37,26,4,5)           # gevels laag 3, onderkant rechts
R(31,32,35,32,4,5); R(33,31,35,31,4,5)           # middelste terras, voorvlak links
R(26,28,30,28,3,4); R(22,33,24,33,3,4)           # lange bovenvlakken: rechts verder weg
R(41,42,43,42,3,4); R(44,11,46,11,3,4); R(43,15,44,15,3,4)
# kroon
R(40,4,43,5,6,15); R(49,6,51,8,6,15); R(50,5,51,5,6,15)
# ---- 6. Donkere zijvlakken die als warme 7 waren gevuld (geen lijn, maar een vlak in de schaduw)
#         -> koele schaduwtint 15; buitenlijn (grenst aan transparant) blijft.
def binnen(x,y):
    return all(a[y+dy,x+dx]!=0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
def R_binnen(x0,y0,x1,y1,van,naar):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if a[y,x]==van and binnen(x,y): a[y,x]=naar
R_binnen(24,19,29,26,7,15)      # dikke dakplaat linker gevel laag 3
R_binnen(42,6,43,7,7,15)        # dakplaat linker gevel kroon
R_binnen(30,34,32,36,7,15)      # rechter kopse kant dak gezichtsgebouw
# ---- 7. Losse pixels (<3 px) van de nieuwe tinten opruimen
P(7,[(52,9)]); R(42,15,44,15,3,4)
P(6,[(40,28),(41,28),(50,37),(54,37),(58,43),(57,45),(48,58)])
P(5,[(14,49)])
P(6,[(46,38)])
# rechterzijde terras laag 3: licht hoekje linksboven, donker rechtsonder
R(44,18,46,19,6,5); R(48,22,49,25,6,15); R(47,24,47,25,6,15)
