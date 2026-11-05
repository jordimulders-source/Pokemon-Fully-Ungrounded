# Keuring kolibrie pre-evo, kleur r2 (onafhankelijke keurder, 2 nov)

Gekeurd: `kolibrie_pre.png` (`normal.pal`, `raster.txt`). Eerst zelf geoordeeld, daarna pas `NOTITIES.md` gelezen.
Vel: `keuring_vel.png` (8× licht met genummerde FAIL-zones en 8× donker; 2× en 1× naast de eindvorm en 11 echte sprites: Fletchling, Taillow, Natu, Pidgey, Starly, Swablu, Pichu, Togepi, Rookidee, Wingull; 3× naast eindvorm, Fletchling, Taillow, Natu, Starly; alles op licht én donker).
Coördinaten: spritecoördinaten (x, y), 0-geteld, zoals in `raster.txt`.

## Metingen (eigen script)
| meting | uitkomst |
|---|---|
| alpha-diff tegen `silhouet_r2/silhouet.txt` | **0** (732 = 732 px) |
| png = raster.txt | ja |
| kleuren | 15 + transparant (palet vol) |
| box | 38 × 37 (x 8–45, y 9–45) |
| aandeel donker (luminantie < 70) | 0,295 (refs 0,07–0,49; Taillow 0,27, Natu 0,28). In orde. |
| randpixels die geen `1` zijn naast transparant | 49, waarvan 32× `2` en 8× `A` (donkere omlijningsbasis, toegestaan) en **9 echte open randen**: geel `C`/`D` naar het gat van de bek (14,14) (13,15) (14,16) (14,17) (11,18) (12,18) (13,18) en lichtpaars `3` onderaan de buik (21,39) (24,40) |
| losse pixels (geen buur van dezelfde kleur, zonder `1`) | 52; bijna allemaal bewuste overgangen (kinlijn 5, ooglidhoekjes 2, keelglans 9, staartpunt). Geen ruis. |
| rand aan de rugkant | y 28–38: **`2 2 2 1` = 4 px donker** langs de hele rug (x 37–42) |

`NOTITIES.md` meldt "open randen: 0". Dat klopt niet: het controlescript telt geel naast het gat van de bek en `3` aan de onderrand niet mee.

## Tabel
| # | onderdeel | oordeel | waarom |
|---|---|---|---|
| – | silhouet ongewijzigd (alpha-diff 0) | PASS | 0 px verschil |
| – | palet, formaat, index 0 | PASS | 16 kleuren, transparency 0 |
| – | mild, niet mysterieus ("fletchling nog niet fire") | PASS | lila/lavendel, geen fluweelzwart; blauwgroen alleen als vlekje |
| 1 | **omlijning: gesloten** | **FAIL** | 9 open randen (zie metingen): geel en lichtpaars grenzen zonder omlijning aan transparant |
| 6 | **omlijning: 1 px, geen klonten** | **FAIL** | rugrand y 28–38 is een band van 3× `2` + `1` (4 px), parallel aan de rechte rug. Op licht leest dat als een dikke zwarte rand, juist wat §8 verbiedt |
| – | omlijning: zwart alleen aan de schaduwkant | PASS | lichtkant `2`, schaduwkant `1` |
| 4 | **licht/schaduw en volume** | **FAIL** | licht linksboven klopt, maar de buik is gearceerd in **rechte verticale banden**: de `5`-strook ligt op x 26–27 over y 26–31 en de `4`-strook op x 28–29: een cilinder, geen bolle borst. Bovendien lopen buik (7/6/5) en lijf (4/3) zonder grens in elkaar over, zodat de "lichte donzige buik" uit de SPEC niet als eigen deel leest; nergens dons (foto 5) |
| – | ruis | PASS | geen zwevende pixels; overgangen zijn bewust |
| 2 | **oog** | **FAIL** | binnenkant is maar 2 px breed (x 25–26, y 15–18) en de glans vult de hele bovenste rij (25,15)+(26,15) plus (25,16): boven is het oog wit, niet donker. Op 1× leest het als een klein wit-zwart stipje; naast Fletchling, Starly en Taillow is het oog het minst "cute" van de reeks |
| – | bek (open bedelbek) | PASS | op 1× en 3× leest de open snavel; bovensnavel donker, ondersnavel geel |
| – | gele mondhoeken | PASS (vorm) | 13 px geel leest op 1×; alleen de rand naar het gat is open (zie 1) |
| 3 | **keelvlek** | **FAIL** | 9 px blauwgroen pal onder de bekpunt (x 15–19, y 20–22), tegen de lichtkantomlijning. Op 1× en 3× leest het eerder als een kruimel/druppel uit de bek of een strikje dan als keelglans; het raakt de bek bijna |
| – | kap (geen helm) | PASS | gebogen naad door de ooglijn, licht/schaduw binnen de kap; leest als kopkleur, niet als helm |
| 5 | **vleugel** | **FAIL** | de ingeklapte vleugel (x 29–39, y 20–40) heeft dezelfde tint `3` als de flank links ervan; alleen een dun `2`-lijntje scheidt ze. Geen eigen lichte bovenrand, geen slagpenpunten. Op 1× leest het als schaduw op de rug, niet als vleugel. Taillow, Starly en Pidgey tonen de gevouwen vleugel als eigen plaat met lichte voorrand en penpunten |
| 7/8 | **pootjes** | **FAIL** | nabije poot (24–28, 42–43) leest net als streepje; verre poot (31–34, 42–43) is volledig `1`: een zwart klodderje van 6 px, leest als schaduw. Onderkant nabije poot `A` naast transparant. Hoort bij 7: twee open `3`-pixels in de buikonderrand vlak erboven |
| – | staart | PASS | stompje rechtsonder (x 37–46, y 38–45) leest op 1× als staart; terecht in schaduw (achter het lijf) |
| – | leest op 1× als jong vogeltje dat bedelt | PASS | ja, zittend jong met open gele bek |
| – | **leest op 1× als kolibrie** | **FAIL** | nee: zonder lange snavel (bewust, jong) moet de kleur het werk doen, en de enige kolibriehint (keelvlek, zie 3) leest niet als keelglans. Naast elkaar leest hij als een lila mus/zanger. Dat was ook punt 3 van Claude bij r1 |
| – | familie van de eindvorm | PASS | violet + blauwgroen accent; houding van de kop en bek lijken |
| – | **net zo "af" als Fletchling/Taillow** | **FAIL** | nee: Fletchling en Taillow hebben duidelijke delen (vleugel, poten, oog, borstvlak). Hier: gladde lila klomp met een verloop, kleine ogen, vage poten. Precies SPEC §Oorzaak 3: "een zittend vogeltje leest door details (oog, bek, vleugelrand, veren), niet door volume" |

## Reparaties per FAIL (alles binnen het bevroren silhouet, alpha-diff blijft 0)
1. **Gaap (zone x 11–15, y 14–18).** Rand naar het gat in `D` (de omlijningstint van het geel): (13,15), (14,16), (11,18), (12,18) → `D`; (14,17) blijft `D`. Het licht `C` blijft binnenin op (14,14), (14,15), (15,16), (15,17), (13,18), (14,18). ±4 px.
2. **Oog (zone x 24–28, y 14–18).** Donker boven, licht onder, en 1 kolom breder voor cute. Nu: ring `1` op x 24 en x 27, binnenkant x 25–26. Nieuw: (28,15)–(28,17) → `1` (nieuwe achterrand, was `B`), (28,14) → `2` (lidhoekje), zodat x 27 binnenkant wordt (blijft `1` = donkere iris); (26,15) → `1`; glans alleen (25,15)+(25,16) als verticaal streepje van 2 `F`; reflectie `E` onderin op (26,17), (27,17), (25,18)–(27,18). ±7 px. Daarna naast Fletchling/Starly op 1× kijken: een donker kraaloog met één glanspunt.
3. **Keelvlek (zone x 15–20, y 19–23).** Weg van de bekpunt en schuin langs de kinlijn naar achteren: (15,20), (15,21) → licht `6`/`5`; vlek als sikkel (17–21, 20–22) in `8` met 1 glanspixel `9` linksboven op (18,20). Zo zit hij op de keel, niet aan de bek. ±8 px. (Plaats is ook een vraag voor Jordi, zie onder.)
4. **Buik (zone x 19–30, y 24–38).** Grens `6`/`5` en `5`/`4` als boog laten lopen: smal bij de kin (y 24–26), naar rechts uitbollend op de borst (y 29–34, grens 1–2 px verder naar rechts), weer smaller onderin (y 36–38). Breek de rechte `5`-strook met een gekartelde grens (1-px inkepingen, om de rij) als dons, zoals §7 vacht/veren. En maak de grens buik/lijf zichtbaar: tussen `5` en `4` een korte rij `4`-pixels die het lijf om de buik heen laat lopen. ±25–35 px.
5. **Vleugel (zone x 29–39, y 20–40).** Eigen plaat: lichte voorrand in `4` direct links van/op de `2`-lijn (x 31–36, y 21–37, 1 px breed); het vleugelvlak `3`; 2–3 slagpenpunten onderaan (x 34–39, y 35–40) met elk een `2`-scheidingslijntje van 2–3 px en een `4`-pixel als randje. De flank links van de vleugel (x 28–30) een tint lichter (`4`), zodat vleugel en lijf twee delen worden. ±30 px.
6. **Rugrand (zone x 37–42, y 28–38).** Per rij de binnenste `2` → `3` (rijen 28–38: x 37/37/38/38/38/39/39/39/40/40/40). Rand wordt `2 2 1` aan de rug, `2 1` waar de vleugel de rand raakt. 11 px.
7. **Onderrand buik (21,39) en (24,40)** → `2`. 2 px.
8. **Pootjes (zone x 24–34, y 41–43).** Verre poot (31–34, 42–43): (32,42) en (32,43)–(33,43) → `A` (schaduwtint), zodat het een pootje met tenen wordt en geen klodder. Nabije poot: (25,43)–(27,43) houden `A` maar omlijn de onderkant niet extra (silhouet bevroren); maak (26,42) → `B`/`4` als licht puntje zodat hij als poot leest. ±4 px.
- **Kolibrie-lezing** volgt grotendeels uit 3 en 5: een echte keelglans en een vleugel als plaat. Komt het daarna nog steeds niet, dan is dat een vraag voor Jordi (zie onder), geen reden voor meer pixels.

Totaal ±90–110 px. Na de reparatie opnieuw: open randen = 0 met een script dat **elke** niet-omlijningskleur naast transparant telt (ook `C`, `D`, `3`), alpha-diff 0, en 1× naast Fletchling/Taillow/Starly.

## Voor Jordi (smaakkeuzes, geen fail)
- **"fluweel als kleur"**: r2 is lila en mat; van fluweel (zachte glans, diepe plooi) is weinig over. Mag de pre-evo matter zijn dan de eindvorm, of wil Jordi een zachte fluweelglans op kap en vleugel?
- **Keelvlek of nekband?** De eindvorm draagt het blauwgroen als band in de nek/schouder. De maker koos een keelvlek (kolibrie-gorget). Familie zegt nek, kolibrie zegt keel.
- **Bovensnavel**: donker grijs `A` tegen een gele ondersnavel. Echt (kolibriejongen hebben een donkere snavel), maar op 1× leest de bovenhelft als een dun zwart stokje. Lichter (grijsviolet) zou zachter/cuter ogen.
- **Kopgrootte en rechte rug** horen bij het bevroren silhouet; niet gekeurd.

## Oordeel: **TERUG**
FAILs: omlijning (open randen in de gaap en buikonderrand; 4 px dikke rugrand), volume (rechte verticale banden, geen buik/lijf-grens, geen dons), oog (glans vult de bovenkant, klein), keelvlek (leest als kruimel aan de bek), vleugel (leest als schaduw), pootjes (verre poot zwarte klodder), leest niet als kolibrie, minder "af" dan Fletchling/Taillow.
