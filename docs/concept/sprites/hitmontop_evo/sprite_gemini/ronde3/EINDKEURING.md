# Eindkeuring Hitmongroove: ronde 3 (`capoeira.png`, torso c)

Keurder: vers en onafhankelijk (8 nov). Ronde 3 is gekeurd, want Jordi koos r3 boven r4. `KEURING.md` (r3) is alleen als context gelezen; alles hieronder is opnieuw gemeten.

Waarmee vergeleken:
- het model `referenties/gemini_gekozen_capoeira.png`;
- de SPEC (toegestane afwijkingen);
- het bovenste 64×64-frame van `anim_front.png` van Hitmontop, Hitmonchan, Hitmonlee en Tyrogue;
- Breloom, Medicham, Blaziken, Hariyama en Machoke.

Alles op 1×, 2× en 8×; de steunarm op 12×.

**Plaatje:** `eindkeuring.png`.
- Boven: links r3 met de reparaties genummerd en omkaderd, in het midden een proef met reparaties 1–7, rechts het model.
- Midden: de steunarm op 12× (r3, proef, model).
- Onder: een rij op 1× en 2× met de echte Gen 3-sprites.

**Proefbestanden** (alleen ter illustratie; de maker voert de reparaties zelf uit):
- `eindkeuring_proef.png` + `eindkeuring_proef_raster.txt`: alle reparaties;
- `eindkeuring_proef_steunarm.png`: alleen 1–3.

**Coördinaten** zijn (x,y), met 0 linksboven. **Tinten:**

| Index | Kleur |
|---|---|
| 1 | zwart |
| 2/3/4/5 | huid, licht → donker |
| 6 | wit |
| 7 | grijs |
| 8/9/A | geel, licht → donker |
| B/C/D | groen, licht → donker |
| E/F | blauw |

## Metingen
| | Kleuren | Vulling | Kader | Lichtkant zwart | Schaduwkant zwart |
|---|---|---|---|---|---|
| **Hitmongroove r3** | 16 | 1205 px | 50×61 | **78%** (141/180) | 100% |
| r4 (ter vergelijking) | 16 | 1205 | 50×61 | 64% | 100% |
| Hitmontop | 14 | 1257 | 53×50 | 21% | 60% |
| Hitmonlee | 13 | 1077 | 53×53 | 33% | 70% |
| Hitmonchan | 14 | 1149 | 42×56 | 29% | 81% |
| Tyrogue | 15 | 675 | 32×46 | 17% | 43% |
| Breloom / Medicham / Blaziken / Machoke | 13–16 | 1036–1579 | | 29–47% | |
| Hariyama | 16 | 2409 | 64×64 | 71% | |

- **Huidtinten** (helderheid 199/161/116/78, stappen 38/45/38): goed. Ze liggen bijna exact op Hitmonlee's huid (238,197,164 → 98,57,24). Dat is een sterke familieband.
- **Geel** (241/206/141, stappen 35/65): ongelijk.
- **Groen** (157/106/69): goed.
- **Blauw:** maar 2 tinten (134/85); Hitmontop heeft er 4. Voor kleine voeten is 2 genoeg.
- **Wit/grijs** (248/186, stap 62): grof, maar in Gen 3 normaal.
- **Kleine vlakjes** (< 3 px):
  - bedoeld: de koorden, de vlecht, de binnenlijnen, de glimpjes;
  - echte ruis: alleen het 8/9-dambord in de steunarmband (rij 43–44).

## 1. Geloofwaardige Hitmontop-evolutie: **BIJNA**

**Wat werkt**
- Kop, ogen en kleuren lezen als familie:
  - het oog is pixel voor pixel Hitmontop;
  - huid en mond liggen dicht bij Hitmonlee;
  - de blauwe voeten komen van Hitmontop;
  - de ronde bokshand komt van Hitmonchan.
- De handstand op het hoofd is een logisch vervolg op Hitmontops kopspin. Het concept (capoeira, corda, ginga-split) is op 1× meteen duidelijk.
- Het silhouet (V van benen, bol lijf, kop omlaag) is uniek binnen de familie en toch Hitmon-achtig: een mager lijf met grote handen en voeten.

**Wat niet sterk is**
- **Hij leest niet groter of krachtiger dan Hitmontop.**
  - De vulling is 1205 px, tegen 1257 bij Hitmontop. De benen zijn dunne streepjes; de massa zit in kop en romp.
  - Een evolutie hoort zwaarder te ogen. Hier oogt hij eerder lichter en jonger. Dat ligt aan het ontwerp, niet aan de vertaling.
- **Hitmontops kenmerk is bijna weg.** Hitmontop heeft één scherpe hoorn en een "tol"-lijf. In het model staat een kleine scherpe hoorn linksonder aan de kop. In de sprite is dat een ronde nop (rij 47–49, x 5–9: `5333` / `14441` / `111`). Daardoor verliest de kop zijn laatste Hitmontop-hoek en leest hij meer als een teddy- of apenkop.
  - De hoornvorm staat in de SPEC als "nog open"; zie ter info.
- **"Niet te menselijk"** (make-fakemon-gids, "guy in a costume"):
  - De broek met vlagkleuren en de koordriem zijn het meest "kostuum" van de hele familie.
  - Dankzij het wit met grijs lezen de benen nu als gekleurde benen, niet als broek. Dat is voldoende, maar het blijft de zwakste plek van het concept.
  - Het gezicht is niet menselijk: er is geen neus. Dat is goed.

## 2. Past hij in Pokémon (Gen 3): **BIJNA**

**Wat werkt**
- Formaat, vulling en kadergebruik (50×61) passen precies tussen Hitmontop, Hitmonchan en Breloom.
- Het detailniveau is gelijk aan Hitmonlee en Medicham.
- Hij leest op 1×: V-benen, kop met twee ogen, bal-hand.

**Wat valt op**
- **Hij is zwaarder omlijnd dan alle referenties behalve Hariyama** (78% zwart aan de lichtkant, tegen 17–47%). Op 1× en 2× oogt hij daardoor donkerder en "plakkeriger" dan Hitmonlee en Hitmontop ernaast. Die hebben aan de lichtkant bruin of tan.
- **De hangende koorden** (1 px geel, aan beide kanten zwart) worden op 1× een zwart-geel laddertje. Het zijn de drukste pixels van de sprite. Dit is toegestaan, want het staat in het model.
- **De steunarm** leest op 1× als een paaltje met ringen (zie onderdeel 4).

## 3. Dragonfly Cave / Gen 3-techniek: **FAIL** (klein, alleen benoemde reparaties)

**Goed**
- 16 kleuren inclusief transparant: het maximum, maar binnen de grens.
- Geen anti-aliasing, geen losse omlijningspixels.
- Licht linksboven, en de ogen hebben hun glans linksboven.
- De bal-handen zijn schoon: een cirkel met trappen 2-1-1, een glans linksboven en een sikkel rechtsonder.
- De diagonale beenranden zijn regelmatige 1:1-trappen (geen jaggies).

**Fout**
1. **Selout:** de lichtkant is 78% zwart (zie metingen). Het grootste Gen 3-verschil.
   - Let op: in r4 werkte selout op de **dunne diagonale benen** (A en D om de pixel naast 1) niet. De beenrand werd rafelig en de A-pixels bovenaan het linkerbeen lezen als roestvlekjes.
   - Selout alleen op de grote ronde vormen: steunarm, vrije bovenarm, eventueel torso. Benen, koorden en tenen blijven zwart.
2. **Steunarmband als 8/9-dambord:** ruis, wat Gen 3 nooit doet.
3. **Torso:** een glansovaal midden in het vlak, 4-schaduw aan de lichtkant (20–21,30 en 20,31), en een sikkel die rij 31–35 constant 2 px breed is (banding). Dat is licht pillow.
   - Jordi koos bewust de glans in het midden ("het minst op een bulge").
   - De r4-sikkel linksboven maakte de torso vlak: hij leest als een plaat met een lichte rand. Die gaat er dus niet in.
   - Alleen de schaduw aan de lichtkant en de banding repareren.
4. **Kruisnaad:** 2 px brede D-binnenlijn (x 35–36, rij 21–24). Gen 3 gebruikt 1 px.
5. **Schaduwstrook rechts van de kop:** 8 rijen 2 px breed (x 23–24, rij 38–39 en verder). Kleine banding.
6. **Steunarm:** stapeling van zwarte horizontale lijnen; zie onderdeel 4.
7. **Geel:** stappen 35/65 zijn ongelijk (ter info; paletkeuze).

## 4. De steunarm: **FAIL**. Jordi heeft gelijk: hij is te recht

Wat er nu staat (x 28–36, rij 41–62):
- De torso eindigt in een **vlakke zwarte lijn** (rij 41 x 26–29, rij 42 x 29–34).
- Daaronder een **koordband als blok** (rij 43–45, 8 px breed), weer een **zwarte lijn** (rij 46), en dan een **pijp van 3×3 px huid** (rij 47–49; x 30 en x 34 kaarsrecht).
- Daarna weer een **zwarte lijn** (rij 50), de manchet (rij 51–52) en de bal (rij 54–62).

Dat zijn vier gelijke blokken met drie volle zwarte dwarslijnen in 12 rijen: een totempaal. De arm heeft:
- geen schouder;
- geen taps verloop;
- geen curve.

Ook de schaduw volgt de pijp: kolom 31 = 2, kolom 32 = 3, kolom 33 = 4 over alle drie de rijen.

**Het model** (12× naast elkaar in `eindkeuring.png`):
- De torso loopt rechtsonder vloeiend over in de arm: de rechterrand van torso en arm is één lijn, en links zit een holle oksel.
- De arm loopt duidelijk taps van ±6 px bij de schouder naar ±4 px bij de pols.
- De zwarte lijn zit alleen om de buitenkant.

**Echte Gen 3-armen** (Machoke, Hitmonchan) lopen ook taps of bollen bij de onderarm. Overgangen tussen arm en band zijn daar donkere tinten, geen volle zwarte dwarslijnen.

**Voorstel** (proef in `eindkeuring_proef_steunarm.png`; reparaties 1–3 hieronder). De lengte blijft, net als de band, de manchet en de bal.
- **De torso vloeit in de band:** de lijn op rij 42 is binnen de vorm een donkere huidtint 5, geen zwart.
- **Geen zwarte lijn onder de band:** de band sluit zelf af met zijn donkere tint A.
- **De arm begint 6 breed en loopt taps naar 5.**
  - Licht 2 alleen als blokje linksboven onder de band.
  - Schaduw 4 rechts, breder naar de pols.
- **Selout 5 op de lichtkant.**

Resultaat: de huidzone wordt 4 rijen in plaats van 3, en er staan nog 2 zwarte dwarslijnen in plaats van 4 (de manchet houdt haar omlijning).

## Reparaties (belangrijkste eerst; diff 0 erbuiten)

**1. Steunarm: schouderaansluiting en taps** (kern van Jordi's opmerking)
- Rij 42: (30,42), (31,42), (32,42), (33,42) van 1 naar 5.
- Rij 46: (29,46) van . naar 1, (30,46) van 1 naar 2, (31,46) van 1 naar 2, (32,46) van 1 naar 3, (33,46) van 1 naar 3. (34,46) blijft 1.
- Rij 47: (29,47) van . naar 1, (30,47) van 1 naar 2.
- Rij 48: (31,48) van 2 naar 3.
- Rij 49: (32,49) van 3 naar 4.
- De nieuwe arm, per rij (x 29–34):

  | Rij | x 29–34 |
  |---|---|
  | 46 | `122331` |
  | 47 | `122341` |
  | 48 | `.13341` |
  | 49 | `.13441` |

**2. Koordband steunarm: geen dambord** (gedraaid koord zoals om de vrije arm; dit deel van r4 was goed)
- Rij 43, x 28–34 wordt `A889A9A`. Was `18989A9`.
- Rij 44, x 28–34 wordt `A89A9AA`. Was `19898AA`.
- Rij 45: (30,45) en (32,45) van 9 naar A. De onderrand wordt `1AAAA1`, zodat de band zonder zwarte lijn afsluit tegen de huid.

**3. Selout steunarm en vrije bovenarm**
- (29,46), (29,47), (30,48), (30,49) van 1 naar 5.
- (30,51), (30,52) van 1 naar 7: de manchet aan de lichtkant.
- (17,26) van 1 naar 5: sluit aan op de 5-rij op (14–16,26).

**4. Torso: geen schaduw aan de lichtkant**
- (20,30), (21,30), (20,31) van 4 naar 3. De glans blijft in het midden (Jordi's keuze c).

**5. Torso: sikkel taps laten beginnen**
- (35,31), (35,32) van 4 naar 3.

**6. Kruisnaad 1 px**
- (35,21), (35,22), (35,23), (35,24) van D naar C.

**7. (Optioneel) Schaduwstrook kop taps**
- (24,38), (24,39) van 4 naar 3.

Niet doen (uit r4, maakte het slechter):
- selout A en D op de diagonale beenranden;
- grijze selout op de witte tenen (de tenen verliezen hun vorm);
- de torsoglans als sikkel linksboven.

Controle na de reparaties (gemeten op de proef): 16 kleuren, geen nieuwe tint, silhouet alleen +2 px (29,46) en (29,47).

## Ter info voor Jordi (ontwerpvragen, geen FAIL)

**r4 tegenover r3**

r4 maakte beter:
- de koordband (gedraaid koord in plaats van dambord);
- de bruine lichtkant van de steunarm;
- de kruisnaad;
- de schaduwvlek op de torso.

r4 maakte slechter:
- de torso werd vlak door de glans als sikkel;
- de rafelige beenranden door selout op 1 px-diagonalen;
- de witte tenen werden vaag.

De reparatielijst hierboven neemt alleen het goede deel over.

**Hoorn.** In het model is de kleine hoorn linksonder aan de kop een scherpe punt. In de sprite is hij een ronde nop (rij 47–49, x 4–9). Een punt (bijvoorbeeld 2 px uitsteeksel naar linksonder, eindigend in één pixel) geeft de kop zijn Hitmontop-hoek terug. Omdat de SPEC "de vorm van de kleine hoorn" open laat, is dit een vraag aan Jordi en geen reparatie.

**Evolutie-gewicht.** Hij oogt niet groter of krachtiger dan Hitmontop, door de dunne benen en dezelfde vulling. Dat zit in het bevroren model en is niet op te lossen zonder ontwerpwijziging. Alleen melden.

**Geel-palet.** A (184,140,40) lichter maken, bijvoorbeeld rond (200,156,56), maakt de stappen 35/65 gelijkmatiger. Dat raakt alle koorden en banden, dus het is een paletkeuze.

**Steunarm langer?** Na "een derde korter" plus de koordband is er nog maar 3–4 rijen huid over. Wil Jordi meer arm zien, dan kan de band 1 rij smaller (2 rijen in plaats van 3). Dat is een vraag, geen reparatie.
