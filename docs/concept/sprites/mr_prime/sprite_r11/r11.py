# r11 (op de r10-uitvoer; vel11.py draait r7.py, r8.py, r9.py, r10.py, dan dit). Jordi bij r10: "linkerhaar is met een
# rechte lijn gedaan, niet mooi, snor is weer slechter geworden, rechte lijnen. Linker oog klopt nog steeds niet, misschien
# moeten we de monocle laten vallen en gewoon beide ogen zo omlijnen". Niets nieuw getekend: pixels uit Mr. Rime (haar),
# de kale modelreductie (snor, kaal_idx.npy = model r9 op het spritegrid) en de sprite zelf (ogen), verschoven/omgekleurd.
R10=C.copy(); LOG.clear()
RIME=np.asarray(Image.open(G%'mr_rime/front')).astype(int)
KA=np.load('kaal_idx.npy'); MOD=np.full((64,64),-1); MOD[3:64,:]=KA[:61]   # modeltonen 0=zwart 2=64 3=80 4=112 5-7 gezicht

# ---- 1. LINKERHAAR: aansluiting vleugel -> hoedrand = Mr. Rime op de hoedverschuiving (+7,-3), rijen 9-13, x20-28 (rij 13 tot x30).
# Rime-tinten omgekleurd: lijn (Rime 1/3) -> 2 aan de lichte kant (boven/links vrij), anders 1; Rime 2 (basis) -> 3 in de
# vleugel, -> 4 in de rand (zoals de rand rechts ervan); Rime 4 (schaduw) -> 2. De rechte band (rij 10-12 tot x21) verdwijnt;
# de V-inkeping van Rime tussen vleugel en rand (rij 10 x24-26, rij 11 x25) blijft open (geen ingesloten gat).
Z='1 linkerhaar (Rime-aansluiting)'
DX,DY=7,-3
def rime(y,x): return RIME[y-DY,x-DX]
for y in range(9,14):
    for x in range(20,31 if y==13 else 29):          # rij 13 tot x30: Rime's schaduw onder de rand (4444) doorgetrokken
        v=rime(y,x)
        if v==0: zet(Z,y,x,0); continue
        vrij_boven = rime(y-1,x)==0
        if v in (1,3): t=2 if (vrij_boven or rime(y,x-1)==0) else 1
        elif v==2: t=4 if (x>=26 and y<=11) else 3
        elif v==4: t=2
        else: t=C[y,x]
        zet(Z,y,x,t)

# ---- 2. SNOR. Vorm = de kale modelreductie per kolom (MOD rij 20-25; kaal_idx = model r9 op het spritegrid): bovenrand
# met de dip naast de linkerkrul (28,21), de inkeping onder de neus (33,21), de krultoppen op rij 20, de kin tussen de lobben
# (33,24), de modelgaten van de krullen (26,22) en (41,22). Alleen de tinten zijn gekozen: krul = lus (grijze streng om het
# witte gat, licht linksboven), lob = hooglicht 5 linksboven, 4 midden, 3 sikkel onder/rechts; omlijning 2 (eigen donkere
# snortint) boven/links, 1 (zwart) onder en rechts; modelzwart binnenin (vouw krul/lob, inkeping) -> 2; bovenrand van de lob
# in het midden 3 (lichte omlijning op de bolling). Kin (33,24) = modelgezicht in de schaduwtint 7 (sluit aan op 7 eronder).
Z='2 snor'
M=set((y,x) for y in range(21,26) for x in range(24,44) if MOD[y,x] in (0,2,3,4))|{(20,25),(20,26),(20,41)}
SNOR={20:(25,'22'), 21:(24,'24428233282233224422'), 22:(24,'24832554323554224831'),
      23:(24,'24335544313544423331'), 24:(24,'13334441171334444331'), 25:(25,'111111----1133333')}
for y,(x0,s_) in SNOR.items(): P(Z,y,x0,s_)
zet(Z,20,41,2); zet(Z,20,27,5)                     # krultop rechts; gezichtsrand (selout) naar de linkerkrul
P(Z,25,42,'11')
for y in range(20,26):                             # controle: snorvorm == modelvorm
    for x in range(24,44):
        if (y,x) in M: assert C[y,x] in (1,2,3,4,5),(y,x,C[y,x])
        elif y>=21: assert C[y,x] not in (1,2,3,4,5) or (y==25 and R10[y,x]==C[y,x] and x>=44),(y,x,C[y,x])

# ---- 3. OGEN: monocle weg, beide ogen dezelfde omlijning. Nabije oog = Rime-oog (x38-40, rij 15-19) met de ring van
# nu (x36-42, rij 14-20) als omlijning van het oog: het witte glasgat tussen ring en oog (x37/x41, rij 16-18) krijgt de
# oogwittint 7 van de Rime-ooghoeken, zodat ring + oog een oog vormen in plaats van een los glas. Verre oog = hetzelfde oog
# 1 kolom smaller (binnenste iriskolom x40 valt weg, zoals Rime's verre oog aan de neuskant korter is; kolommen
# x36,x37,x38,x39,x41,x42 -> x29-34), op dezelfde rijen; het oude verre oog wordt gezichtswit.
Z='3 ogen'
for y in (16,17,18): zet(Z,y,37,7); zet(Z,y,41,7)
OOGKOL=(0,1,2,3,5,6)
OOG=C[14:21,36:43].copy()                       # nabije oog met omlijning, 7 rijen x 7 kolommen
OOG[6,5]=8                                      # (41,20) is de krultop van de snor, geen oog
for y in range(15,21):
    for x in range(29,35):
        if C[y,x] in (1,3,6,7): zet(Z,y,x,8)      # oud verre oog (rij 16-20) weg (gezichtswit)
for j in range(7):
    for i,xs in enumerate(OOGKOL):
        v=OOG[j,xs]
        if v!=8: zet(Z,14+j,29+i,v)
