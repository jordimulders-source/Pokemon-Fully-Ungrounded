# Kolibrie ronde 3 (24 okt)

Bestanden:
- `kolibrie.png`: hoofdversie op `silhouet_v6_groot_1x.png`, ±1 px. 64×64, 16 kleuren, index 0 transparant, 1016 px.
- `kolibrie_variant_lint.png`: variant met slierten buiten het silhouet; kop, lijf, vleugels en franje gelijk aan de hoofdversie. 1007 px.
- `kolibrie_variant_sleep.png`: tweede variant met de slierten naar achteren (zie Aanvulling).
- `vel.png`:
  - ronde 3, variant lint en variant sleep op 3× naast Venomoth, Yanma, Swellow, Articuno, Fearow en Honchkrow;
  - die rij op licht en op donker;
  - daaronder alles op 1× op licht en donker, ook compact naast elkaar.
- `teken.py`: met de hand getypt tekst-raster; de variant is een overlay (`LINT`).
- `check.py`: pixeldiff en de >1 px-controle.
- `vel.py`: maakt het vel.

## Toets op 1× (eerst, eerlijk)
- **Hoofdversie:** een mug is het niet meer. De segmentatie (zwart / blauwgroen / neonpaars) is weg. Kop, snavel, kuif en V-vleugels lezen als kolibrie. De slierten blijven het zwakke punt.
  - Op licht vervagen ze tot bleke geestlinten; dat leest als staart.
  - Op donker lichten de drie vlammetjes op onder het lijf en lezen de slierten nog half als drie hangende poten met lichtpuntjes.
  - Oorzaak: in het bevroren silhouet hangen drie evenwijdige slierten bijna verticaal onder het lijf. Kleur kan dat binnen ±1 px niet helemaal opheffen; dat voorspelde de keuring ook.
- **Variant lint:** leest op 1× op licht en donker als kolibrie met een staart die naar achteren sleept:
  - een brede krul met een vlammetje omhoog;
  - twee linten die naar rechtsonder wapperen, met vlammetjes die naar achteren wijzen.
  - Geen poten meer. Dit is mijn advies aan Jordi; het is wel een silhouetwijziging, dus zijn keuze.

## Aanvulling: variant sleep (`kolibrie_variant_sleep.png`)
Claude keurde de variant lint af: die hing nog te recht onder het lijf, waardoor er verticale strepen bleven die als poten lazen. Daarom deze tweede variant.
- **Gelijk aan de hoofdversie:** kop, kuif, lijf, vleugels en franje. Pixeldiff buiten de staartzone (x < 42, en vanaf rij 41 x < 36) is **0**, gecontroleerd met een script. Alleen de franje is onderaan gesloten (rij 40, x 42–49 `K`), omdat de oude slierten daar uitkwamen.
- **Staart:** de drie slierten slepen naar rechts, in het verlengde van de rug- en buiklijn, zoals de staartveren van de langstaartsylfe en de linten van Articuno. Ze waaieren uit, en pas aan het eind krullen ze of wijken ze uit:
  - S1 (boven, het verst weg, als eerste getekend): lint over de staartbasis naar rechts, dat aan het eind omhoog krult. Het vlammetje staat met de punt omhoog boven de krul (rij 26–31).
  - S2 (midden): golft naar rechts met één dip (rij 39–42). Het vlammetje ligt met de punt naar achteren tegen de rand (rij 38–42).
  - S3 (onder, het dichtstbij, als laatste getekend): loopt schuin naar rechtsonder (helling 2 px per rij). Het vlammetje wijst met de punt naar achteren (rij 49–53).
  - De ruimte direct onder de buik (x < 44, onder rij 40) is leeg.
- **Kleur:** zoals in de hoofdversie. Lichtkant `v`, kern `V`/`L`, schaduwkant `w`; naar het eind vervagend via `g`/`m` naar `p`, met vlammetjes met een `m`-rand en een `W`-kern. Geen open randen, op de kuif na (pseudo-omlijning, toegestaan).
- 997 px; 133 erbij en 122 eraf t.o.v. het silhouet, alles in de staart. Dit is een silhouetwijziging voor Jordi.

## Eerlijk 1×-oordeel per versie (vel: licht en donker, naast de referenties)
- **Ronde 3 (hoofdversie, bevroren silhouet):**
  - Kop, snavel, kuif en vleugels lezen als kolibrie; de segmentatie (mug) is weg.
  - De slierten hangen bijna verticaal onder het lijf. Op licht vervagen ze tot geestlinten; op donker lezen ze nog als drie poten met lichtpuntjes.
  - **Niet goed genoeg**, en binnen ±1 px niet op te lossen.
- **Variant lint:**
  - Breder en met een krul, maar de twee onderste linten lopen nog steil omlaag onder de staartbasis. Op 1× zie je nog verticale strepen onder het lijf, die als poten lezen.
  - **Niet goed genoeg** (eens met Claudes keuring).
- **Variant sleep:**
  - Op 1× leest hij op licht en donker als kolibrie met een lange staart die naar achteren sleept, zoals bij Swellow en de langstaartsylfe. Er staat niets verticaal onder het lijf, dus geen poten; de mug-lezing is weg.
  - Op donker vormen de drie vlammetjes aan de rechterkant een lichte waaier van punten. Dat leest als staartpunten en niet als vork, omdat S1 omhoog krult en S3 lager en meer naar links eindigt.
  - **Mijn advies.**
  - Kanttekening voor Jordi: de staart loopt tot de rand van de box (x 63), en de slierten zijn korter dan bij een echte langstaartsylfe (±2× het lijf); langer past niet in 64 px.

## Per keuringspunt
1. **Slierten als glanzende linten:**
   - Lichtkant `v`, kern `V`/`L`, schaduwkant `w`; zwart (`K`) alleen onder de bocht van sliert 2.
   - Rechte stukken binnen ±1 px omgezet in bogen:
     - sliert 1 buigt uit tot x 63 (rij 42–43);
     - sliert 3 bolt uit naar x 46–48 en loopt terug, met looprijen van ≤ 3;
     - sliert 2 buigt bij rij 45–47.
   - Naar het eind dunner (3 → 2 px) en **vervagend naar bleek** (violet → `g`/`m` → `p`), zodat het eind een geestlint is en geen poot met voet.
2. **Sliert 2 los:**
   - één kolom lucht (x 55, rij 48–51) tussen sliert 2 en vlammetje A;
   - vlammetje B hangt via een steeltje van 1–2 px aan het eind van sliert 2;
   - sliert 3 heeft 1–2 kolommen lucht tot B.
3. **Vlammetjes:**
   - Eén vlamvorm, drie maten, niet gekopieerd: smalle punt omhoog (vrij, met lucht naast de sliert) en een brede ronde voet.
   - Kern `W` laag in de voet; rand `m` rondom, dus geen donkerste tint onderaan.
   - De sliert hecht aan de zijkant van de voet.
   - In de variant wijzen B en C naar achteren (rechts), A omhoog in de krul.
4. **Vleugels Venomoth/Yanma:**
   - Fluweel alleen op de wortel (rugdeel, ±⅓).
   - Daarna lila `m`, dan bleek `p`/`P`, met een gesloten buitenrand `g`.
   - Twee doorlopende pennen evenwijdig aan de voorrand tot aan de rand: de bovenste loopt tot de punt, de onderste eindigt op de achterrand. Kleur `k` op de wortel, `g` in het midden, `m` in het bleke deel.
   - Geen gaas meer. De verre vleugel is hetzelfde, iets donkerder.
5. **Segmentatie weg:**
   - Violet gedempt: basis (134,84,198), verzadiging 0,58; schaduw (100,58,146); hooglicht (178,138,230).
   - Blauwgroen is een smalle glans (3 rijen) bovenop de schouder naar de vleugelwortel, zonder eigen rand; hij gaat daar over in fluweel.
   - De kop loopt via `k` → `w` in nek en keel over in het violet (kraag).
6. **Koel randlicht:**
   - `H` (118,116,176) als lichte omlijning op kruin, voorhoofd, achterhoofd en snavelrug, en op de voorrand van beide vleugelwortels, zoals Murkrow/Honchkrow.
   - Op het donkere vel blijven kop en snavel nu leesbaar.
7. **Buik en franje:**
   - De buik is een boog: rij 38 x 19–21, rij 39 x 22–25, rij 40 x 26–32, rij 39 x 33–37, rij 38 x 38–41.
   - De franje heeft twee veerpunten met donkere inkepingen bij (48,36) en (49,38).
8. **Kuif:**
   - Drie losse veren: een donkere inkeping (13,16–17) tussen veer 1 en 2, en lucht tussen veer 2 en 3.
   - Bleke punten van 2–3 px in de veerrichting.
   - Veren in violet (lichtkant `V`, schaduwkant `v`), dus pseudo-omlijning voor delen van 1–2 px (§8).
9. **Open randen:**
   - Alle punten uit de keuring zijn gesloten.
   - Een eigen controle (basis/hooglicht naast transparant) geeft alleen nog de kuifveertjes; dat is pseudo-omlijning en toegestaan.
10. **Polijsten:**
    - Hooglicht als één band langs nek en bovenflank, en als een tweede band achter de vleugel op de rug (rij 34). Geen losse vlekjes meer.
    - Oog: glans linksboven (10,26), reflectie rechtsonder (11,27), bovenlid (10–11,25).

## Pixeldiff (hoofdversie t.o.v. silhouet_v6_groot_1x.png)
- 1016 px (silhouet 986): **64 erbij, 34 eraf**.
- **Op één pixel na alles binnen 1 px van de omtrek:** (30,40) ligt 2 px onder het oorspronkelijke buikgat. Dat is de uitbolling van de buik die de keuring zelf voorstelde (rij 40, x 25–33).
- Erbij:
  - binnenranden en bogen van de slierten;
  - buikboog (26–32,40) en het buikgat (29–31,39);
  - voorhoofd (4,26–27);
  - kuif (14,12–13);
  - vlammetjes binnen de ±1 px-ruimte.
- Eraf:
  - lucht tussen sliert 2 en vlammetje A en B;
  - verhoogde buiklijn bij de staartbasis (38–41,39);
  - kuif (12,12–13);
  - losse randpixels van het oude racket B.
- Volledige lijst: `python3 check.py -v`.
- Variant: 124 erbij en 103 eraf, alleen in de staart (bewust buiten het silhouet).

## Dragonfly Cave-regels (SPRITING §1–§8)
- **§1:** met de hand, tekst-raster.
- **§2:** per onderdeel en op 8× bekeken: kop, vleugels, lijf, franje, slierten, vlammetjes, kuif, variant.
- **§3:**
  - curven met oplopende/aflopende looplengtes in slierten en buik;
  - geen knik in een boog;
  - de enige rechte delen zijn de vleugelranden (echte rechte veren) en de bovenkant van het lint van sliert 1 (6 px, de top van de boog).
- **§4:**
  - Groepen: fluweel (K/k/h + randlicht H), violet (v/w/V/L), glans (T/U), vleugel/geest (g/m/p/P/W).
  - Violet gedempt naar Crobat/Ghost-niveau. 16 kleuren.
- **§5:**
  - Licht linksboven: randlicht en hooglicht links/boven; schaduw aan keel, buik en achterrand van de vleugelwortel; slagschaduw `w` onder de vleugel.
  - Slierten: lichtkant links/boven.
- **§6:** één glanspixel en een reflectie in het oog; één kernpixel per vlammetje.
- **§7:** geen schubben.
- **§8:**
  - Zwart alleen aan de schaduwkant: buik, onderzijde staartbasis, achterrand vleugelwortel, onder de bocht van sliert 2.
  - Selout aan de lichtkant: `H` op de kop, `v` op lijf en slierten, `g` op de vleugels.
  - 1 px, geen buiten-AA.
- **Making Fake Pokémon:** drie hoofdkleuren plus geestlicht, geen gaas of stipjes meer, Ghost via vervagende linten en vlammetjes.

## Wat nog niet klopt (eerlijk)
- **Hoofdversie, slierten op donker:** ze lezen nog half als drie hangende poten met lichtpuntjes. Binnen het bevroren silhouet heb ik geen betere oplossing gevonden dan vervagen naar bleek. Daarom ligt de variant ernaast. Dit is een silhouetvraag voor Jordi, geen pixelfout die ik nog binnen ±1 px kan repareren.
- **Formaat** (1016 px) blijft klein voor een eindvorm (keuring D1). Ook dat is Jordi's keuze.

## Lessen
- Drie evenwijdige slierten die verticaal onder een lijf hangen, lezen op 1× als poten, welke kleur je ze ook geeft. Laat ze naar achteren slepen (diagonaal of een krul), dan leest het als staart.
- Een lint dat naar het eind vervaagt naar bleek leest als geest/staart; een egaal lint met een bleke klodder aan het eind leest als poot met voet.
- Een vlam heeft een vrije punt en een ronde voet met de kern laag; een vorm die met de punt aan de sliert hangt, leest als druppel.
- Een kruis- of ruitvorm leest als glinstering (sparkle), niet als vlam: maak de vlam asymmetrisch (ronde voet, punt van 2 px).
- Doorschijnende vleugel = bleke vulling + doorlopende pennen tot de rand + gesloten rand. Een verloop van donker naar licht leest als kleurverloop.
- Een kleurvlak met een eigen donkere rand tussen kop en lijf leest als los segment (insect). Een glans hoort zonder rand op de vorm te liggen.
- Koel randlicht (`H`) op een fluweelzwarte kop houdt hem leesbaar op donker, zoals bij Murkrow/Honchkrow.
- Staartslierten van een zwevende vogel horen in het verlengde van de lijflijn naar achteren te slepen. Alles wat onder het lijf naar beneden wijst, leest als poot. Toets: is de ruimte direct onder de buik leeg?
- Een variant die "breder" is maar dezelfde richting houdt, lost een leesfout niet op; de richting is het probleem.
