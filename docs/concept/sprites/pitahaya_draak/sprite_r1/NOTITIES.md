# Pitahaya-draak fase 1, sprite r1 (maker)

Methode: model overnemen, niets tekenen (Krassault / blobfish r1 / ijskomeet r15). Jordi: "niks zelf tekenen, totdat er een vorm staat, volg de geslaagde lessen van recente sprites".

## Stappen
1. `natief.py` (kopie van `blobfish/sprite_r1/natief.py`, pitchbereik 5,0–5,25): raster **5,118 px** (fase 4,25), natief **199×199**, figuur **94×148**. De pitchzoeker over 4–16 px geeft 10,24 als hoogste piek (veel details zijn 2 natieve px), maar op een uitvergrote uitsnede (oogglans, pupil) zijn de cellen 5,12 px; 5,12 scoort 2,4× het gemiddelde.
2. `groepen.py`: elke natieve modelpixel in een kleurgroep (achtergrond = bijna-wit verbonden met de rand, zwart lum < 42, wit, amber, groen G ≥ R, mauve kin |G−B| ≤ 10, roze) en per groep tonen (k-means, gezet op echte modelkleuren). Controle: `groepen.png`.
3. `half3.py`: **exacte 3×3-reductie met regels** (afgeleid van `half4.py`). Per spritepixel uit zijn eigen 9 modelpixels: achtergrond bij ≥ 5/9; schubpunt in het hoofd (modelrij < 110) bij ≥ 3 groene px en < 4 zwarte → groen (anders verdwijnen de punten onder hun zwarte rand); **lijn bij ≥ 2 zwarte px (donkerste wint, ijskomeet r15)**; wit bij ≥ 2; amber bij ≥ 3; anders de meerderheidsgroep: roze met ≥ 2 px lum < 78 → toon van de donkerste pixel (dunne mondlijn/schubnaden), groen met ≥ 3 px donkerste toon → donkerste groen (ribbels), anders gemiddelde → dichtstbijzijnde toon. Alle 9 fases gemaakt (`fases/alle.png`, nog met de eerste regelset); gekozen **oy=0, ox=1** (beide ogen tonen amber onder het ooglid, mondlijn het meest doorlopend). Aanroep: `python3 half3.py kaal.png 0 1 78 2 3` → `kaal.png` + `kaal_info.npz`.
4. `maak_r1.py`: alleen technische opschoning op `kaal.png` → `pitahaya_r1.png`; elke wijziging in `afwijkingen.txt`. Silhouet-diff met de kale reductie: **0**.

Hulpmiddelen: `gezvel.py` (gezicht sprite | natief model), `vel.py`.

## Maat
Gen 3-basisvormen (frame 1, breed×hoog, px): Bagon 28×45 763, Larvitar 33×45 771, Dratini 47×45 753, Treecko 41×45 846, Chikorita 39×44 903, Pupitar 36×43 980, Shelgon 39×45 1271 (fase 2).
Gekozen: de 3×-reductie zelf, **31×49, 1087 px**, onderste rij **y = 55**, x 16–46 (horizontaal gecentreerd). Even hoog als Bagon/Larvitar (+4 rijen); meer px door het grote ronde hoofd. 4× zou 24×37 ≈ 600 px zijn (kleiner dan Torchic, ogen en mond vallen weg); een tussenfactor kan niet zonder hertekenen of middeling.

## Palet (13 + transparant, allemaal modelkleuren)
| idx | kleur | helderheid | rol |
|---|---|---|---|
| 1 | (17,17,26) | 18 | zwart: lijn, schaduwkant |
| 2 | (113,36,59) | 61 | donkerroze: selout hoofd, mondlijn, schubnaden |
| 3–5 | (163,53,86) (219,89,131) (225,140,162) | 89 / 132 / 167 | roze schaduw / basis / licht |
| 6 | (181,112,115) | 132 | mauve kin (idx 7 in palet, ongebruikt) |
| 8 | (53,87,57) | 73 | donkergroen: selout + schaduw rank |
| 9–11 | (80,113,76) (107,137,94) (146,172,126) | 98 / 123 / 158 | groen schaduw / basis / licht |
| 12–13 | (189,127,75) (231,184,118) | 139 / 190 | amber ogen |
| 14 | (239,240,234) | 239 | wit: tandje, oogglans, stekeltjes |

## Afwijkingen van de kale reductie (118 px van 1087; 121 stappen, 3 px twee keer)
| Stap | Reden | hoofd/gezicht | schubpunten | lijf | armen | poten | totaal |
|---|---|---|---|---|---|---|---|
| B | buitenlijn 1 px: zwart aan de schaduwkant (normaal onder/rechts), selout aan de lichtkant (roze → idx 2, groen → idx 8); geen lichte tint op de rand | 8 | 29 | 4 | 15 | 7 | 63 |
| C | ruis: losse vulpixel (8-verbonden cluster van 1) → meest voorkomende buurtint uit dezelfde kleurgroep | 7 | 2 | 3 | 5 | 7 | 24 |
| C2 | ontkorrelen (Krassault): vlakjes < 3 px (4-verbonden) in de middentinten roze 3/4 en groen 9/10 → meest voorkomende 4-buur uit dezelfde groep; lichtste tinten (glans), lijnen, ogen bevroren | 12 | 2 | 3 | 11 | 2 | 30 |
| D | per pixel naar het model (hieronder) | 4 | 0 | 0 | 0 | 0 | 4 |

Zones: hoofd/gezicht = y ≤ 36 behalve groen; schubpunten = groen in y ≤ 36; poten = y ≥ 48, x 19–44; armen = x ≤ 22 of ≥ 39 (y 37–47); lijf = de rest.

Stap D, elke pixel (x,y):
- (30,25) zwart → donker amber: nabije oog, iris links van de pupil; 3 zwarte modelpx (rand ooglid) maakten hem lijn, 6 amber px, gemiddeld (184,126,76).
- (33,25) zwart → donker amber: iris rechts van de pupil; 2 zwarte px (pupilrand, < 1 spritepx breed), 4 amber, gemiddeld (200,140,86).
- (31,25) donker amber → wit: oogglans; het model heeft daar een witte glanspixel (255,241,223) linksboven de pupil, onder de drempel van 2.
- (28,32) roze → donkerroze: mondlijn; de dunne diagonale modellijn (1 px lum 41 in het blok) viel weg, waardoor de lijn brak tussen (27,32) en (29,31).

## Gezicht (12× naast het model, vel.png)
- Nabije oog (x 29–35, y 23–26): zwart ooglid schuin, amber iris met glans (31,25) en zwarte pupil (32,24–25), lichte amber onderrand; leest als het halfgesloten, brutale oog van het model.
- Verre oog (x 19–22, y 24–26): amber kolom met zwart rechts (pupil/ooglid), zoals het model; ongewijzigd.
- Mond: donkerroze lijn van onder de snuit (19,31) tot het tandje (32,30–31); mauve kin eronder; lichtroze snuitbult (y 27–28). Tandje = 2 witte px met zwart eromheen, uit de reductie.

## Zelf geziene zwakke punten
- **Rechterkant van het hoofd vrij zwart en streperig**: de zwarte randen van de schubpunten worden met "≥ 2 zwarte px → lijn" verticale zwarte streepjes (x 39–45, y 8–30). Ze staan in het model (zwarte schaduwkant van elke punt), maar lezen op 1× drukker dan in het model. Met drempel 3 werd de buitenlijn op armen en hoofd open; daarom 2 gehouden.
- **Schubpunten klein**: op 3× zijn de groene punten 1–2 px; de grote achterste punten (rechtsboven) lezen, de kleine links lezen vooral als groene vlekjes op de rand.
- **Contrast groen**: stap 9 → 10 is 25 helderheid (Gen 3 ±30–40); een paletronde (alleen waarden) kan later.
- **Maat**: 1087 px is ruim voor een eerste fase (Bagon 763); de hoogte (49) is wel Bagon-maat. Kleiner kan alleen met een andere methode (middeling), dan vallen ogen en mond weg.
- Verre oog is 1 px breed amber; groter maken = afwijken van het model, niet gedaan (ogen komen volgens SPEC later apart met Jordi).
