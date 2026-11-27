# Icoonregels per bouw (27 nov)

Vraag: hoe maakt Game Freak van een Gen 3-front een party-icoon, per bouw? Aanleiding: de proeficonen Gumfish (vis) en Sunperor (rechtop, grote kroon) gingen mis, eerst "gewoon verkleind" en daarna hertekend tot iets anders.

## Bron en meting
- **Bron:** 55 Gen 3-paren: `anim_front_gba.png` (frame 1, `normal_gba.pal`) tegen `icon_gba.png` (frame 1, GBA-icoonpalet uit `iconPalIndex = P_GBA_STYLE_SPECIES_ICONS ? x : y`). Ter vergelijking ook `icon.png`, het moderne icoon dat nu in de game zit.
- **Bouwgroepen:** vis 8, vogel 9, tweevoeter 9, bol/zwever 8, object 8, plant 8, viervoeter 5 (controle). De lijst staat in `meet/soorten.py`.
- **Automatisch** (`meet/auto.py`, `meet/sol.py`):
  - hoogte, breedte en schaal S (= icoonhoogte / fronthoogte);
  - pose-overlap (IoU met de front, verkleind tot icoonhoogte, beste verschuiving van ±3 px; ook gespiegeld);
  - oppervlak t.o.v. gewone verkleining;
  - kleuren en omlijning;
  - solidity (oppervlak / convex omhulsel).
- **Met de hand** (`meet/hand.py`), afgelezen op roosters (front 9×, icoon 16×):
  - kaders van kop/kopgroep en grote onderdelen;
  - "rel" = (icoonmaat / frontmaat) / S. Dus ×1,00 = gewone verkleining.
  - Nauwkeurigheid ±1 px in het icoon, dus ±10% op een kop van 10 px.
  - Waar n klein is, staat het erbij. Dat is een richtlijn, geen harde regel.
- **Vellen:** `per_bouw/<bouw>.png` met per soort vier kolommen op 4×:
  1. front;
  2. front verkleind tot icoonhoogte;
  3. icoon Gen 3;
  4. icoon nu.
- **Opnieuw rekenen:** `cd meet && python3 auto.py && python3 stats.py` (uitvoer in `stats_uitvoer.txt`).

## Vijf algemene inzichten (nieuw t.o.v. ICOON_WERKWIJZE)

1. **De icoonhoogte is bijna vast, dus S is geen vaste factor.**
   - Gen 3: icoonhoogte = 14,0 + 0,12 × fronthoogte (rest ±1,4 px; max 23). Dat geeft S 0,55 bij een front van 31 px en 0,34 bij 64 px.
   - De iconen die nu in de game zitten (`icon.png`) zijn groter: 9,7 + 0,23 × fh. Dat geeft 35→18, 45→20, 55→22, 63→24 en sluit aan op de tabel in ICOON_WERKWIJZE.
   - **Volg die tabel**, want onze iconen staan naast `icon.png`-buren. Reken daarna per groep met rel-factoren t.o.v. deze S.
2. **Het icoon is dikker dan de verkleining, behalve bij compacte vormen.**
   - Oppervlak t.o.v. gewone verkleining: vogel ×1,29, tweevoeter ×1,30, plant ×1,26, viervoeter ×1,32, bol ×1,21, object ×1,16, vis ×1,04.
   - Breedte t.o.v. S: vogel ×1,29, viervoeter ×1,27, plant ×1,15, tweevoeter ×1,09, vis/bol/object ×1,02–1,06.
   - **Hoe meer uitsteeksels, hoe meer er bijkomt.** Een vis of bol is al compact en wordt gewoon verkleind; daar is het chibi-effect klein.
3. **De kop groeit in de hoogte meer dan in de breedte, en de onderkant betaalt.**
   - Kop over alle bouwtypes (n 17): breedte ×1,25 (1,14–1,32), hoogte **×1,45 (1,35–1,55)**.
   - Aandeel van de kopgroep in de figuurhoogte: 0,37 → **0,57** (0,50–0,63).
   - Poten en onderlijf krimpen ×0,65–0,88, onderlijf/steel ×0,69–0,98.
   - Rechtopstaande figuren worden dus sterker chibi dan de viscacha. Bij viervoeters ging het aandeel van 0,39 naar 0,50; bij tweevoeters gaat het van 0,38 naar 0,58.
4. **Grote attributen horen bij de kopgroep; lange dunne attributen krimpen in lengte.**

   | Soort attribuut | Voorbeelden (rel-factor) |
   |---|---|
   | Hoed, bloem, kroon (hangt aan de kop) | Ludicolo-hoed ×1,04 b / ×1,47 h; Vileplume-bloem ×1,03 / ×1,27; Sunflora-kop ×1,14 / ×1,22 |
   | Lang en dun (snorharen, staartlinten, kuif, gaswolken) | lengte ×0,30–0,65, mediaan ×0,40 (n 6): Whiscash-snorharen ×0,30, Swellow-staartlinten ×0,50, Altaria-kuif ×0,65 |

   - Wat lang en dun is, blijft wel minstens 2 px dik. Een **gedragen voorwerp** wordt korter en dikker: de Farfetch'd-stengel lengte ×0,78, dikte ×1,55.
5. **Pose:**
   - **13 van 55 krijgen een eigen pose en 2 worden gespiegeld. De vorm van het silhouet voorspelt dat niet** (solidity: wissel 0,67 tegen zelfde 0,74, overlappend). Het is een vaste ontwerpkeuze in twee gevallen:
     - (a) **frontaal aanzicht van een dier dat je normaal van opzij ziet**, wordt profiel: Pidgeot, Fearow en Ho-Oh met gespreide vleugels (3 van 3), en Goldeen;
     - (b) **ledematen of nek diagonaal ver van het lijf**, worden ingetrokken: Gardevoir, Cacturne, Baltoy, Metang, Hitmonlee, Shuckle, Tropius, Victreebel, Barboach.
   - Zonder wissel is de IoU 0,69 (0,64–0,75), met wissel 0,57. **Herhaalde details krijgen minder exemplaren:**
     - Registeel: 7 stippen → 4;
     - Claydol: 4+2 ogen → 2+2;
     - Koffing: gaswolken → losse blokjes van 1–2 px;
     - Jynx: de armen vallen weg.

   Kleuren 13 → **8** (7–9). De omlijning is dicht. De bovenrand is donker (65); de onderrand is in Gen 3 lichter (86), in `icon.png` overal 65.

## Per bouw

Overal: factoren t.o.v. S uit de hoogtetabel. De onderkant ligt op y 29 (28,5–30), het midden op x 15,5. Ankerpunt voor de kopgroep = het halsgewricht. Bij bol, object en vis is dat het midden van het lijf.

### Vis / zwemmer (n 8)
- **Gemeten:**
  - S 0,45 (0,40–0,49); breedte ×1,02; oppervlak ×1,04; IoU 0,70.
  - Lijf ×1,32 b (1,16–1,34) / ×1,00 h (n 3): het lijf wordt langer, niet hoger.
  - Kop (Barboach, n 1) ×1,72 / ×1,54.
  - Oog ×1,56 (1,38–1,88; n 3): Relicanth 2 px → 2 px, Whiscash 4 → 3. **Minimaal 2 px**, met wit en pupil zoals in de front.
- **Weglaten:**
  - Snorharen en baarddraden worden stompjes (×0,3).
  - Vinnen en uitsteeksels blijven allemaal, maar kleiner: Corsola-takken ×0,74 b / ×0,99 h, en alle 4 blijven.
- **Pose:**
  - 6 van 8 houden de pose.
  - Frontale vis (Goldeen) → profiel.
  - Verticale S-vorm (Barboach) → liggend en compact.
- **Recept:**
  1. Lijf 1,3 × S in de lengte en 1,0 × S in de hoogte.
  2. Kop (snuit tot kieuw) 1,3–1,5 × S, vast aan de voorkant van het lijf.
  3. Vinnen en staart 1,0 × S, aan hun aanhechting; kleiner dan 2 px wordt een stompje van 2 px.
  4. Draden en snorharen 0,3–0,4 × lengte, 1–2 px dik.
  5. Het oog behoudt de opbouw van de front, minimaal 2 × 2.

  Een vis is compact, dus bijna gewone verkleining. De fout zit niet in te weinig chibi maar in blur en dunne delen.

### Rechtop vogel (n 9)
- **Gemeten:**
  - S 0,36 (0,34–0,42); breedte ×1,29; oppervlak ×1,29.
  - Kop ×1,20 b (1,10–1,25) / **×1,43 h** (1,37–1,51) (n 5).
  - Kopgroep in de hoogte 0,36 → 0,50 (0,43–0,50).
  - Vleugels ×0,96 / ×0,92 (n 2).
  - Kuif, staartlinten en kroonveren ×0,50–0,65 in lengte.
  - Poten 2–3 px.
- **Weglaten:**
  - Lange kuif en staartlinten worden korter, maar houden hun richting (Altaria, Swellow).
  - Grote kammen en kuifjes blijven als blok (Noctowl-oorpluimen, Pidgeot-kuif).
- **Pose:**
  - Frontaal met gespreide vleugels → profiel met de vleugels omhoog (3 van 3).
  - Staand of in profiel: de pose blijft (Xatu, Farfetch'd, Swellow, Noctowl, Altaria).
- **Recept:**
  1. Kopgroep (kop + snavel + kuif/kroon): ×1,2 b / ×1,45 h, met het halsgewricht als anker. De kopgroep vult de helft van de hoogte.
  2. Romp ×1,0.
  3. Vleugels ×0,95.
  4. Poten worden stompjes van 2–3 px.
  5. Lange kuif- of kroonveren ×0,5–0,65 in lengte, minimaal 2 px dik.
  6. Een kroon die als blok op de kop staat, schaal je mee met de kop (×1,2–1,45), niet met de veerfactor.

  Voor Sunperor: kroon = kopgroep, en de staart- en vleugelpunten ×0,6.

### Tweevoeter / mensachtig (n 9)
- **Gemeten:**
  - S 0,35 (0,34–0,36); breedte ×1,09; oppervlak ×1,30.
  - Kop ×1,26 b (1,19–1,31) / **×1,51 h** (1,38–1,60) (n 8).
  - Kopgroep in de hoogte 0,38 → **0,58** (0,54–0,65). Dat is het sterkste chibi-effect van alle bouwtypes.
  - Benen ×0,65–0,88 (n 2); lijf onder een grote hoed ×0,74.
  - Armen en handen ×0,77–1,10.
- **Weglaten:**
  - Benen worden 4–7 px.
  - Vingers en klauwen worden blokjes; de armen van Jynx vallen helemaal weg.
  - Hoed of haar blijft met de kop één groot blok (Ludicolo ×1,04 / ×1,47, Jynx, Kecleon-kraag).
- **Pose:**
  - 7 van 9 houden de pose.
  - Diagonaal of uitgerekt (Gardevoir, Hitmonlee-trap) → rechtop en compact.
- **Recept:**
  1. Kopgroep (kop + haar/hoed/kam) ×1,25 b / ×1,5 h vanaf de nek. Die groep vult 55–60% van de hoogte.
  2. Romp ×0,9–1,0.
  3. Armen ×0,9, tegen het lijf aan getrokken als ze ver uitsteken.
  4. Benen ×0,7, minimaal 3 px.
  5. Wat in de breedte niet in 32 past, vouw je in, niet verkleinen.

### Bol / zwever (n 8)
- **Gemeten:**
  - S 0,38 (0,36–0,40); breedte ×1,05; oppervlak ×1,21; IoU 0,72; 8 van 8 houden de pose.
  - Lijf/kern ×1,07 / ×1,11 (n 2).
  - Stralen en punten ×0,9 (Solrock).
  - Gaswolken ×0,4: Koffing en Weezing krijgen losse blokjes van 1–2 px.
  - Oog: Lunatone van 9 px → ±3 px (×0,83). Grote ogen groeien dus niet.
- **Weglaten:**
  - Gezichtsdetails op de kern (Solrock).
  - Een rij ogen wordt teruggebracht tot 2 grote + 2 aan de rand (Claydol).
  - Losse handen worden kleine blobs naast het lijf (Haunter).
- **Recept:**
  1. Kern ×1,1, gecentreerd.
  2. Losse elementen houden hun plek t.o.v. het middelpunt, maar worden ×0,4–0,9 (zwevende wolkjes: 1–2 px).
  3. Gezicht: minimaal 2 px per oog; grote ogen ×0,8.
  4. Niets bijmaken.

### Object / machine (n 8)
- **Gemeten:**
  - S 0,44 (0,44–0,47), groter dan bij levende bouwtypes; breedte ×1,06; oppervlak ×1,16; IoU 0,70.
  - Hoofdlichamen ×1,14–1,27 (Magneton-bollen, Shuckle-schild); kop op een nek ×1,33 / ×1,45 (Shuckle).
  - Ogen kunnen krimpen naar 1 px (Metang, ×0,57).
  - Patronen worden uitgedund: Registeel 7 → 4 stippen.
- **Pose:**
  - 4 van 8 houden de pose, 3 wisselen en 1 wordt gespiegeld (Porygon).
  - Armen naar beneden of schuin (Metang, Baltoy) worden horizontale stompjes opzij.
- **Recept:**
  1. Hoofdvorm ×1,15–1,25, met de geometrie behouden (rechte lijnen recht, symmetrie houden).
  2. Een kop of oog op een nek ×1,35.
  3. Uitsteeksels worden stompjes van 2–3 px opzij.
  4. Herhaalde patronen tot ±60% van het aantal (de spreiding is breed).

### Plant (n 8)
- **Gemeten:**
  - S 0,40 (0,35–0,44); breedte ×1,15; oppervlak ×1,26; IoU 0,61.
  - Bloem/kop ×1,08 b / ×1,25 h (n 2).
  - Kopgroep in de hoogte 0,52 → 0,65 (n 2).
  - Steel/lijf eronder ×0,69–0,98.
  - Bladeren en handbloemen ×1,0 b / ×0,8 h (Roselia-rozen ×1,14 / ×0,76; Sunflora-bladeren ×0,93).
- **Weglaten:**
  - Wortelvoetjes worden stompjes.
  - Stippen in de bloem blijven, maar er zijn er minder.
- **Pose:**
  - 5 van 8 houden de pose.
  - Wijd gespreide armen of een lange nek (Cacturne, Tropius, Victreebel) worden ingevouwen.
- **Recept:**
  1. Bloem/kop ×1,1 b / ×1,25 h; die groep vult ±⅔ van de hoogte.
  2. Bladeren ×1,0, iets platter.
  3. Steel/lijf ×0,7–0,9.
  4. Gespreide armen intrekken als de breedte anders boven 30 px uitkomt.

### Viervoeter (controle, n 5)
- **Gemeten:** S 0,38; breedte ×1,27; oppervlak ×1,32; IoU 0,54.
- **Pose:** Ninetales wordt gespiegeld (staarten achter het lijf).
- **Recept:** zoals in `verhoudingen/STUDIE_VERHOUDINGEN.md` (kop ×1,25, lijf ×0,95). Dit sluit aan.

## Wat dit betekent voor de mislukte proeven
- **Gumfish (vis):** goed recept = vrijwel gewone verkleining.
  - Het lijf in de lengte ×1,3, het oog minimaal 2×2 met de opbouw van de front.
  - Dunne delen worden stompjes, geen blur.
  - "Kop groter" geldt hier nauwelijks.
- **Sunperor (vogel met kroon):** kroon + kop is één kopgroep ×1,2 b / ×1,45 h.
  - Die kopgroep beslaat de helft van de hoogte; de romp blijft ×1,0, de poten worden stompjes.
  - Lange veerpunten ×0,6. Niets hertekenen buiten deze factoren.

## Beperkingen
- Kopfactoren per bouw rusten op n 1–8 handmetingen (±10%). Vis-, object- en plantkoppen zijn dun bemeten (n 1–2).
- De pose-keuze zit niet in de vorm van het silhouet, maar volgt de regels (a) en (b) uit inzicht 5.
- Gen 3-iconen (`icon_gba`) en de huidige iconen (`icon.png`) verschillen in hoogte en omlijning, maar volgen hetzelfde patroon (IoU en oppervlak vergelijkbaar, zie `meet/auto.json`).
