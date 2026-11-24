# ---- zones k4 (wordt door k4.py uitgevoerd; a = raster, E=14, F=15) ----
LICHTER={14:15,15:6,6:5,5:4,4:3}
def bereik(d):  # {y:(x0,x1)} -> set
    return {(x,y) for y,(x0,x1) in d.items() for x in range(x0,x1+1)}
def lijn(pts): return set(pts)

def kleur_vlak(naam, masker, voegen, voegkleur, basis, bevel_links=True, geen_bevel=()):
    """masker min voegen -> stenen (4-samenhang); basis(cx,cy,stenen) -> tint; bevel boven (+ links bovenste helft)."""
    m={p for p in masker if a[p[1],p[0]] not in MOS and a[p[1],p[0]]!=1}
    for p in voegen:
        if p in m: a[p[1],p[0]]=voegkleur
    vrij=m-set(voegen)
    stenen=[]; gezien=set()
    for p in sorted(vrij):
        if p in gezien: continue
        st=[]; stack=[p]; gezien.add(p)
        while stack:
            q=stack.pop(); st.append(q)
            for d in ((1,0),(-1,0),(0,1),(0,-1)):
                r=(q[0]+d[0],q[1]+d[1])
                if r in vrij and r not in gezien: gezien.add(r); stack.append(r)
        stenen.append(st)
    VS=set(voegen)
    for st in stenen:
        cx=sum(p[0] for p in st)/len(st); cy=sum(p[1] for p in st)/len(st)
        t=basis(cx,cy,len(st))
        S=set(st); ymin={}
        for (x,y) in st: ymin[x]=min(ymin.get(x,99),y)
        ytop=min(p[1] for p in st); ybot=max(p[1] for p in st)
        for (x,y) in st:
            c=t
            if (x,y) in geen_bevel: pass
            elif (x,y-1) in VS: c=LICHTER[t]                          # bovenrand onder een voeg vangt licht
            elif bevel_links and (x-1,y) in set(voegen) and y<=(ytop+ybot)/2: c=LICHTER[t]  # linkerrand na verticale voeg
            a[y,x]=c
    print(naam, 'stenen:', len(stenen), [ (round(sum(p[0] for p in s)/len(s)),round(sum(p[1] for p in s)/len(s)),len(s)) for s in stenen])

# ===== Bergwand boven (x48-57, r11-26) =====
BWb=bereik({11:(48,52),12:(48,53),13:(48,54),14:(48,54),15:(49,55),16:(49,55),17:(50,55),18:(50,55),19:(50,55),
            20:(51,56),21:(51,56),22:(51,56),23:(51,56),24:(51,56),25:(51,57),26:(53,57)})
Vbw=lijn([(48,14),(49,14),(50,13),(51,13),(52,12),(53,12),
          (53,13),(53,14),(53,15),
          (50,18),(51,18),(52,17),(53,17),(54,16),(55,16),
          (52,19),(52,20),(52,21),
          (51,23),(52,22),(53,22),(54,21),(55,21),(56,20)])
def basis_bw(cx,cy,n):
    if cy<19.5: return F
    if cx<54 : return E          # binnenhoek onder het terras / naast het blok
    return F
kleur_vlak('bergwand boven',BWb,Vbw,E,basis_bw)
# ===== Bergwand onder (x54-58, r26-37) en strook x58-61 (r38-48) =====
BWo=bereik({27:(54,57),28:(54,57),29:(54,57),30:(54,58),31:(54,58),32:(54,58),33:(54,58),34:(54,58),35:(54,59),36:(54,59),
            37:(58,59),38:(58,59),39:(58,59),40:(59,60),41:(59,60),42:(59,60),43:(59,60),44:(59,60),45:(60,61),46:(60,61),47:(60,61),48:(60,61)})
Vbo=lijn([(55,27),(55,28),
          (54,30),(55,30),(56,29),(57,29),
          (57,31),(57,32),
          (54,34),(55,34),(56,33),(57,33),(58,32),
          (56,35),(56,36),(59,42),(60,42)])
kleur_vlak('bergwand onder',BWo,Vbo,E,lambda cx,cy,n:E, bevel_links=False)
# plaatselijk: in de smalle strook alleen steenkoppen
for (x,y) in [(58,40),(59,40),(59,44),(60,44)]: pass

# ===== Zijvlak bovenste blok (US, x45-49, r18-25) =====
US=bereik({18:(45,48),19:(45,48),20:(45,49),21:(45,49),22:(45,49),23:(45,49),24:(45,49),25:(45,49)})
Vus=lijn([(45,22),(46,22),(47,21),(48,21),(49,20),(48,22),(48,23),(48,24),(48,25)])
kleur_vlak('zijvlak boven',US,Vus,E,lambda cx,cy,n: 6 if cy<21 else F)

# ===== Zijvlak middelste terras (MTS) =====
MTS=bereik({29:(45,53),30:(41,53),31:(41,53),32:(41,53),33:(41,53),34:(41,53),35:(41,53),36:(41,53),37:(41,53),38:(41,51),39:(41,48),40:(41,44),41:(41,42)})
ONDER=[(46,39),(47,39),(48,39),(49,38),(50,38),(51,38),(52,37),(53,37)]   # binnenhoek met het bovenvlak van het blok eronder
Vmt=lijn([(47,29),(47,30),(47,31),(47,32),(47,33),(47,34),(51,29),(51,30),(51,31),(51,32),(51,33),
          (41,37),(42,37),(43,37),(44,36),(45,36),(46,36),(47,35),(48,35),(49,35),(50,34),(51,34),(52,34),(53,33),
          (45,37),(45,38),(50,35),(50,36),(50,37)]+ONDER)
def basis_mt(cx,cy,n):
    if cx<45.5: return 6
    return F
kleur_vlak('zijvlak midden',MTS,Vmt,E,basis_mt)
for x in range(40,41):
    for y in (33,34,35,36): a[y,x]=5          # voorvlakhoek recht houden op x40|41

# ===== Bovenvlak blok rechtsonder, achterste deel (TF) =====
TF={49:(39,41),50:(39,40),51:(39,40),52:(38,39),53:(38,39),54:(38,39),55:(37,38),56:(37,38),57:(37,38)}
for x,(y0,y1) in TF.items():
    for y in range(y0,y1+1):
        if a[y,x] in MOS: continue
        a[y,x]= 5 if x<=52 else 6

# ===== Zijvlak blok rechtsonder (LBS) =====
LB={}
top={44:45,45:47,46:48,47:45,48:44,49:44,50:41,51:41,52:40,53:40,54:40,55:39,56:39,57:39,58:40,59:45,60:49}
for x,y0 in top.items():
    for y in range(y0,62):
        if a[y,x]==1 or a[y,x]==0: break
        if x==58 and y>52: break
        LB[(x,y)]=1
LBS=set(LB)
J1=[(44,53),(45,52),(46,52),(47,51),(48,51),(49,50),(50,50),(51,49),(52,49),(53,48),(54,48),(55,47),(56,47),(57,46),(58,46),(59,45)]
Vlb=lijn(J1+[(48,44),(48,45),(48,46),(48,47),(48,48),(48,49),(48,50),
             (54,40),(54,41),(54,42),(54,43),(54,44),(54,45),(54,46),(54,47),
                          (51,50),(51,51),(51,52),(51,53),(51,54),(51,55),(51,56)])
def basis_lb(cx,cy,n):
    if cx<48: return 6
    return F
kleur_vlak('zijvlak onder',LBS,Vlb,E,basis_lb)

# ===== Streep naast de deur rechts: het model heeft daar een voeg (y~53.5, x25-31) met een verticale voeg eronder (x~29.5)
# en erboven (x~27). Voeg over de volle breedte (van deurstijl tot zijstrook) + de twee verticale voegen, zoals het model.
rij(53,26,'777777')
for y in range(54,60): a[y,29]=7
for y in range(49,53): a[y,27]=7

# bovenrand middelste terras (licht bovenvlak tussen het mos)
for (x,y) in [(47,28),(49,28),(52,28),(53,28),(53,27)]: a[y,x]=4

# ===== Dakplaten van de gevels: licht bij de nok, naar de voet toe donkerder (verloop langs de plaat) =====
# G1 (middelste rij links)
rij(19,22,'66666'); rij(20,22,'66666'); rij(21,23,'6666F'); rij(22,23,'66FFF')
rij(23,24,'6FFFF'); rij(24,24,'6FFFF'); rij(25,25,'6FFFF'); rij(26,26,'FFEE')
# G2 (middelste rij rechts)
rij(20,35,'6666'); rij(21,35,'6666'); rij(22,36,'666F'); rij(23,36,'66FF')
rij(24,37,'6FFF'); rij(25,37,'6FFF'); rij(26,38,'FFEE')
# G3 (bovenste rij links)
rij(9,33,'66'); rij(10,32,'666'); rij(11,33,'666'); rij(12,33,'66F'); rij(13,34,'6FF'); rij(14,34,'FFE')
# bovenste blok: linker gevelplaat licht boven -> donker onder (was omgekeerd), rechter zijvlak naar onderen donkerder
rij(6,42,'66'); rij(7,42,'66'); rij(8,41,'6F'); rij(9,41,'FF')
rij(8,47,'6F'); rij(8,49,'FFE'); rij(9,49,'FEE')
