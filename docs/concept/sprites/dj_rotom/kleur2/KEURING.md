# DJ Rotom kleur2 – onafhankelijke keuring (5 nov)

Gekeurd: `dj_rotom_A.png`, `dj_rotom_B.png` (64×64, P-modus, transparency=0, 15 van 16 indexen gebruikt).
Vel: `keuring_vel.png` (A en B op 1× licht/donker naast de 6 Rotoms + magnemite, magneton, voltorb, electrode,
porygon, porygon2, bronzor, klink, klang, golett, cryogonal, sigilyph; 3× naast Frost, Wash, Heat en Mow; de bron).
Oordeel gevormd vóór het lezen van NOTITIES.md.

## 1. Hoofdvraag: **FAIL** (klein, te repareren)
- **Rotom-vorm uit dezelfde game: ja.** Op 1× staat hij zonder schuren naast Heat/Wash/Frost: zelfde oranje (game-oranje
  e67329), 2 px gloed zonder zwarte buitenlijn, Rotom-ogen, spits. Even breed als Frost/Wash.
- **DJ Rotom uit de bron: bijna.** Speakers, oranje kop met gezicht, zwart display met groene equalizer en het snoertje lezen.
  Het kenmerk bovenop niet: **de bliksem met noot leest op 1× als een groen spruitje/blaadje op een steeltje** (spits + smal
  getaperd blok + witte schuine streep = blad met nerf). Geen zigzag, geen noot. Dat is precies het onderdeel dat hem van
  "een Rotom met speakers" tot DJ Rotom maakt.

## 2. Harde eisen (SPRITE_NORM)
| # | eis | oordeel | reden |
|---|---|---|---|
| 1 | leest op 1× als echte Pokémon | PASS | Leest als Rotom-vorm naast 18 echte sprites; massa 1894 px (Frost 2173, Wash 1681). |
| 2 | 3/4 links-voor | **FAIL** | Zijvlakken rechts en grotere nabije rechterspeaker kloppen, maar de kop doet niet mee: boven- (y32) en onderrand (y57) van de kop zijn vlak terwijl beide speakers kantelen, en het gezicht vult het hele voorvlak (rechteroog x26–30 raakt het zijvlak op x31). Bij Frost staat het gezicht in het linker/middendeel van het voorvlak en blijft rechts oranje over. |
| 3 | ledematen (analogie: plasma) | **FAIL** | De bliksem is vast aan de spits, maar het onderste deel is een stokje: 1 px kern (`h`, x27 y22–25) met aan elke kant 1 px gloed. Geen herkenbare Z-knik zoals in de bron (breed scheef blok → knik → dunne staart). |
| 4 | geen Escher | PASS | Overlap consequent: kop vóór linkerspeaker (naad x15), achter rechterspeaker (naad x35); snoer over het zijvlak van de kop klopt met de bron. |
| 5 | skelet, curven | PASS (analogie) | Kasten mogen recht (Frost). Opmerking: de hoeken zijn harder dan bij Frost (die rondt 2–3 trappen af) en de bron (zacht speelgoed). |
| 6 | kop | PASS | 26 van 49 rijen (53 %), kopoppervlak ±27 %. Opmerking: voorvlak 14×24 (1 : 1,7) is een zuil, de bron is bijna een kubus (1 : 1,2); Jordi vroeg "groter", het werd vooral "hoger". Zie reparatie 2. |
| 7 | ogen | PASS (Rotom-stijl) | Opbouw als Frost/Mow: wit rondom, zwart opzij, iris donker boven (`t`) / licht onder (`e`). Geen donker bovenlid, maar dat heeft geen enkele game-Rotom; de stijlnorm van Jordi gaat voor. |
| 8 | kenmerken op 1× leesbaar | **FAIL** | (a) Noot onleesbaar: 9 witte px als schuine streep (x22–25, y16–21) op lichtmint; de maker zegt zelf "de noot pas vanaf 2–3×" (zelfgenoemd zwak punt = fail). (b) Conussen van de rechterspeaker lezen op 2–3× als sleutelgat/stopcontact: dikke zwarte bovenkom + 2 px verticaal grijs streepje onder het midden (x45 y40–41 en y52–53). |
| 9 | omlijning, licht, open randen | **FAIL** | Geen open randen (script). Maar: (a) zwart staat alleen op 4 px in de hoek rechtsonder ((59,59) los + x55–57 y60) – leest als een zwart vlekje/voetje; game-Rotoms zetten zwart óf langs de hele schaduwkant (Frost x51/y57) óf nergens. (b) Het licht op de conussen komt van onderen (glans onder het midden) terwijl de rest van linksboven belicht is. |
| 10 | geen Chernobyl | PASS | Eén aaneengesloten vorm (1 component), geen beige vlakken, gezicht niet misvormd. |

## 3. Stijl van de game-Rotoms
- **Gloedrand:** opbouw klopt (buiten donker `g`, binnen `G`, 2 px; brede gloedzones onder links en boven rechts in `G`, net als Frost). Wel bleker en minder contrastrijk dan alle zes game-gloeden (die hebben een verzadigde, donkere buitentint: Wash 0848c0, Mow 009800). Op licht valt de rand weg; dat komt door de bronkleuren (smaakkeuze, zie §8).
- **Oranje:** exact de game-tinten (f6a483 / e67329 / bd4a18 / 7b3920). Goed; de bron (≈ e2673c) verschilt nauwelijks.
- **Ogen:** echte Rotom-ogen; schuin en iets "sluw" zoals Frost/Heat. Formaat (±4–5 × 6) gelijk aan Frost.
- **Spits:** opbouw goed (lichte streep links, schaduw rechts), maar smal en lang (2–3 px breed over 7 rijen); samen met de bliksem wordt het een steeltje. Frost/Wash: voet 5–7 px, sneller taps.
- **Shading/volume:** zijvlakken en hooglichtrij bovenaan kloppen. Het voorvlak van de kop is vlak `O` van y45 tot y56: Frost en Wash laten het voorvlak onderaan en rechts naar `r` aflopen (Frost y53–56 `3333`), daardoor hebben ze volume. De speakerfronten zijn één vlak navy zonder randglans; acceptabel (bron is ook vlak zwart).

## 4. Trouw aan de bron
| onderdeel | oordeel |
|---|---|
| speakers | Goed: links lager/kleiner, rechts hoog met twee conussen, zwarte (navy) fronten met smalle oranje rand, zijvlakken rechts. Conusvorm: zie eis 8b. Linker conussen klein maar leesbaar. |
| kop | Oranje kast met spits: ja. Verhouding te hoog (zuil i.p.v. kubus); bij de bron zit de kop lager dan de linkerspeaker, hier steekt hij erboven uit (bewuste keuze "groter", maar breedte had meer opgeleverd dan hoogte). |
| ogen | Rotom-stijl in de kleuren van de bron (wit, blauwgroen). De bron heeft ronde, rechtop staande, blije ogen; de sprite schuine. Past bij Jordi's stijleis. |
| grijns met tandjes | Aanwezig (mondhoeken y42, 3 witte px y43, zwarte onderlijn y44); op 1× een lachje, tandjes vanaf 2×. Voldoende. |
| display met equalizer | Groot zwart display in de onderste helft: ja. Bron: bovenrand golvend (grijns met tanden), ±9 kolommen blokjes. B komt dichter bij (golvende rand, meer en smallere kolommen). |
| snoertje | Ja, y51 naar beide speakers. **B: het linker snoer raakt het display niet** (x17 y51 is oranje tussen snoer x14–16 en display x18). |
| bliksem met noot | **Niet trouw**: bron = breed scheef parallellogram met witte achtste noot, scherpe knik, dunne staart naar de spits. Sprite = smal blaadje met witte streep. |
| kleuren | Palet uit de bron (navy fronten 182031 ≈ bron 181d34, mint gloed, blauwgroene iris, groene equalizer); oranje = game-oranje. Goed. |

## 5. Technisch (script op de indexrasters)
- Open randen (niet-gloedkleur 4–15 naast transparant): **0** (A en B). Binnengloed `G` naast transparant: 0.
- Componenten: 1 (1894 px, A en B).
- Losse pixels (geen enkele buur, ook diagonaal, met dezelfde index): A 6, B 12.
  - A: (25,16) en (27,22) gloed in de bliksem; (27,38) iris; (9,43) navy en (9,44) grijs in de kleine conus; **(59,59) zwart** (de losse zwarte hoekpixel).
  - B: dezelfde 6 + de equalizertoppen (23,50), (27,50), (21,51), (25,52) en voeten (19,53), (25,53) – inherent aan 1 px-staafjes.
- Kleuren: 15 + transparant; index 0 = 98d0a0 (zelfde conventie als de game-Rotoms). Bbox x2–61, y14–62.

## 6. A of B: **B**
- De golvende bovenrand lijkt meer op de grijnzende displaymond uit de bron; A's twee hoorntjes lezen op 2–3× als een kattenkop.
- 5 smalle staafjes lezen op 1× meteen als equalizer (de bron heeft veel smalle kolommen); A's 4 blokjes lezen als groene tanden/klodders.
- B laat links en rechts 1 px oranje naast het display, zoals de bron; A plakt het display tegen de linkerrand van het voorvlak.
- Voorwaarde: het snoergat in B dichten (reparatie 5).

## 7. Reparaties (per zone, uitvoerbaar)
1. **Bliksem met noot (x19–30, y14–25)** – de belangrijkste. Maak het bovenste blok een scherp parallellogram en verbreed het
   2 px naar rechts (binnenkant x21–27, y15–20; Jordi gaf ruimte: "bliksem noot mag idd dikker"), met een harde schuine
   rechterbovenhoek. Zet er een rechtopstaande achtste noot in: steel x25 y15–19, vlag (26,15)–(26,16), kop 2×2 op (23–24, 19–20);
   de rest van de kern `G`, geen `h` om de noot heen zodat wit tegen mint het enige contrast is. Daaronder een duidelijke knik
   naar rechts (y21–22) en een staart met **2 px kern** (`h`+`G`, x26–27, y22–25) die in de punt van de spits loopt.
   Toets op 1×: moet lezen als "bliksem met noot", niet als blad.
2. **Kop in 3/4 (x31–32, y32–57)**: maak x31–32 voorvlak (`O`, bovenrij y33 `o`, bovenrand y32 `r`) en laat het zijvlak x33–35
   (`r r R`); omtrek ongewijzigd. Laat de ogen staan, zodat er rechts 2–3 px oranje naast het rechteroog overblijft (zoals Frost),
   en schuif display/grijns 1 px mee naar rechts of laat ze staan (display dan x18–30). Optioneel: bovenrand van de kop 1 rij laten
   stijgen naar rechts (x26–32 op y31) zodat hij meekantelt met de speakers.
3. **Conussen rechterspeaker (x40–50, y34–55)**: haal het grijze streepje weg ((45,40),(45,41),(45,52),(45,53) → `n`) en zet een
   stofkap van 3×3 `s` in het midden (boven: x44–46 y38–40; onder: x44–46 y49–51) met één `S`-glans linksboven ((44,38) en (44,49)).
   Maak de zwarte kom boven 1 rij dunner (y36 resp. y47 → `s`/`n` aan de linkerbovenkant) zodat het een ronde conus wordt i.p.v. een sleutelgat.
   Kleine conussen links idem: (9,44) `S` → `K`, (9,43) → `S`.
4. **Zwarte hoek rechtsonder (x55–59, y59–60)**: (59,59) en (55–57,60) → `R`. (Of, als Jordi het Frost-model wil: een doorlopende
   zwarte schaduwlijn langs x58 y33–59 en y60 x45–57 – niet half.)
5. **Snoer B (17,51)** → `K`, zodat het linker snoer het display raakt. Tegelijk volume op het kopvoorvlak: y55–56 x18–30 en kolom
   x30 (na reparatie 2: x32) y45–56 van `O` naar `r`, zoals Frost onderaan.
6. (klein) **Spits (x25–29, y26–32)**: voet 1 px breder (x24–30 op y31–32), punt 1 rij lager, zodat hij een kegel is en geen steel.

## 8. Smaakkeuzes voor Jordi (geen opdrachten)
- **Gloed:** brontrouw bleekmint (nu) of iets donkerder/verzadigder buitentint (bijv. 2a8860) zodat de rand op licht net zo hard staat als bij de game-Rotoms.
- **Ogen:** schuine Rotom-ogen (nu, game-stijl) of rondere, rechtop staande ogen zoals in de bron (blijer, minder "sluw").
- **Kopverhouding:** zuil (nu, steekt boven de linkerspeaker uit) of meer kubus zoals de bron (2–3 rijen lager bovenkant).
- **Gekantelde kop:** volledig meekantelen met de speakers of vlak laten (Frost is ook vlak).
