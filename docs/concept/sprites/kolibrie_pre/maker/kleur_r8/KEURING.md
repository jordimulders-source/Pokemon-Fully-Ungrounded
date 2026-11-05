# Keuring kolibrie pre-evo, kleur r8 (onafhankelijke keurder, 3 nov)

## Wat gekeurd is
| stand | bestand | raster |
|---|---|---|
| kapgrens zoals r7b | `kolibrie_pre.png` | `raster.txt` |
| kapgrens hoger | `kolibrie_pre_hoger.png` | `raster_hoger.txt` |
| kapgrens lager | `kolibrie_pre_lager.png` | `raster_lager.txt` |

- **png = raster:** ja, voor alle drie. Elk 734 px.
- **Palet:** 8 en 9 zijn nu mondroze (236,120,146) en donkerrood (150,40,84). Het blauwgroen is weg.
- Eerst zelf geoordeeld, daarna `NOTITIES.md` gelezen.

**Jordi, letterlijk:**
- "r7b is de beste, maar waarom hangt er opeens een blauw achtig puntje onderin het hoofd?"
- "de snavel is nog niet helemaal goed aan de binnenkant overigens"
- "dat vlekje ziet er niet uit"
- "het starly oog is prima, plus dat de kleur boven het oog nog verandert. Alleen misschien nog net iets hoger boven het oog doen? Of juist net iets lager, de plek van het oog is vooral goed in r7b"

**Vel `keuring_vel.png`:**
1. r8 op 8× met zones C1–C3, Taillow op 8× en foto 3 (het open bekje uitgesneden);
2. de koppen op 14×: r7b, r8, Taillow en Pelipper (een echte open bek in Gen 3);
3. de drie kapgrenzen op 12×;
4. 3× en 1× op licht en donker: r7b, r8, hoger, lager, Taillow, Starly, Pelipper en Pidgey.

Coördinaten: (x, y), 0-geteld.

## Claude's twijfel: snavel of doosje?
**Het leest als een doosje of vierkante mond, niet als snavel.** Dat geldt op 14× en op 3×. Op 1× zie je vooral een roze open mond.

**Oorzaken (gemeten):**
- **Twee rechte, evenwijdige zwarte lijnen van 6 px:** rij 13 (x 11–16, `111122`) en rij 21 (x 11–16, `111111`). Dat zijn de boven- en onderkant van de bek, en ze vormen de boven- en onderrand van een rechthoek.
- **Bek-helften als horizontale balken:** beide helften zijn even dik en horizontaal, met een stompe, vierkante punt (bovensnavel 5 px `1/F/D`, ondersnavel 4 px `D/F/1`). Ze lopen niet uit elkaar.
- **De opening is een rechthoek van gelijke hoogte:** 3 rijen, y 16–18, op x 13–15, aan de voorkant afgesloten door donkerrood `9` (14,16) (13,17) (13,18). De mond is daardoor een gat met een donkere lijst eromheen.

**Hoe een echte open bek eruitziet:**
- **Foto 3:** een **V-wig**. De twee helften lopen vanaf de mondhoek uit elkaar en eindigen in punten. Langs beide binnenranden zit een gele flens, en binnenin is het geel-oranje.
- **Pelipper:** een lange open bek met de mondlijn en het rood als smalle wig naar de mondhoek.
- **Taillow:** een gesloten bek, kort en breed, maar wel spits naar de punt.

In r8 is de spitsheid verdwenen. Daarmee is het een mond geworden.

## Nagelopen uit r7
| r7 | r8 | oordeel |
|---|---|---|
| B1 draai | Snavel kort en in het gezicht, geen verre wang. De kop leest nu naast Taillow wel meer naar de kijker gedraaid: het frontale Starly-oog en de korte bek passen bij elkaar. Ik neem het argument van de maker aan dat een verre wang als doosje las | **PASS** voor de kop. De snavel zelf: C1 |
| B2 kaplijn-kader | De donkere koepel is weg; kap en gezicht zijn gescheiden door kleur | **PASS** |
| B3 voorhoofd | (18,11) en (16,12) zijn weg | **FAIL in een nieuwe vorm** (C3): de omtrek loopt nu als trap 23-21-19-17-15 (stappen 2-2-2-2). Dat leest als een rechte schuine lijn (§3), en die gaat met een hoek over in de rechte bovenrand van de snavel (rij 13) |
| r6 1–8 | lijf, vleugel, buik en poten zijn ongewijzigd ten opzichte van r7b | **PASS** |
| Jordi: blauwgroen puntje, "vlekje" | weg; de keel (21–22, 21–22) is `6`/`5` | **PASS** |
| Jordi: oog | Starly-oog en plek uit r7b, 0 px anders | **PASS** |

## Tabel r8
| # | onderdeel | oordeel | waar / waarom |
|---|---|---|---|
| – | formaat, palet, lijf ongewijzigd | PASS | |
| – | oog | PASS | gedefinieerd, staat vrij in het gezicht, geen bril meer |
| – | kop: draai naast Taillow | PASS | korte bek in het gezicht en frontaal oog: de kop kijkt naar je toe |
| – | kopvolume | PASS | hooglichtvlek, schaduwsikkels, kleurgrens kap/gezicht |
| – | keel | PASS | geen vlekje meer |
| – | open randen | PASS | `9` (14,16) (13,17) (13,18) en teen `F` (25,43) zijn dunne delen. Zie wel C2 voor `9` |
| C1 | **snavel: vorm** | **FAIL** | doosje/vierkante mond (zie boven), zone x 10–17, y 12–21 |
| C2 | **snavel: binnenkant** | **FAIL** | Roze en donkerrood lezen als tong of mensenmond, terwijl foto 3 geel-oranje heeft. Het donkerste `9` zit aan de voorkant van de opening in plaats van diep in de keel bij de mondhoek: een donkere lijst, geen diepte |
| C3 | **voorhoofd en snavelbasis** | **FAIL** | Omtrek in gelijke stappen (23,9)→(15,13) = een rechte lijn, met daarna zonder inkeping de rechte bovenrand van de snavel: de voorkant van de kop wordt hoekig |

## Reparaties
**C1 + C2: de snavel als V-wig.** Kort houden (≤ 5 px), met de basis in het gezicht (x 15–16) zoals nu. Zone x 9–17, y 12–21; de omtrek mag hier veranderen.
- **Bovensnavel loopt schuin omhoog naar de punt:**
  - basis op (15,14), punt op (10–11,12);
  - 2 px dik bij de basis, 1 px bij de punt;
  - bovenrand `1`, vulling `F`, aan de gaapkant een gele flens `C`/`D`.
- **Ondersnavel loopt schuin omlaag naar de punt:**
  - basis op (16,19), punt op (11,21);
  - gele flens aan de bovenkant, `F`, onderrand `1`.
- **De opening wordt een wig:**
  - vooraan open lucht tussen de punten (zoals r6/r7b: x 10–12 transparant tussen de helften);
  - achteraan de mondbinnenkant in een driehoek van 2–3 px bij de mondhoek (x 14–15, y 16–18), donkerst (`9`) diep bij de mondhoek (15,17).
- **Palet 8/9 naar foto 3:**
  - 8 naar geel-oranje, bijvoorbeeld (244,168,64);
  - 9 naar een donker oranjebruin keelgat, bijvoorbeeld (150,70,40);
  - of de bestaande `D` voor de binnenkant gebruiken en alleen 9 als keel.
- **Niet terug** naar de lange, steile spies van r6/r7b: die las als profiel.

**C3: voorhoofd als koepel met een inkeping bij de bekbasis.**
- (17,12) → transparant; (15,13) en (16,13) → transparant.
- (17,13) wordt de selout `2`; de bekbasis begint daaronder op (15,14).
- Looplengtes 4-2-2-1-1: een koepel. Het inkepinkje tussen voorhoofd en bovensnavel laat de bek *voor* het gezicht zitten, zoals bij Taillow.

## Kapgrens (Jordi kiest)
| stand | hoe hij leest |
|---|---|
| **hoger** | De kap stopt boven het oog. Boven en rechtsboven komt een lichte rand rond het oog ((25–26,13–14) `4`). Dat begint weer als oogkas of bril te lezen. Niet aangeraden. |
| **zoals r7b** | **Voorkeur.** Het bovenlid ligt tegen de kap, het gezicht is licht links en onder het oog. Dit is precies "de kleur boven het oog verandert", wat Jordi goed vond. Op 1× het helderst. |
| **lager** | De kap loopt over het voorhoofd tot aan het lid ((16–21,14) (17–18,15) `B`). Het oog verliest zijn bovenrand in de donkere kap en de kop wordt zwaarder. Tweede keus. |

## Na het eigen oordeel: NOTITIES r8
- **Verre wang:** de maker zag die als doosje lezen en liet hem weg. Akkoord; de draai leest nu zonder.
- **"Open bek leest als twee snavelhelften met gele rand en roze keel":** op 8× ja, maar als twee evenwijdige balken. Op 3× en 1× leest het als een vierkante roze mond. De les van de maker zelf, "een open bek blijft open aan de voorkant", is maar half toegepast: de voorkant is wel open, maar de helften lopen niet uit elkaar.

## Oordeel: **TERUG**
- **C1, snavel als doosje:** rechte zwarte lijnen (11–16,13) en (11–16,21), stompe evenwijdige helften, rechthoekige opening (13–15, 16–18). Repareren als V-wig.
- **C2, binnenkant:** roze/donkerrood in plaats van geel-oranje (foto 3), en `9` vooraan op (14,16) (13,17) (13,18) in plaats van diep bij de mondhoek (15,17).
- **C3, voorhoofd:** rechte trap (23,9)→(15,13) die hoekig overgaat in de snavel. Repareren met (17,12), (15,13) en (16,13) → transparant.

Kop, draai, oog, kapgrens (zoals r7b), keel en lijf zijn goed.
