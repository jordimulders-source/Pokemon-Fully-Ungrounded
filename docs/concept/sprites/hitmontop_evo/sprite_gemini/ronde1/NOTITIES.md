# Capoeira-evolutie (Hitmontop), sprite naar Gemini-model, ronde 1 (maker)

Model (bevroren): `referenties/gemini_gekozen_capoeira.png`. Twee eisen: accuraat op het model + Gen 3. Alleen de vijf afwijkingen van Jordi (SPEC "Bevroren ontwerp, 7 nov").

## Opgeleverd
- `capoeira.png`: 64×64, geïndexeerd, 16 kleuren (index 0 transparant), steunarm **een derde korter** (hoofdversie). Figuur rijen 2-62, kolommen 7-56.
- `capoeira_kwart.png`: variant met de steunarm **een kwart korter**. Dit is de hoofdversie met 1 rij extra arm. Het bovenlijf staat 1 rij hoger (rijen 1-62). Pixeldiff 0 op de rest: bovenlijf alleen verschoven, onderarm/polsband/hand identiek (bewezen met `gereedschap/kwart.py` + controle).
- `vel.png`: model en sprite op 8× naast elkaar in hetzelfde kader, plus de kwart-variant. Daaronder close-ups op 12× naast het model (kop; steunarm met koordband, polsband en hand; vuist), de benen op 8× en de sprite op 1× en 2× op licht en donker.
- Raster: `raster.txt` (hoofdversie) en `raster_kwart.txt`. Het tekenwerk staat als pixelruns, met de hand geschreven, in `hand_benen.txt` en `hand_lijf.txt`. `gereedschap/zet.py` legt ze over `onderlaag2.txt` (alleen montage).

## Werkwijze
1. **Model aangepast per script** (`gereedschap/model.py`):
   - **Steunarm korter.** Uit het rechte armstuk tussen lijf en polsband zijn rijen geknipt. De armlengte lijf→polsband is 185 modelpx. Voor de derde gaan er 62 px uit (rijen 774-835). Alles erboven zakt mee en de hand blijft staan.
   - **Ruimte voor een ronde steunhand.** Alles boven de onderkant van de polsband (y<896) is 40 px omhoog gezet. De bal is daarna met de hand getekend.
   - Diff 0 op de rest (alleen verschuiving).
2. **Kader.** De figuur is zo groot mogelijk gemaakt. De kwart-variant moet in 62 rijen passen, dus s = 14,31 modelpx per spritepx (`gereedschap/kader.json`). Beide versies hebben dezelfde schaal.
3. **Onderlaag** (`onderlaag2.txt/.png`): het masker van het model, verkleind (dekking ≥ 0,45). De buitenring is omlijning en het binnenwerk is de meest voorkomende modelkleur. Daarna is alles met de hand gedaan.
4. **Meetgereedschap vanaf de start:**
   - `rij.py`: modelklasse per halve spritepixel.
   - `blok.py`: modelklasse per spritepixel. Dit was de beslissende meting voor kop, vuist, knot, gat en strengen.
   - `rooster.py` en `naast.py`: model met spritepixelrooster, naast de sprite.
   - `overlay.py`: spritelijnen over het model.
   - `controle.py`: kleuren, silhouetverschil met het model, kleine vlakjes, losse omlijningspixels en lichte randpixels.

   Elke lijn (V-lijn, mondlijn, ogen, knotband, hoorn, strengen, lijfrand) staat op een gemeten modelpixel.
5. **Studie Gen 3:** Hitmontop en Hitmonlee op 6×. Hitmontop staat ook op zijn kop. Het oog is een zwart rondje met een wit punt. De selout is bruin aan de lichtkant.

## Palet (16)
| Index | Kleur | Gebruik |
|---|---|---|
| 0 | transparant (152,208,160) | achtergrond |
| 1 | omlijning (32,24,24) | buitenlijn |
| 2-5 | bruin: licht / basis / schaduw / donker | 5 = selout lichtkant en binnenlijnen |
| 6-7 | wit / grijs | polsbanden, knotband, tenen, ogen |
| 8-A | geel licht / geel / oker | gemeten naar het modelgeel (248,216,72) |
| B-D | lichtgroen / groen / donkergroen | D = selout van het rechterbeen |
| E-F | blauw / donkerblauw | voeten |

Helderheidsstappen: bruin ±36-45, geel 34/56, groen 42/30.

## Toegestane afwijkingen: hoe uitgevoerd
1. **Benen (kleur, niet vorm).** Het silhouet van de benen is ongewijzigd (masker). Het witte "broekje" met de harde horizontale grens is weg. De strepen van het scheenbeen lopen in de lengte van het been door tot aan het koord: lichtgroen (lichtkant), geel en groen. Het rechterbeen heeft donkergroene selout aan de linkerkant, zoals het model daar groen omlijnt. In het kruis zit een smalle donkergroene vouwlijn (kolom 36, rij 21-26), zoals de vouw in het model.
2. **Torso bol.** Eén bol met een glansvlek linksboven (2), basis (3), een sikkelschaduw rechtsonder (4) en een donkere rand rechts en onder (5). Er zijn geen anatomielijnen.
3. **Vuisten volle ballen.**
   - Bovenvuist: alleen kleur. Glans linksboven, sikkel rechtsonder en selout linksboven. De onderrand is aaneengesloten.
   - Steunhand: nu een ronde bal van 9 breed × 9 hoog (kolom 28-36, rij 54-62). De bovenste rij zit achter de polsband. Glans linksboven en een sikkel rechtsonder. De polsband werpt een schaduwrij (rij 55).
4. **Steunarm korter.**
   - Hoofdversie: lijf-onderkant (rij 41) tot polsband (rij 51) is 9 rijen. Modelequivalent van de oorspronkelijke arm op deze schaal: 12,9.
   - Kwart-variant: 10 rijen. Het verschil tussen een derde en een kwart is op deze schaal maar 1,1 px, dus 1 rij.
5. **Koordband om de steunarm.** Dezelfde gele gevlochten band als bij de vrije arm, direct onder het lijf (rij 42-45). Hij is 1 px breder dan de arm aan elke kant (omwikkeld). Het vlechtpatroon is schuin, een 3-cyclus 8/9/A, gelijk aan het taillekoord en de band van de vrije arm.

## Afwijking van de onderlaag per zone
Gemeten als pixels die anders zijn dan `onderlaag2.txt`:

| Zone | Anders | % |
|---|---|---|
| Voeten | 48/170 | 28% |
| Benen | 135/268 | 50% (strepen in plaats van wit, opzet) |
| Touw + strengen | 114/203 | 56% (vlecht, doorlopende band, strengen op de modelkolommen) |
| Lijf | 107/252 | 42% (bolle schaduw) |
| Vrije arm + vuist + polsband | 71/159 | 44% |
| Kop + knot + hoorn | 69/305 | 22% |
| Steunarm + koordband | 44/64 | 68% (koordband is nieuw) |
| Polsband + hand | 48/90 | 53% (bal is nieuw) |

**Silhouet tegen het model** (buiten de zone steunarm/band/hand): 45 px verschil.
- 12 px zijn het gat tussen de vrije arm en de kop. Dat is in het model achtergrond, maar ingesloten wit, dus het masker telt het als figuur. In de sprite is het transparant, zoals het model het toont.
- De rest zijn omlijningspixels op de rand van het masker (modeldekking 0,2-0,44). Er zijn geen grote vormverschillen.

**Controle:** 0 randpixels zonder donkere rand en 0 losse omlijningspixels midden in een vlak. De kleine vlakjes die overblijven zijn bedoeld: lijnstukken in selout, het vlechtpatroon, oogwit, teen- en polsbandgrijs, en 2-px stukjes in de dunne elleboog.

## Eerlijke zwakke punten (na eigen reparaties)
1. **Taillekoord.** Het binnenwerk is 2 rijen dik, het model heeft ±1,5. De onderrand van het koord ligt daardoor ±0,5-1 px lager dan in het model en de bovenkant van het lijf onder het koord is 1 rij smaller. Dit is gedaan omdat een vlecht van 1 rij als trapjes las.
2. **Linkerstreng.** Die eindigt 1 px breed, zoals het modelmasker. Het kwastje aan het eind leest daardoor niet als een dikker knoopje. In het model is het net iets breder dan 64 px kan tonen.
3. **Hoorn.** De onderrand staat op rij 49, waar het model 0,2-0,3 dekking heeft (±1 px lager). Dat is gedaan om de hoorn 2 rijen dik en leesbaar te houden. De vorm van de hoorn staat in de SPEC nog open.
4. **Ogen** zijn 3 px, zoals gemeten in het model. Het wit staat in het midden, zoals in het model, en leest op 8× als een rondje met een gat. Op 1× is het een oog met een glimpje.
5. **Wit uit de benen.** Het wit is helemaal uit de benen verdwenen: de strepen lopen door tot aan het koord. Als Jordi het wit als lengtestreep terug wil, is dat een variant om te vragen. Die heb ik niet gemaakt; ik heb niets zelf ingevuld.
6. **Voeten** hebben geen glanstint, omdat het palet vol is (16). Dit is plat blauw, zoals in het model.
7. **Kwart-variant** verschilt maar 1 rij armlengte van de hoofdversie. Dat volgt uit de schaal: het verschil tussen een kwart en een derde van een arm van 13 px.
8. **Scheenbenen.** De lichtgroene lengtestreep op de scheenbenen is 1 px breed. Bij diagonale benen breekt de clusterscan die in stukjes van 1-2 px, maar op 8× leest het als een doorlopende streep.

## Niet gedaan (volgens opdracht)
Geen keurder gestart, niet gecommit of gepusht.
