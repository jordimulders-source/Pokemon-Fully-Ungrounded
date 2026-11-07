# Potoo-poppetje ronde 1: notities (maker)

Script: `pop3d_potoo.py` (vanuit de repo-root: `python3 docs/concept/sprites/potoo/poppetje/pop3d_potoo.py`), vel: `vel_ronde1.png`.
Geen Blender, geen mesh: dezelfde soort renderer als de lama (z-buffer, vlakke kleur, één schaduwtoon, lijn bij dieptesprong),
uitgebreid met **volumes met snijvlakken en holtes** (ellipsoïde ∩ halfruimtes − holtes). Daardoor is de open bek één holle
onderkaak die om het scharnier openklapt, in plaats van losse stokjes/schijfjes. Mondkleur zit alleen op de binnenwand.

## Gemeten (oogstraal r = 1)
| maat | leidraad (duo links) | close-up | zijfoto (duo rechts) | poppetje |
|---|---|---|---|---|
| kopbreedte | ±11,7 | 9,1 | – | 10,3 |
| oogmidden → kruin | 3,9 | 5,0 | 2,8 | 3,5 (oog groter: 1,25) |
| oogmidden → bovenrand bek | ±1,5 | 1,3 | 2,4 (mondhoek) | ±2,6 (Jordi: ogen hoger) |
| bovenrand mondhoek → haakje | – | 5,9 (3/4) | 6,2 | ±7 (mondhoek recht onder het oog) |
| bekopening hoogte / breedte | ±1,0 | 0,8 | – | ±1,1 (overdreven grote bek) |
| lijf / kop breed | – | – | nachtfoto 1,6 | 1,15 (Pokémon: lijf kleiner) |

## Waar elke vorm vandaan komt
- **Kop**: brede koepel + iets plattere kruin (close-up, leidraad) + 'gezicht' dat breed en plat naar het haakje loopt (zijfoto: voorhoofd daalt in één bocht naar het haakje).
- **Mondhoek**: recht onder het oog en ver opzij (zijfoto, close-up); de kop is daar het breedst.
- **Bovenrand**: snijvlak door mondhoeken en haakje; van boven gezien een spitse boog (twee grote 'lens'-bollen), daardoor van 3/4 een rechte rand naar het haakje. Hoornrand wordt breder naar de punt (bovensnavel leest als hard deel, zoals in de open-snavelsprites).
- **Onderkaak**: de kop onder de gaplijn als holle schaal, 62° opengeklapt om het scharnier (plus 9° kop voorover); van voren een schild/U met spitse donkere punt, lichte kaakrand (close-up). Langer dan echt: overdreven grote bek.
- **Muil**: geestblauw/paars alleen binnen de rand; donkere V-keel in de bodem (close-up), achterwand achter het scharnier.
- **Haakje**: klein, donker, krult omlaag (close-up).
- **Veertjes tussen de ogen**: rijen kleine spitse veertjes van tussen de ogen naar het haakje, punt iets los (close-up); in een iets donkerder lila, zonder eigen lijntjes (geen ruis).
- **Lijf**: peervormig, breed direct onder de kop, geen hals; schouders/vleugels hoog naast de kop (leidraad); lange platte staart (nachtfoto, illustratie).
- **Kleur**: C2 (bijna wit met lila zweem, pikzwarte ogen zonder glans); een paar schorsachtige vegen op vleugel en flank.

## Bewust gestileerd
Oog 1,25× en hoger op de koepel; bek langer en verder open; lijf 0,85×; kop licht voorover.

## Open / zwak
- Het verre oog steekt in de spritehoek als zwarte bult buiten de kopomtrek (klopt met de close-up, niet met de leidraad).
- Van voren leest de kop wat als schedel (wit + zwarte ronde ogen + V-veertjes); in de spritehoek minder.
- Veertjes tussen de ogen zijn subtiel; op 64 px vallen ze weg.
- Muil is één vlak paars met keel; diepte komt alleen uit de rand.

# Ronde 2 (vel_ronde2.png)
Reparaties op de punten van de coördinator:
1. **Geen helm/klep meer**: de kop is één koepel (`Ed`), het breedst vlak boven de gaplijn; de bovenkop wordt door dezelfde (nu verticale) lens gesneden als de kaak, dus het gezicht boven de rand is nergens breder dan de muil. De onderomtrek van de kop loopt in de mondhoeken over.
2. **Muil zo breed als de kop**: mondhoeken op de kopomtrek (`zc` = kopbreedte op de gaplijn); kaak op het scharnier even breed.
3. **Rand dun**: bovenrand één band van 0,22 + lijn; kaakrand = alleen het snijvlak van de schaal (0,35 dik). Donker alleen de kaakpunt. Kaakschaal ondieper (wig van opzij, zijfoto).
4. **Oog vlak boven de rand**: ruimte ½ oogstraal, x halverwege de koplengte (zijfoto); oog 1,15 r_e.
5. **Kopvorm**: ronde koepel, hoogste punt boven/achter het oog, voorhoofd in één bolle bocht naar het haakje (geen plat 'gezicht' meer).
6. **Kop : muil**: open muil ±60% van de hoogte kop+muil op de leidraadhoek.
Verder: keelholte achter het scharnier (`gul`) zodat er geen wit vlak in de muil zichtbaar is en geen paars buiten de rand; borst naar achteren (stak door de muil heen); schorsveeg op de borst smaller.

**Controle** (rij 2 van het vel): omtrek kop+muil (rood) en mondrand (oranje) met de hand overgetrokken op de foto's (`TRACES` in het script), uitgelijnd op het oog en geschaald op de oogstraal (foto-oog = 1 r_e), over de render op dezelfde hoek.
- Close-up (140°, 4° van boven): bovenrand, nabije kaakrand en kaakpunt vallen op de oranje lijn (afwijking < ½ oogstraal); de kruin van de foto ligt ±1 oogstraal hoger en verder naar achteren.
- Leidraad (140°, 4° van onder, kop 5° omhoog zoals op de foto): kruin en voorkant kloppen; de foto-muil hangt ±1 oogstraal verder omlaag en naar links (de foto is van onderaf, de kaak staat verder open). Bij meer openen past de close-up niet meer; nu een middenweg (66°).
- Hoek gevonden door de overlap van mondvorm en oranje lijn te meten over een reeks hoeken/kaakmaten.

# Ronde 3 (vel_ronde3.png)
Op de 10 punten van de keurder:
1. Bovensnavel = onderrand van het gezicht: dunne lichte rand, vóór rond het haakje hoornkleur (donkerder). Haakje: gebogen buis van ±1,5 r_e, donkerste accent, voorste punt van het profiel, hangt vóór de muil.
2. Onderkaak: diepe schep (dieper en langer, 66° open: punt ±6,5 r_e onder de gaplijn), eigen bevederde buitenkant met omtrek (`jawfur`, lijn op de grens), donkere punt; van opzij een wig vóór de borst.
3. Muil als holte: licht bij de rand (`mouth`), donkerder naar bodem/keel (`mouth2`), achterin een donkere keelholte (`throat`). Wat binnen de mondrand ligt en geen mondwand is, wordt in beeldruimte keelholte (floodfill): nooit vacht ín en nooit mondkleur buiten de muil.
4. Koepel lager (boven de gaplijn ±4,9 r_e), ruige kruin met veerplukjes (`tufts`); in de spritehoek is de muil minstens zo hoog als de koepel.
5. Ogen met smal licht ooglidrandje, geen glans, binnen de kopomtrek van voren, ¾ oogstraal boven de rand. **Afwijking:** 2,2 oogdiameters uit elkaar in plaats van ±1: met de ogen dichter bij elkaar (gemeten: z = 2,6/3,4/4,0) passen de overgetrokken close-up en leidraad duidelijk slechter (mondvorm-overlap 0,57→0,65); 3,7 is de middenweg.
6. Veertjes tussen de ogen: 6 donkerdere plukjes boven het haakje die de omtrek breken.
7. Schouders/vleugels lager: bovenkant ±op de gaplijn.
8. Vier getrapte slagpennen langs de staart; staart lang, smal, versmallend in het verlengde van het lijf.
9. Schors als korte gerichte vegen op vleugel, flank en kruin; haakje en kaakpunt de donkerste accenten.
10. Omtrek licht onregelmatig door veerplukjes langs kruin, wangen en borst (zoals de lama-wol).

# Ronde 4 (vel_ronde4.png)
Basis = ronde 3 (bewaard: `pop3d_potoo_ronde3.py`, `vel_ronde3.png` ongewijzigd). Alleen Jordi's vijf punten:
1. Geen bol hoofd: koepel breder en vlakker (5,6 × 3,25 × 5,5) + een tweede, lager 'gezicht' (`Ef`) dat zonder knik doorloopt naar de snavel.
2. Kaak verder naar voren: minder ver open (66° → 50°) en langer (punt −5,8 → −6,6), zodat de punt vóór het gezicht steekt in plaats van recht omlaag.
3. Ogen hoger: ruimte tot de mondrand 0,7 → 1,0 r_e; ogen iets meer uitbollend; ooglid volgt.
4. Bovensnavel: de lijn tussen gezicht en rand is weg (rand/hoorn niet meer omlijnd, dus geen naad); snavelvoorkant stomper (boog 62° → 70°, iets verder naar voren); haakje kleiner en stomp omlaag gekruld; veertjes erboven liggen platter.
5. Minder pacman: de donkere keelspleet in de kaakbodem (las als hoektand) is weg; keelholte lichter (geen donker gat), alleen een klein V-spleetje achterin; kaakpunt kleiner donker.

# Ronde 4b (vel_ronde4b.png)
Alleen punt 5 (pacman); ronde 4 bewaard als `pop3d_potoo_ronde4.py` (+ `vel_ronde4.png`).
- Bovensnavel = eigen hoornvlak (`beak` #B8AFB8, snijrand `beak2` #9A919E) op de onderrand van het gezicht: ±1 r_e hoog bij de mondhoek, hoger naar het haakje; geen omlijning, dus geen naad met het voorhoofd. In de spritehoek ligt hij als grijze band tussen oog en muil.
- Onderkaak: buitenkant iets donkerder (`jawfur` #D9D3E3) met omtrek en dunne lichte rand.
- Binnenkant met diepte: licht roze-paars bij de rand en naar de punt (`mouth`), middentoon (`mouth1`), donkerder achterin naar de keel (`mouth2`).

# Ronde 4c (vel_ronde4c.png)
Basis = ronde 4 (niet 4b; 4b bewaard als `pop3d_potoo_ronde4b.py` + `vel_ronde4b.png`). Jordi: "de punt is echt onderdeel van de snavel he, niet een decoratie".
- Bovensnavel: blijft de dunne onderrand van het gezicht; pas vóóraan steekt hij uit als één taps toelopende vorm die doorloopt in het omlaag gekrulde haakje. Kleur verloopt rand → hoorngrijs → donker (`rim`, `hk1`–`hk3`, `hook`), zonder eigen lijn.
- Onderkaak: loopt zelf spits toe; rand en buitenkant worden geleidelijk donkerder naar de punt (`jt1`, `jt2`, `tip`), geen apart kapje en geen lijn op de kleurgrens.
- Haakje, kaakpunt en hoornrand staan niet meer in LINED: alleen dieptesprongen krijgen een lijn.

# Ronde 5 (vel_ronde5.png)
Basis = 4c (bewaard als `pop3d_potoo_ronde4c.py` + `vel_ronde4c.png`). Jordi (gecorrigeerd): de kop moet juist **bol** zijn.
- Koepel `Ed` (2,4; −0,7) met radii (5,5; 4,7; 5,5): vol en rond, kruin hoger en verder naar achteren, vult de rode omtrek van de close-up en de leidraad. Gezicht `Ef` (−0,4; −1,3) met radii (4,6; 3,3; 4,8): het voorhoofd bolt in één ronde lijn naar de snavel. De afplatting van ronde 4 is teruggedraaid.
- Mondbreedte `zc` volgt de nieuwe koepel; snavelpunten, kaak naar voren, ogen hoger en haakje zijn ongewijzigd uit 4c.
- Veertjes tussen de ogen liggen platter tegen de bollere kop en iets hoger, zodat het haakje in de spritehoek zichtbaar blijft.
- Gecontroleerd: het oog staat ruim boven de mondrand (niet in de mond); de snavel sluit aan, zonder naad.

# Ronde 6 (vel_ronde6.png, pop2d_potoo.py)
Nieuwe aanpak (Jordi: "waarom ben je al uren bezig met een fucking snavel nabouwen"): het hele poppetje als 2D-vectortekening, met de hand overgetrokken, gladde Catmull-Rom-curven, getekend op 4× en met antialiasing verkleind. Geen fotopixels, geen segmentatie. De 3D-rondes blijven bewaard (`pop3d_potoo_ronde*.py`).
- Lijf, vleugel, staart, kop en bovensnavel: overgetrokken van `jordi_great_potoo_illustratie_LICHAAMSVORM.png` (punten in illustratiepixels, op 2–4× met raster gemeten), gespiegeld naar links. Kop op dezelfde plek op de schouders, geen nek, niet naar voren geschoven.
- Bovensnavel: één vorm (basis tussen de veren, rug naar voren, krult omlaag in de haak, snijrand terug), één kleurverloop van lichtgrijs naar donker; geen lijn aan de basis.
- Onderkaak: klapt om de mondhoek (onder/achter het oog) open en hangt vóór de borst; de vorm (U naar een spitse punt, kom met twee spleetjes, donker achterin onder de bovensnavel) is naar de leidraad, waarvan de muil opnieuw op 3× is overgetrokken (`L_GAPE`, `L_NEAR`, `L_FAR`). Diepte van de muil ≈ 0,94 × de kophoogte boven de gaplijn, zoals op de leidraad.
- Oog: puur zwart, alleen de donkere lijn, geen lichte rand (Jordi).
- Kleur C2, één schaduwtoon (sikkel rechtsonder), korte schorsstreepjes, borstelveertjes voor het oog.
Open: de kop staat in de 3/4-zijhoek van de illustratie, niet in de 3/4-voorhoek van de leidraad; daardoor is de muil smaller dan op de leidraad (daar even breed als de kop). Een 2D-kop over de leidraadfoto (paneel b) is daarom niet gemaakt; paneel b toont alleen de nieuwe overtrek.

# Ronde 7 (vel_ronde7.png, pop2d_potoo_r7.py)
- Kop + muil + snavel = overtrek van de leidraad (`L_HEAD`, `L_GAPE`, `L_NEAR`, `L_FAR`, `L_JAWOUT`, oog), gespiegeld; paneel (b) legt de 2D-kop met dezelfde lijnen over de foto.
- Bovensnavel `L_BILL`: één vorm (basis tussen de veren boven de gaplijn, rug, haak als einde), 1,15× (Pokémon-stap), kleurverloop lichtgrijs → donker.
- Kop op het lijf: kopschaal 0,60, achterhoofd/kruin op die van de illustratie, geen nek; kop+kaak ±37% van de hoogte. Lijf 1,25× breder dan de illustratie, staart lang.
- Oog puur zwart (1,08× van de foto), alleen de donkere lijn.
Open: het lijf leest nog als een lange taps toelopende zak (de illustratie is slank, de vleugel ligt als één groot vlak), de muilkleur is in ringen getrapt, de borstelveertjes lezen als snorharen, en op 64 px valt de haak weg.

# Ronde 8 (vel_ronde8.png, pop2d_potoo_r8.py)
Kop + snavel + muil = ronde 7 (dezelfde puntlijsten en lijnen, uit `pop2d_potoo_r7.py` geïmporteerd). Alles nu in leidraadpixels, gespiegeld.
- Nieuw lijf: rug komt achter het achterhoofd vandaan (geen nek, binnenlijn van het achterhoofd over de schouder), brede schouder, daarna bijna recht en taps naar een lange brede staart (illustratie). Breedte en de 3/4-draai naar het lijf op de leidraad zelf (rug valt op de rugrand van de foto, borst onder de kaak); kop+kaak ±40% van de hoogte (was ±37% in een stokfiguur).
- Onderkaak hangt vóór de borst (blinde test r7: "bek midden op de borst"): borst is een smalle reep onder de kaak; verre vleugel als smalle reep langs de verre borstrand (verre schouder net zichtbaar).
- Vleugel: dekveren met de boeg vóór onder de kaak en drie rijen schubveertjes; vijf pennen, langste (handpennen) voor, getrapte punten ver langs de staart; binnenlijnen in donker lila (`jt`), alleen de voorrand over de borst in de lijnkleur. Schorsstreepjes op borst, dekveren en pennen (blinde test: "glad spookje").
- Muil: één vloeiend verloop (keel achterin donker → rand licht), geen ringen; tongrichel zachter. Borstelveertjes = kleine schubveertjes dakpansgewijs tussen oog en snavel (lazen als snorharen).
Valkuil: pennen elk met een volle omtrek lezen als vingers/planken; alleen de lijn waar een pen over de vorige valt, anders wordt de vleugel weer één groot vlak.
Open: verenpatroon blijft bewust licht (C2); bij 64 px is de lijn nog grijs door het verkleinen (pas in de spritefase).

# Ronde 9 (vel_ronde9.png, pop2d_potoo_r9.py)
Basis ronde 8; blinde test r8: "parkiet 45%, potoo 25%". Kopvorm, oog, muilomtrek en haak blijven die van ronde 7.
- Snavel: snijrand (tomium) als hard grijs deel van de mondhoek langs de hele bovenrand van de muil naar voren, één vorm en één kleurverloop met de bovensnavel; de haak is de voorhoek van de open bek, het paars eronder is de bek.
- Kop: licht ruige omtrek (afgeronde veerpuntjes om de 25 px langs achterhoofd en kruin, punt naar achteren); rug begint hoger achter het achterhoofd, drie veertjes over de naad, geen binnenlijn meer tussen kop en schouder.
- Muil: spleten zijn zachte langgerekte taps toelopende lenzen (`slit2`, donkerder dan de keel, niet zwart, vervaagd).
- Lijf voller (rug ±12 px breder, borst ±12 px), staart breed (±100 px) en stomp, pennen korter mee.
- Schorspatroon: verspreide korte gerichte streepjes en vegen (bark/bark2, 16–28 px, minimale afstand 36 px) over kop, borst, vleugel en staart; nooit op lijnen, oog, snavel of in de muil (masker van donkere pixels + muil + snavel).
Valkuil: veerpuntjes om de 17 px met spitse driehoeken gaven een zaagblad/egelkop; afgerond en om de 25 px leest als "licht ruig". Maskerfilters op 4x-resolutie zijn traag: op 1/4 rekenen.

# Ronde 10 (vel_ronde10.png, pop2d_potoo_r10.py)
Basis ronde 9; blinde test r9: reuzenpotoo 55% (kaketoe 25%, witte uil 10%).
- Muil als brede U: beide kaakhelften (`L_NEAR`, `L_FAR`, `L_JAWOUT`) bollen naar buiten (max ±16–18 px halverwege), de punt is stomper; de voorhoek onder de haak blijft op de leidraad (vloeiende overgang, anders een knik). Nooit smaller dan de leidraad.
- Haak kort: 1,15x → ±1,06x de foto, en óver de mondlijn getekend (anders verdwijnt hij onder de lijn).
- Mantel/schouderveren lopen hoog achter en naast de kop door (rug begint bij y 150, gebocheld zoals de leidraad); kop + mantel hebben één doorlopende ruige omtrek; de losse naadveertjes van ronde 9 zijn weg (gaven witte vlekken).
- Veerpuntjes (`ruffle`) langs rug (om de 34 px) en borst/flank (om de 38 px); dons onder de kin (boogjes); achterste pennen breder zodat de vleugel een eigen getrapte rand heeft buiten de rug.
Valkuil: veerpuntjes om de 26 px over de hele omtrek maken er een pluche knuffel van; spaarzaam houden.

# Ronde 11 (vel_ronde11.png, pop2d_potoo_r11.py)
Basis ronde 10; blinde test r10: uil 40%, kaketoe 25%, potoo 20% ("paars vlak als vizier/masker/glas", "grijze rand als kromme snavelpunt").
- Grijze snijrand langs de muil weg: de gezichtsveren lopen door tot de dunne lila-roze lip. Snavel = alleen het korte hoornstukje vóóraan (`L_BILL`, één vorm met de haak, over de mondlijn).
- Muil mat: middentoon paars, één zachte indigo holte bovenmidden rond keel en spleten, lichtere kom naar de kaakpunt; geen verloop, geen tongvlek. Spleten donker, zacht, langgerekt.
- Bevederde wang van de nabije kant valt over de mondrand (muil = holte in de kop).
- Voorhoofd tot 9 px verder naar voren (rond y 205); mantel begint lager (y 188) met een zachte lila binnenlijn langs het achterhoofd, zodat de koepel heel blijft.
- Vel: extra paneel (f) kop naast de gespiegelde leidraad, zelfde uitsnede.
Valkuil: drie diepte-zones als banden langs de bovenrand gaven banding (parallel aan de rand); één vlek met zachte rand leest als holte.

# Ronde 12, diagnosevarianten (vel_ronde12_varianten.png, pop2d_potoo_r12v.py)
Blinde tests r11: "snavel te klein en los boven het paarse gat, geen boven- en onderdeel", "egale witte zuil", "oog hoog en ver naar achteren". Vier varianten, één ding per stap, zonder tekst in `scratchpad/bt/v1–v4.png`:
- v1: onderkaak als eigen deel (lichte kaakrand `jawrim` met dunne lila binnenlijn langs de hele onderrand van de muil, niet langs de bovenrand); bovensnavel = hoornstuk vast aan de bovenrand (kort taps stukje langs de rand) dat in de haak eindigt; oog 24 px naar voren, afstand oog–rand 0,55 oogstraal (daardoor ±8 px hoger, niet lager: lager kan niet zonder onder 0,5 r te komen, de rand loopt naar voren omhoog).
- v2: v1 + roze muil (alleen diagnose). v3: v1 + sterker grijsbruin gemêleerd patroon (3 tonen, dichter, vaker vegen). v4: v2 + v3.
Valkuil: een brede kaakrand als dikke PIL-lijn langs een catmull-curve geeft kamtanden; als masker (muil min erosie, zonder de bovenrand) is hij strak. Grote MinFilters op 4x: op 1/4 rekenen (`ferode`).

# Ronde 13 (vel_ronde13.png, pop2d_potoo_r13.py)
Basis ronde 12 v3 (paars + sterker patroon; blinde tests potoo als 1e keus: v1 55%, v2 roze 60%, v3 schors 70%, v4 65%).
- Bek groeit uit de kop: mondhoek met plooi en schaduwwig, de lip loopt erin; bovenrand van de muil als zachte golfjes (gezichtsveren over de lip); kin/keelzak als bevederd volume onder de kaakpunt dat vloeiend (smoothstep vanaf y 380) uit de kaak groeit, met lijn alleen waar hij over het lijf valt.
- Geen harde lijn kop–schouder: bovenste deel van `L_JAWOUT` en van de dekverenrand zonder lijn, veerpuntjes van de wang over de mantel met alleen fijne puntboogjes; lila achterhoofdlijn weg.
- Patroon met verloop (`region`): mantel/vleugel/staart dicht (19 px) en donker met vegen, kruin klein en middel, gezicht en borst ijl en licht.
Valkuil: smalle puntjes langs de bovenrand van de muil met een donker lijntje lezen als tanden; brede ondiepe golfjes niet. Een kinzak met harde start geeft een knik; laat de verschuiving geleidelijk beginnen.

# Ronde 14 (vel_ronde14.png, pop2d_potoo_r14.py)
Basis ronde 13; alleen muil/kaken (blinde tests r13: "paars schild/masker vóór op kop en borst", "geen mondhoek tot onder/achter het oog", "kaken te dun", "binnenkant vlak, sticker", "onderkaak sluit niet aan op kin/keel"). Alles buiten de muil/kin is bevroren: het script tekent ronde 13 (patroon opgenomen en herhaald) en neemt buiten de opdrachtzone ronde 13 over; controle in het script: pixeldiff buiten de zone = 0.
- Mondhoek als scharnier: de lip rondt de hoek af en loopt in de dunne bovenlip; de gaplijn loopt als taps toelopende plooi (eerst lijnkleur, dan donker lila) met een schaduwwig achter de hoek door, de wang/mantel in.
- Kaken dikker: lichte lip langs de hele onderkaak, wisselend dik (23 bij de mondhoek, ±17 langs de nabije kaak, 9 bij de punt, 4–6 langs de verre kaak; leidraadpixels), met één schaduwtoon aan de onderkant en een donkere binnenrand (`lipin`) naar de holte; bovenlip blijft dun onder de gezichtsveren; hoornstuk + haak ongewijzigd; kaakpunt licht hoornkleurig, alleen op de lip.
- Holte: gehemelte (`mroof`) met slagschaduw onder de bovenkaak (indigo, dik in het midden, dun naar hoek en voorkant), donkere V-spleet, donkere keelrand achter de tongwortel, lichtere kaakbodem (`mfloor`) met tong + groef, binnenwand van de verre kaak als eigen toon (`mwall`).
- Kin: bevederde onderkant van de kop (9 → 28 leidraadpixels breed onder de punt) die vanaf de punt terugloopt naar de keel onder de mondhoek, schaduwsikkel aan de onderkant, slagschaduw op de borst, omlijning taps aan beide uiteinden. Cheek-overlap van r13 (wang over de nabije mondrand) is weg: de dikke lip neemt die rol over.
Valkuil: een gaatje van 1 px tussen twee aangrenzende maskers (kin min muil) wordt door de buitenlijn (MinFilter-erosie, vierkante kern) een zwart vierkantje; het silhouet met de onbewerkte (iets verwijde) kinvorm samenstellen. Snel kijken: `python3 .../pop2d_potoo_r14.py prev.png` (alleen kop, 14 s; de volledige render met patroon ±2 min, ronde 13 gecachet in de scratchpad).
