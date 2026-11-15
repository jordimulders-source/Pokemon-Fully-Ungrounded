# Keuring welp c4 (A/B, greige + grijs), 15 nov – onafhankelijke keurder

Bekeken: 8× alle zes naast elkaar (p8, c2, c4 A/B greige en grijs), kop op 14× en 22× (x8–31, y16–33), dij op 14× naast c2, 3× en 1× naast Regirock, Claydol (`anim_front_gba.png`), Growlithe en de volwassen vorm. Eerst blind geoordeeld, daarna `c2/keuring.md` gecontroleerd.

## Metingen
- **Silhouet:** alpha-diff met p8 = **0 px** (A en B). `_grijs` = dezelfde indexen als de greige-versie (alleen palet).
- **Gezicht:** rij 26–41 (oog, pupil, neus, tanden, tong, mondlijn) in A identiek aan c2/p8. B wijzigt x24–26, y25–30 (lijn rechts van het verre oog).
- **A vs B:** 16 px, allemaal in x22–26, y22–30 (alleen de verre oogboog).
- **Palet greige:** 2 (84,74,70) · 3 (126,114,104) · 4 (162,150,136) · 5 (196,186,168) · 14 (224,216,198). Stappen ±35: goed Gen 3-contrast. Oogwit 9 nu (214,208,196): leest beter.

## Blind oordeel (hoofdvraag eerst)
**Lijf: goed.** Op 3× en 1× is dit een gehouwen stenen welp die naast Regirock en Claydol past. Licht links/voor, schaduw rechts/achter, consequent. De schoudervoluut is een echte Chavín-voluut (hoekig, open staart). De dijspiraal is veel rustiger dan in c2: geen schaakbord meer, doorlopende groeven.

**Kop: hier valt het.** Jordi vroeg om "een licht lijnen patroon in het hoofd, mogelijk cirkelend om de bovenkant van de ogen heen" en "2" lijnen "naar de bovenkant van het hoofd tussen de oren in". Wat er staat:
1. **De oogbogen zijn één doorlopende lijn over de neusbrug** (A): (12,24)–(13,24) → (14–16,25) → via (17,24) en (18,23) naar (19–21,23) → (22,24) → (23,23)–(24,22). Op 3× leest dat als een **frons/doorlopende wenkbrauw (bril-effect)**, niet als twee bogen om de ogen. Het stuk (14–16,25) ligt bovendien boven de neusbrug, niet boven een oog. De verre boog maakt een V-dip bij (22,24) en klimt dan naar het oor: een zigzag in plaats van een boog.
2. **De kruinlijnen raken de oogbogen.** Kruinlijn 1 = (16,21),(16,22),(15,23),(15,24); kruinlijn 2 = (20,20),(19,21),(19,22),(18,23),(17,24). Ze eindigen op rij 24 precies op de boog, en samen met (12–13,24) geeft rij 24 de reeks 3 3 5 3 5 3 14: een **stippellijn + verticale streepjes = rastertje**. Precies wat niet mocht.
3. **Niet "licht":** de bogen staan in index 2 (L±77) op vlak 5 (L±187), het donkerste groefdonker dat ook de buitenlijn is. Dat is zwaarder dan de kruinlijnen (index 3) en zwaarder dan de lijfgroeven op lichte vlakken.
4. **Glinsters:** de lip-pixels index 14 op (17,21),(17,22),(20,21),(16,23),(18,24) zitten 1 px naast index 3 op een vlak 5: op 8× leest het voorhoofd als gebarsten tegels met glinsters, op 1× als vlekkerig voorhoofd (c2 had een rustig, mooi gehouwen voorhoofd).
5. **B is erger:** de extra verticale groef (24,25)–(24,28) + (25,29) sluit een kader rond het verre oog: dat is letterlijk een **bril**. B valt af.

**Zou Jordi dit mooi vinden?** Het lijf waarschijnlijk wel (hij krijgt eindelijk steen). Maar de kop is het eerste waar hij naar kijkt, juist omdat hij om die lijnen vroeg, en hij keurde eerder "willekeurige lijnen op het hoofd" af. Zoals het nu is (frons + rastertje) verwacht ik dat hij het afkeurt. Met de reparaties hieronder (twee losse lichte bogen, twee korte kruinlijnen die niets raken) verwacht ik wel een ja.

## Check c2-MOET
1. Dijspiraal rustiger, hart opgeruimd: **opgelost** (geen 1-px diagonale trappen meer; groeven doorlopend; hart is een haakje (42–43,52),(44,53),(44,54) dat aan de buitenring vastzit: een echte spiraal). Restpunt zie MOET 3.
2. Losse groefstip (32,49): **opgelost** (nu 4).
- c2-MAG oogwit lichter: **gedaan**. Kraaghooglicht (31–33,32): **gedaan** (nu 4).

## Eindoordeel
**FAIL** (lijf, silhouet, gezicht en tint zijn goed; alleen de kopgravure en één punt op de dij). **Variant A** is de basis; B vervalt (bril). Buiten de genoemde pixels diff 0.

## MOET (op A; coördinaten x,y op 64×64, indexen van het palet)
1. **Twee losse oogbogen, licht, geen brug:**
   - Neusbrug vrijmaken: (15,25),(16,25) 2 → **4** (c2-waarde).
   - Nabije oogboog = (12,24),(13,24),(14,25), alle drie index **3** ((14,25) is nu 2). Dat is een korte boog over de bovenkant van het nabije oog, die rechts afzakt.
   - Verre oogboog = (18,24),(19,23),(20,23),(21,23),(22,24) in index **3** (nu: (18,24)=14, (19–21,23)=2, (22,24)=2). Geen V-dip naar het oor: (23,23) 2 → **3** (c2-waarde) en (24,22) 2 → **c2-waarde**. De boog eindigt bij (22,24).
2. **Kruinlijnen los van de bogen, 1 px ruimte:**
   - (15,24) 3 → **5** en (17,24) 3 → **5** (c2-waarde).
   - (18,23) 3 → **5** (c2-waarde), zodat kruinlijn 2 = (20,20),(19,21),(19,22) eindigt boven de verre boog en kruinlijn 1 = (16,21),(16,22),(15,23).
   - Beide lijnen in index 3 laten (licht); (20,20) mag 3 worden in plaats van 2 zodat de lijn niet als inkeping in de buitenlijn leest.
   - Hooguit **één** lip-pixel 14 per kruinlijn, aan de rechteronderkant: houd (17,22) en (20,21); (17,21) en (16,23) → **5**.
   - Toets daarna op 3×: het voorhoofd moet rustig zijn zoals in c2, met twee lichte bogen en twee korte streepjes omhoog; geen rij van afwisselende pixels meer op rij 24.
3. **Dijspiraal: geen schietschijf.** De buitenring is rondom gesloten ((40,49) is 4, maar (41,49) en (40,50) raken elkaar diagonaal) en wordt omringd door een lichte ring 5 en daarbuiten nog een donkere boog (x49, y52–56): op 3× leest het als concentrische ringen. Maak er een voluut met staart van: (48,52)–(48,56) 5 → **3** (dat is bovendien de schaduwkant van de dij; lichte lip hoort daar niet) en laat de buitenring linksboven uitlopen in de dijlijn: (40,49) 4 → **2** en (39,48) 5 → **2**, zodat de groef aansluit op (38–39,47). Hart en binnenhaak niet aanraken.

## MAG
- Grijs tegenover greige: zie hieronder; puur palet, geen pixelwerk.
- De lichte ring 5 linksboven rond de dijspiraal (x38–44, y47–48) mag 1 rij smaller als de dij na MOET 3 nog als schijf leest.
- Voorpootbanden (x24–32, y52/54) zijn nog kaarsrecht; mogen blijven (de foto heeft geribbelde poten).

## Tint
**Grijs** werkt beter: leest op 1× direct als steen naast Regirock, minder als beige huisdier (Jordi's klacht "teveel een huisdier"), en het warme oogwit en de mauve pupil springen er meer uit. Greige ligt dichter bij de foto (warme kalksteen) en het bruin van de volwassen vorm. Mijn advies: grijs, maar toon Jordi beide (keuze voor Jordi, palet verandert verder niets).
