# Keuring kolibrie pre-evo, kleur r6 (verse onafhankelijke keurder, 3 nov)

Gekeurd: `kolibrie_pre.png` (`normal.pal`, `raster.txt`; png = raster, 0 px verschil). Eerst zelf geoordeeld en gemeten, daarna pas `NOTITIES.md`, `kleur_r4/KEURING.md` en `kleur_r2/KEURING.md` gelezen.
Maatstaf: Taillow (`graphics/pokemon/taillow/anim_front.png`, frame 1). Vergeleken op 10×/8×, 3× en 1×, licht en donker, met Taillow, Pidgey, Natu, Swablu, Wingull, Starly, Spearow, Pidove, Fletchling, Rookidee (en Chatot, Pikipek op 1×).
Vel: `keuring_vel.png`: r6 op 10× met genummerde FAIL-zones 1–8 | Taillow 10× | reparatievoorstel 10×; daarna 3× licht en donker en 1× licht en donker (r6, voorstel, 10 referenties).
Coördinaten: (x, y), 0-geteld, zoals in `raster.txt`. Indexen: `1` bijna-zwart, `2` donker violet, `3` lijfschaduw, `4` lijf licht, `5`–`7` buik (7 wit), `8`/`9` blauwgroen, `A` poot, `B` kap/vleugel, `C`/`D` geel/oranje, `E` kap-/vleugelschaduw, `F` snavel.

## Vraag van Jordi: "is dit een sprite of een tekening, naast Taillow?"
**Een sprite, maar nog niet zo af als Taillow.** Op 3× en 1× valt r6 tussen Taillow, Pidgey en Starly niet meer uit als tekening: kop, kap, oog, bek, borst, vleugel, staart en pootjes zijn elk een omlijnde vorm, de buitenlijn is bijna-zwart met selout bovenop de kop (zoals Taillow, die daar zijn donkerblauw gebruikt), en de kop is nu een eigen vorm (koplijn `2` van de nekknik naar de inkeping in de borst). Jordi's punt "belijning voor de vorm van het hoofd" is opgelost.
Wat op 8× nog "getekend" leest, en waarom Taillow mooier is: Taillow bouwt zijn binnenvormen met **kleurclusters** (lichte veerranden op donkere veren, grijze vlekken in het wit), r6 met **1-px streeplijnen op vlakke vulling**: twee even lange, evenwijdige veerlijnen (een hark), een lichtband langs de kruin, een lichte band onder de buik die de buiklijn volgt, en twee losse streepjes op de keel. Meting: r6 heeft 139 kleurvlakken (5,3 px per vlak), de referenties 178–257 (2,8–4,1 px per vlak). Dat zijn kleine, benoembare reparaties, geen herbouw.

## Metingen (eigen scripts)
| meting | r6 | referenties |
|---|---|---|
| alpha-diff tegen `kleur_r5/raster.txt` | **0** | moet 0 |
| px / kleuren | 734 / 15 + transparant | Taillow 838/13, Pidgey 692/13, Starly 767/12 |
| aandeel zeer donker (luma < 45) | 0,195 | 0,07–0,33 (Taillow 0,27, Pidgey 0,19) |
| spreiding luma (contrast) | 73 | 52–91 (Taillow 64, Pidgey 75) |
| kleurvlakken / px per vlak | 139 / 5,3 | 128–257 / 2,8–4,1 (Natu 3,4, Taillow 4,1) |
| niet-`1` naast transparant | `2` ×12 (selout kruin/voorhoofd), `D` ×6 (gaap), `A` ×6 (pootjes) | selout en pseudo-omlijning van dunne delen (§8) toegestaan |
| losse pixels (geen 8-buur van dezelfde kleur, zonder `1`) | 8: oog (26,17) (27,17) (28,18); kin (15,19); keel (18,21) (19,21) (21,22); poot (27,42) | Taillow e.a. 23–54; hier gaat het om wát er los staat |
| 2×2-klonten zwart | 1, in het oog (27,15): bewust | – |
| omtrek rechts (stappen) | 1-1-1-1-2-…-3-3-4 gelijkmatig; nekknik y 19–21 bewust | – |
| omtrek links (borst/buik) | 1-1-1-1-2 / 2-1-1-3-2-2-1-1-2-3 | geleidelijk; inkeping (19,26–27) = kop/lijf-grens |
| evenwijdige 1-px banden | kruin `444` 3 px breed op y 10–13; onderlijf `5|2|4|3` vier diagonalen y 34–38; veerlijnen 4 en 5 px evenwijdig aan de rugrand | Taillow: geen band > 2 rijen gelijk |

## Tabel
| # | onderdeel / richtlijn | oordeel | waar / waarom |
|---|---|---|---|
| – | formaat, palet, index 0, png = raster | PASS | 64×64, 15 + 0 |
| – | silhouet ongewijzigd | PASS | alpha-diff r5: 0 |
| – | leest op 1× als vogeltje naast echte sprites | PASS | lila zittend jong met open gele bedelbek, licht én donker |
| – | 3/4 naar links-voor, licht linksboven | PASS | kop en lijf schuin; schaduw rechts |
| – | buitenlijn: zwart aan de schaduwkant, selout `2` boven op de kop | PASS | zelfde schema als Taillow (donkerblauwe kruinlijn) |
| – | kopvorm (Jordi: "belijning voor de vorm van het hoofd") | PASS | koplijn (19–22,25)→(32,21) sluit de kop af; kapnaad (18–23, y14–16) en (29–31, y18–20) |
| 1 | kruin: hooglicht | **FAIL** | `4`-band precies 3 px breed op y 10–13 (x 17–25), evenwijdig aan de selout: banding/pillow. Hooglicht hoort een vlek op de koepel te zijn |
| – | kruin/rug: schaduw `E` | PASS | breedte 1-2-2-2-2-3-3-2-1: een sikkel, geen band |
| 2 | oog | **FAIL** | gedefinieerd en helder (goed, Jordi wil dat), maar de reflectie rechtsonder (27,17) is **wit**: met de 3-px glans linksboven leest het op 8× als een ring/hol oog. §6: tegenover de glans hoort een **gekleurde** reflectie. Daaronder (28,18) een losse lichte `4` naast de ooghoek die het oog laat "lekken" |
| – | kapnaad die in het oog loopt (22–23,16) | PASS | leest als teugelstreep (vogel), geen bril |
| 8 | bek: bovensnavel | **FAIL** | vast silhouet, maar de vulling is 2 px `F` (11,12) (12,13) tussen zwart: op donker verdwijnt de bovensnavel bijna (3× donker), alleen ondersnavel en gaap blijven. Onder- en bovensnavel hebben bovendien elk een andere opbouw (onder: `D` boven/`1` onder; boven: alles zwart) |
| – | bek: gaap, korte open snavel | PASS | gele mondhoek leest op 1×; `D` naar het gat = pseudo-omlijning van een dun deel (§8), zoals r2/r4 al aanvaardden |
| 3 | keelveertjes | **FAIL** | twee losse streepjes van 2 px (18–19,21) en (21–22,22) plus (23,23): op 8× twee krasjes/traantjes, op 1× ruis. Norm 8: geen streepjes. De eindvorm heeft een blauwgroen vlak; dit moet één vlekje zijn |
| – | borst/buik, hooglicht `7` | PASS | hooglicht linksboven, `5`-schaduw wordt naar onder breder (2→6 px) |
| 5 | onderlijf/flank (rechts van de buiklijn) | **FAIL** | vier evenwijdige diagonalen `5 | 2 | 444 | 333` op y 34–38: banding. Bovendien is de `4`-band lichtlogisch fout: dit vlak ligt onder de evenaar, tussen buik en vleugel, en hoort in schaduw |
| 6 | vleugel: voorrand | **FAIL** (klein) | `4` op x 31, y 26–29 naast lijn `1` (x 30) en flank `44` (x 28–29): drie 1-px strepen `4|1|4` naast elkaar; het licht hoort alleen bij de schouder |
| 4 | vleugel: veerlijnen | **FAIL** | twee 1-px `2`-lijnen (37,32)–(40,35) en (35,34)–(39,38), zuiver 45°, bijna even lang, evenwijdig aan elkaar en aan de rugrand: een hark (norm 8). Taillow tekent veren als lichte rand van de bovenste veer op de donkere onderste, niet als krassen |
| – | vleugel/staart, staartpunt | PASS | ingeklapte vleugel over de staart; middenstreep `B` in de staart rustig |
| 7 | pootjes | **FAIL** (klein) | nabije poot (24–28, 42–43) `1F1 / 1AAA1`: op 8× een stempel/paaltje, geen tenen; naast Taillow en Starly de zwakste ledematen. Open rand `A` is pseudo-omlijning (dun deel) en op zich PASS |
| – | omlijning 1 px, geen klonten | PASS | enige klont in het oog (bewust) |
| – | jaggies / onregelmatige trapjes | PASS | snavelpunt (8–9,10) en hiel zijn echte hoeken; omtrek gelijkmatig |
| – | ruis / losse pixels | PASS behalve 2, 3 | zie F2 en F3 |
| – | contrast, aandeel donker | PASS | binnen de reeks; lichtste van de rij, maar dat is de vaste lila familie |
| – | kleurfamilie, korte bek, mus-read | vast | niet gekeurd |

## FAILs met reparatie (36 px kleur, alpha-diff 0; op het vel als voorstel getoond)
1. **Kruinhooglicht (zone 1, 6 px).** Breder bovenop, smal naar het voorhoofd: (26,10) `B`→`4`, (24,11) `B`→`4`; (21,12) `4`→`B`, (18,13) en (19,13) `4`→`B`, (17,14) `4`→`B`. Breedtes worden 4-4-2-1-1: een vlek op de koepel.
2. **Oog (zone 2, 2 px).** (27,17) `7`→`8` (gekleurde reflectie in het blauwgroen van de lijn; past bij "mysterieuzer" in de eindvorm); (28,18) `4`→`3`. Glans linksboven (25–26,15)+(25,16) en iris `E` (26,17) blijven.
3. **Keelvlek (zone 3, 7 px).** Eén vlekje in plaats van twee streepjes: (19,21) `8`→`9`, (20,21) `6`→`8`, (19,22) en (20,22) `6`→`8`, (21,22) `9`→`8`; (22,22) `8`→`6`, (23,23) `8`→`5`. Resultaat `998 / 888` op x 18–21, y 21–22.
4. **Veerlijnen (zone 4, 4 px).** Elke lijn begint met een lichte veerrand en eindigt in de schaduw: (37,32) `2`→`4`, (40,35) `2`→`E`; (35,34) en (36,35) `2`→`4`. Lijnen worden `4-2-2-E` en `4-4-2-2-2`: overlappende veren, geen hark.
5. **Flank (zone 5, 12 px).** `4`→`3` op (30–33,35), (29–31,36), (28–30,37), (27–28,38). Rij 34 (30–32) blijft `4` als bovenrand onder de schouder. Flank wordt schaduw; banden weg, meer massa onder de vleugel.
6. **Vleugelvoorrand (zone 6, 2 px).** (31,28) en (31,29) `4`→`B`; het licht blijft op (34,25) (31,26) (31,27).
7. **Poot (zone 7, 1 px).** (25,43) `A`→`F`: voorste teen vangt licht, poot leest als voet met tenen in plaats van een stempel.
8. **Bovensnavel (zone 8, 2 px).** (12,12) en (13,13) `1`→`D`: binnenrand van de bovensnavel in de gaapkleur, gespiegeld aan de ondersnavel (`D` boven, `1` onder). Leest op donker, en de twee snavelhelften horen bij elkaar.

Gemeten op het voorstel: alpha-diff 0 tegen r5 en r6; geen nieuwe open randen behalve de gaap-`D` (dun deel, al aanvaard) en de teen `F` (dun deel); geen banden meer > 2 rijen gelijk.
Na reparatie opnieuw op 3× naast Taillow en Starly kijken, op licht én donker; let vooral op het oog (de `8`-reflectie mag op 1× niet als tweede oogkleur lezen; zo wel, dan `E`).

## Na het eigen oordeel: notities en eerdere keuringen
- NOTITIES r6 zegt "Ik zie geen open punten" en noemt de witte reflectie rechtsonder bewust ("kleine tweede reflectie"). §6 vraagt een **gekleurde** reflectie; wit naast een witte glans maakt het oog hol (F2). Volgens de norm is een zelfgenoemd "geen open punten" geen bewijs; de banden (F1, F5) en de hark (F4) zijn nieuw in r6, doordat de binnenlijnen zijn toegevoegd zonder de vulling eromheen te herschikken.
- r4-keuring F5 (lange lichte vleugelrand) is in r6 grotendeels opgelost; de rest staat hier als F6. r2/r4 aanvaardden `D` als pseudo-omlijning van de gaap; ik ook.
- r2 vroeg de keelvlek als één sikkel; r6 heeft twee streepjes (F3).

## Oordeel: **TERUG**
Dicht bij goed: r6 leest als sprite en Jordi's twee punten (kopbelijning, gedefinieerd oog) zijn in de kern opgelost. Acht kleine reparaties, samen 36 px, alpha-diff 0, geen herbouw. De maker moet daarna zelf op 8× naast Taillow zoeken naar evenwijdige 1-px banden; dat is het patroon dat r6 nog "getekend" maakt.
