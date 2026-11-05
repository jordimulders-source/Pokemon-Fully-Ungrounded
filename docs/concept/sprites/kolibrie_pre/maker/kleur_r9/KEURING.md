# Eindkeuring kolibrie pre-evo, kleur r9 (onafhankelijke keurder, 3 nov)

Gekeurd: `kolibrie_pre.png` = `raster.txt` (0 px verschil); 732 px; `normal.pal` (15 kleuren + 0).
Eerst zelf geoordeeld, daarna pas `NOTITIES.md` gelezen.

Jordi, letterlijk:
- "de snavel is in r8 verknald"
- "r8 lager is goed wat betreft het hoofd"
- "met het snavel bedoel ik puur dat de verbinding aan de mond wat meer een lijn moest hebben, zoals bij andere pokemon, niet dat het hele snavel anders moest"

Door Jordi vastgelegd en dus niet gekeurd: de r7b-snavel (vorm en kleur), de kop en de kapgrens van r8 lager, het Starly-oog en zijn plek. C1 en C2 uit r8 vervallen.

Vel `keuring_vel.png`:
1. r9 op 8× met zone 1, naast Taillow op 8×;
2. de snavelbasis op 24×: r9 | voorstel;
3. de koppen op 14×: r7b | r9 | Taillow | Starly;
4. 3× en 1× op licht en donker: r7b, r8 lager, r9, r9 met voorstel, Taillow, Starly, Pidgey, Natu.

Coördinaten: (x, y), 0-geteld.

## Leest de lijn bij de mondhoek zoals bij Taillow en Starly?
**Ja.** Bij Taillow en Starly scheidt een donkere lijn de snavel van de kop, en de mondhoek loopt als kort lijntje het gezicht in. In r9:
- de lijn loopt langs de snavelbasis (15,14) (15,15) (16,16) en daarna (17,17)–(17,20);
- het uiteinde van de mondlijn (18,18) staat in `2`.

**Resultaat per schaal:**
- Op 3× en 1× zit de snavel nu aan het gezicht vast in plaats van eruit te groeien. De gele gaap is aan de kant van het gezicht afgesloten.
- Op 1× is het verschil met r7b klein maar zichtbaar: een donkere snavelbasis, zoals bij Starly.

**Eén pixel is niet goed:** (15,16) staat zwart naast (15,15) en (16,16). Dat is een elleboog (drie zwarte pixels in een L) precies in deze lijn. Op 8× en 24× zie je daar een klontje waar de lijn een knik maakt. Zie FAIL 1.

## Metingen
| meting | r9 |
|---|---|
| png = raster | ja |
| alpha-diff tegen r7b | 4: (20,10) erbij; (16,12), (15,13), (14,14) weg (koepel en inkeping) |
| oog tegen r7b | 0 px |
| lijf (y ≥ 22) tegen r7b | gelijk, behalve de keel (21–22, 21–22), nu zonder blauwgroen |
| niet-`1`/`2`/`A` naast transparant | `D` van de r7b-snavel (13,14) (14,15) (14,17) (14,18) (13,19) (12,20): gaap, pseudo-omlijning; teen `F` (25,43) |
| losse pixels | (23,17) oog; (18,18) mondlijn-uiteinde (bewust); (37,32) veerrand; (27,42) en (25,43) poot. Allemaal bewust |
| ellebogen in de kop | snavelpunt (9–11, 12–13) en ondersnavelpunt (10–14, 20–21): r7b, vast. Oog (22–23, 14/17): Starly, vast. **Nieuw: (15,15)/(15,16)/(16,16)** |
| voorhoofdomtrek | 23-20-18-17-16-15: looplengtes 4-3-2-1-1-1, een koepel |
| aandeel zeer donker | 0,20 (Taillow 0,27, Pidgey 0,19) |

## Tabel (naast Taillow)
| # | onderdeel | oordeel | waarom |
|---|---|---|---|
| – | formaat, palet, index 0 | PASS | 64×64. 8/9 staan nog roze in `normal.pal`, maar worden niet gebruikt (vrij voor later) |
| – | leest op 1× als echte sprite naast Taillow, Starly, Pidgey, Natu | PASS | licht en donker |
| – | silhouet en draai (snavel r7b) | vast | leesbaarheid niet gebroken: op 1× een zittend jong met open gele bedelbek |
| – | voorhoofd (C3) | PASS | koepel met een inkeping van 1 px (14,14) boven de snavel; de snavel zit ervoor |
| – | kap, kapgrens (r8 lager) | PASS | kleurgrens, geen kader; het oog staat met zijn bovenlid in de kap |
| – | oog (Starly) | PASS | Pokémon-oog, helder op licht en donker |
| 1 | **snavelbasislijn** | **FAIL** (1 px) | Elleboog (15,15)-(15,16)-(16,16): een klontje in de lijn. De rest van de lijn (15,14)→(17,20) en de mondlijn (18,18) zijn goed |
| – | mondhoek, gaap | PASS | gele flens aan het gezicht afgesloten. De naad (16,20) `C` tegen keel (16,21) `6` valt op 1× en 3× niet op; geen fail |
| – | keel | PASS | geen vlekje meer |
| – | kopvolume | PASS | hooglichtvlek, `E`-sikkel, `3`-schaduw onder de wang, slagschaduw `5` op de borst |
| – | buik, flank, vleugel, staart, poten | PASS | gelijk aan r7b, waar r6-reparaties 1 en 3–8 al in zaten |
| – | omlijning 1 px, open randen, ruis | PASS behalve 1 | zie metingen |
| – | licht linksboven, contrast | PASS | |

## Minimale reparatie
1. **(15,16) `1` → `C`.** De lijn loopt dan diagonaal (15,15)→(16,16)→(17,17) zonder klontje. De gele flens wordt bij de mondhoek één band van boven- naar ondersnavel. Op het vel getoond (24× en 3×/1×); alpha-diff 0.

## Na het eigen oordeel: NOTITIES r9
- De maker noemt (18,18) bewust "het uiteinde iets lichter". Akkoord: dat is de mondlijn het gezicht in, zoals bij Taillow.
- De elleboog (15,16) noemt hij niet. Die pixel was in r7b de onderste omlijning van de bovensnavel; hij werd een elleboog toen (16,16) zwart werd.

## Oordeel: **TERUG**, alleen voor 1 pixel
Reparatie: (15,16) `1` → `C`. Daarna is hij **GOED** zonder nieuwe keuring: alpha-diff 0 en alleen deze pixel anders.
