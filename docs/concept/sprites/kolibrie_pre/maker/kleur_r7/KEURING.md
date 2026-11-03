# Keuring kolibrie pre-evo, kleur r7a en r7b (onafhankelijke keurder, 3 nov)

Gekeurd:
- **r7a:** `kolibrie_pre_r7a.png` = `raster.txt`.
- **r7b:** `kolibrie_pre_r7b.png` = `raster_r7b.txt`.

Beide png's zijn gelijk aan hun raster (0 px verschil). Het palet `normal.pal` is gelijk aan r6.
Eerst zelf geoordeeld en gemeten; `NOTITIES.md` pas daarna gelezen.
Jordi, letterlijk: "het hoofd is nog steeds veel te 2d", "misschien moet er een draai plaatsvinden", "en ik vind het oog ook nog steeds niet mooi, is geen pokemon oog, steel er desnoods een".

Vel: `keuring_vel.png`. Het bevat:
- r7a en r7b op 8× met FAIL-zones, naast Taillow op 8×;
- de koppen op 14×: r7a | r7b | Taillow | Starly (de bron van het oog);
- 3× op licht en donker: r6, r7a, r7b, Taillow, Starly, Pidgey, Natu, Swablu;
- 1× op licht en donker: r6, r7a en r7b naast 10 referenties.

Coördinaten zijn (x, y), 0-geteld, zoals in de rasters.

## Kern: waarom de kop nog 2D is (naast Taillow)
- **Beide koppen staan in zuiver profiel.** De snavel steekt aan de omtrek uit de kop: de bovensnavel zet de voorhoofdslijn voort, de ondersnavel de kinlijn.
- **Bij Taillow (en Starly) zit de snavel ín het gezicht.** Hij is kort, breed en verkort, en links ervan en erboven is nog gezicht te zien. Dat is wat een kop 3/4 maakt. Norm 2: "de kop draait meer naar de kijker dan het lijf"; in r6 heb ik dat te mild als PASS gerekend.
- **r7b verschuift de snavel 2 rijen omlaag en het oog 3 px naar voren.** Op 3× en 1× is er nauwelijks verschil met r7a: de draai leest niet. De snavel heeft dezelfde lengte en hoek en zit nog steeds op de omtrek. Het enige dat wel in 3/4 leest, is de gevulde mondhoek (`D` met `C`-rand).
- **De belichting van de kop is verbeterd en is niet meer het probleem.** De hooglichtvlek op de koepel, de `E`-sikkel achter, de `3`-sikkel onder de wang en de `5` als slagschaduw op de borst kloppen.
- **Wat de kop nog plat maakt, naast het profiel:** de kapnaad. Die loopt als donkere `2`-lijn door het gezicht en tekent kap en gezicht als twee platte vlakken. In r7b is het een omlijnd kader rond het oog. Taillow scheidt kap en gezicht alleen met kleur, zonder lijn.

## Het oog (Starly, pixel voor pixel)
- **Het oog zelf is een Pokémon-oog.** Een zwart ovaaltje 3×5 met een witte verticale glans van 2 px, een lichte onderkant `5` en zijkanten `2`. Die zijkanten zijn trouw aan Starly: op dezelfde verhouding tussen zwart en huid als Starly's grijs.
- **Het is wel een frontaal oog.** Starly kijkt de kijker aan omdat zijn kop 3/4 naar voren staat. Op een kop in profiel met de snavel opzij (r7a, en feitelijk ook r7b) staart het oog de speler aan terwijl de kop opzij kijkt.
- **Het oog klopt dus pas als de draai klopt (B1).** In r7a is het een mismatch (A2).

## Metingen
| meting | r7a | r7b |
|---|---|---|
| px | 734 | 734 |
| alpha-diff tegen r6 | 0 | 32, alleen in de kopzone (x ≤ 18, y 10–21); lijf gelijk |
| kleurdiff tegen r6 | 91 | 181 |
| aandeel zeer donker | 0,193 | 0,191 |
| niet-`1` naast transparant | selout `2`, gaap `D`, pootjes `A`, teen `F` (25,43): alle als selout of pseudo-omlijning van dunne delen | idem |
| losse pixels | oog (26,17), kin (15,19), keel (21,21), veerrand (37,32), poot (27,42) (25,43): allemaal bewust | oog (23,17), keel, veerrand, poot: bewust |
| 2×2-klonten zwart | 0 | 0 |
| voorhoofdomtrek (looplengtes) | 4-2-2-2-1-1 (r6) | **4-2-3-2-1-1**: besluiteloos door (18,11) |
| lijf y ≥ 27 | r7a en r7b identiek | – |

## FAILs van r6 nagelopen (beide varianten gelijk)
| r6 | oordeel r7 | toelichting |
|---|---|---|
| 1 kruinhooglicht | PASS | vlek met breedtes 3-4-4-2 (x 20–24, y 10–13); los van de omlijning |
| 2 oog | vervangen | Starly-oog; zie hierboven en A2 en B1 |
| 3 keelveertjes | PASS | één 2×2-vlekje `98/88` op (21–22, 21–22). Klein maar samenhangend. Het argument van de maker (mijn `998/888` las als onderlip) neem ik aan |
| 4 veerlijnen | PASS | `4-2-2-E` en `4-4-2-2-2`; op 8× overlappende veren. (37,32) is een losse lichte pixel, maar het is een veerpunt en storend is het niet |
| 5 flank | PASS | `3`, geen banden meer |
| 6 vleugelvoorrand | PASS | licht alleen bij de schouder |
| 7 poot | PASS | `1FAA1`; leest als voet |
| 8 bovensnavel | PASS | `D`-binnenrand; leest op donker |

## Tabel r7a
| # | onderdeel | oordeel | waar / waarom |
|---|---|---|---|
| – | formaat, palet, silhouet (alpha-diff 0) | PASS | |
| – | lijf, vleugel, buik, staart, pootjes | PASS | zie hierboven |
| – | kopbelichting | PASS | vlek, sikkels, slagschaduw op de borst |
| A1 | **kop 3/4, draai** | **FAIL** | zuiver profiel: snavel (8–16, 10–19) aan de omtrek, geen gezicht links van de snavelbasis. Jordi: "te 2d" |
| A2 | **oog in perspectief** | **FAIL** | frontaal Starly-oog (24–28, 14–18) op een profielkop: staart de speler aan. De kapnaad loopt in de linkeronderhoek van het oog (23,17) (24,17), waardoor het oog een staartje krijgt |
| A3 | **kapnaad** | **FAIL** | donkere `2`-lijn door het gezicht: (17–19,14) (20,15) (21,15) (22,16) (23,17), achter het oog (29,18) (30,19). Deelt de kop in twee platte vlakken; Taillow gebruikt alleen een kleurgrens |
| – | bek (kort, open, gaap) | PASS | als r6 met de `D`-binnenrand |

## Tabel r7b
| # | onderdeel | oordeel | waar / waarom |
|---|---|---|---|
| – | formaat, palet; omtrek alleen in de kopzone gewijzigd | PASS | Jordi vroeg de draai, dus de omtrek mag daar veranderen |
| – | lijf, vleugel, buik, staart, pootjes | PASS | identiek aan r7a |
| – | kopbelichting | PASS | als r7a |
| – | gaap, mond in perspectief | PASS | gevulde mondhoek `D` met `C`-rand (13–16, 14–20) leest op 1× als bedelbek |
| – | oog zelf | PASS | Pokémon-oog (22–24, 14–18); het perspectief hangt aan B1 |
| B1 | **draai leest niet** | **FAIL** | De snavel (9–16, 12–21) is even lang, even schuin en zit nog steeds op de omtrek. Er is geen verre wang of voorhoofd links van de snavelbasis. Op 3× en 1× is de kop gelijk aan r7a. Daardoor staart het frontale oog nog steeds opzij |
| B2 | **kaplijn-koepel rond het oog** | **FAIL** | De `2`-lijn (20–24,13), (25,14) (26,14), (27,15), (28,16) (28,17), (29,18) plus de naad (18,14) (19,14) (17,15) (16,16) zet een donker kader om het oog: leest als bril of masker, en dus plat. (20–24,13) ligt als rechte lijn van 5 px op het zwarte ooglid (22–24,14): dubbel lid, zware wenkbrauw |
| B3 | **voorhoofdcurve** | **FAIL** (klein) | looplengtes 4-2-3-2-1-1 door (18,11): besluiteloos (§3) |

## Reparaties
**Advies: ga verder met r7b.** Alleen daar kan het frontale Starly-oog kloppen, en de mond in perspectief werkt al.

**B1, de draai (zone x 8–20, y 11–22; omtrek mag hier wijzigen).** Leg Taillow als skelet over de kop:
- **Snavel in het gezicht:** de bekbasis 2–3 px naar rechts, ín het gezicht. Daardoor wordt de voorhoofds- en wanglijn links van de bekbasis zichtbaar. Dat is de verre kant van de kop: 1–2 kolommen `5` met selout `2` op x 12–14, y 14–20, zodat het gezicht om de bekbasis heen loopt.
- **Snavel verkort:** bovensnavel 4–5 px in plaats van 7, en minder steil (meer naar links dan naar boven); 2 px vulling `F` met de `D`-binnenrand. Ondersnavel 4 px.
- **Jordi's punten blijven:** de snavel blijft kort en open. Het oog blijft waar het staat (x 22–24); met de snavel in het gezicht staat het dan op de goede afstand.
- Controle: op 3× moet je naast r7a zonder raster zien dat de kop naar je toe draait.

**B2, kaplijn (±14 px).** Kap en gezicht alleen met kleur scheiden:
- (20,13) t/m (24,13) `2` → `B`: het zwarte bovenlid van het oog doet het werk.
- (25,14) en (26,14) `2` → `B`; (27,15) `2` → `B`.
- (28,16) en (28,17) `2` → `E`; (29,18) `2` → `E`.
- (18,14) en (19,14) `2` → `4`; (17,15) en (16,16) `2` → `5`.

Het gezicht wordt dan één licht vlak van snavel tot oog, met de `4`-strook achter het oog als wang.

**B3 (1 px, omtrek).** (18,11) → transparant: de voorhoofdomtrek wordt 4-2-2-2-1-1.

**Voor r7a, als Jordi toch de profielkop wil (niet aangeraden):**
- A3: (17–19,14) (20,15) (21,15) (22,16) (23,17) `2` → `4`; (29,18) en (30,19) `2` → `E`.
- A2: geen frontaal oog maar een zijwaarts kijkend oog (SPRITING §11b): pupil tegen de voorrand, licht oogwit erachter, zoals Taillow.
- A1 blijft dan staan: Jordi vroeg om meer dan profiel.

## Na het eigen oordeel: NOTITIES r7
- De maker noemt r7b "3/4 zoals Taillow" en "geen open punten". Naast Taillow klopt dat niet: Taillows 3/4 zit in de brede snavel ín het gezicht, niet in een lagere snavel en een oog dat 3 px opschuift.
- "Een kop wordt pas bol als de kapnaad een boog over de bol is": de belichting is inderdaad bol geworden, maar de donkere naad zelf maakt de kop weer vlak (Taillow heeft er geen).
- Keuze oog: Starly is een goede keuze als de kop draait. Op een profielkop past het niet.

## Oordeel
- **r7a: TERUG.** FAILs: A1 (profiel, geen draai; 8–16, 10–19), A2 (frontaal oog op profielkop; 24–28, 14–18, naad in (23,17) (24,17)), A3 (kapnaad als donkere lijn; (17–19,14) (20–21,15) (22,16) (23,17) (29,18) (30,19)). Geen basis voor verder werk.
- **r7b: TERUG, de betere variant.** FAILs: B1 (draai leest niet; snavel 9–16, 12–21 op de omtrek, niet verkort, geen verre wang), B2 (kaplijn-kader rond het oog; (20–24,13) (25–26,14) (27,15) (28,16–17) (29,18) en naad (18–19,14) (17,15) (16,16)), B3 (voorhoofd (18,11)).

Lijf, vleugel, buik, poten en de 8 reparaties uit r6 zijn goed. Wat ontbreekt, zit alleen nog in de kop (zone x 8–30, y 10–22).
