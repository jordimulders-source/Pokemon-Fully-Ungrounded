# Kolibrie ronde 1: kleur-frontsprite (24 okt)

Bestanden: `kolibrie.png` (64×64, geïndexeerd, index 0 transparant), `vel.png` (3× sprite, 3× silhouet v6, 1× op vier achtergronden, 1× naast Venomoth, Ho-Oh, Fearow, Articuno, Talonflame en Ninjask), `teken.py` (het tekst-raster: elke pixel is met de hand getypt; het script zet alleen die pixels), `check.py` (pixeldiff tegen het silhouet), `vel.py`.

## Palet (14 kleuren + transparant; slot 15 is reserve)
| idx | teken | kleur | gebruik |
|---|---|---|---|
| 0 | `.` | 152 208 160 | transparant |
| 1 | K | 20 10 30 | omlijning aan de schaduwkant (violetzwart, geen puur zwart) |
| 2–4 | k h H | fluweel donker/basis/hooglicht | kop, keel, snavel, kuif, staartslierten |
| 5–8 | v w V L | violet omlijningsbasis/schaduw/basis/hooglicht | lijf, vleugelwortel, omlijning vleugels |
| 9–10 | t T | blauwgroen | schouderglans (dekveren langs de voorrand van de nabije vleugel) |
| 11 | m | lila | vleugel halfdoorschijnend, pennenlijnen, rand van de racketpunten |
| 12–13 | p P | bleek lavendel / zeer bleek | doorschijnende vleugelpunten, kuifpuntjes, racketpunten |
| 14 | W | wit | glans in het oog, één gloedpixel per racketpunt |
| 15 | o | warm oranje | niet gebruikt (warm accent was optioneel; zonder oogt het rustiger) |

## Pixeldiff ten opzichte van silhouet v6
783 px (silhouet 782): **10 erbij, 9 eraf**, alles binnen 1 px van de omtrek:
- Kuif: bovenste punt van het eerste veertje 1 px naar rechts ((11,14)→(12,14)) en (11,15) weg: het veertje leunt nu iets naar achteren in plaats van recht omhoog (afgekeurd: "recht omhoog leest als oren").
- Voorhoofd: (6,22), (5,24), (5,30) weg, (4,26), (4,27) erbij: de 7 px rechte verticale voorkant wordt een curve 1-1-2-2-2.
- Buik: rij 38 x25–31 erbij (de gaten in de buiklijn), (20,38), (21,38), (34–36,38) eraf: één gladde bolle onderlijn in plaats van twee bobbels.

## §0-checklist (SPRITING.md)
1. Lijf en blik 3/4 naar links-voor: ok, volgt het silhouet (kop links, snavel schuin linksonder, verre vleugel smal en hoger, nabije groter).
2. Alle delen geteld en verbonden: ok. Snavel, kop, kuif (3 veren), 2 vleugels, lijf, staartfranje, 3 slierten met elk een racketpunt. Pootjes ingetrokken (zoals bij een zwevende kolibrie); niets zweeft los.
3. Geen rechte lijnen waar hij rond is: voorhoofd afgerond (zie diff); buiklijn bol gemaakt. Rest: de vleugels zijn echte rechte veren (mag).
4. Ogen geïntegreerd: ok. Klein (2×3): donker bovenlid, iris met één witte glanspixel linksboven, lichtere violette reflectie eronder. Geen tweede oog (vogelkop in 3/4 met lange snavel: één oog). Een bleek vlekje achter het oog (zoals op de foto) las op 1× als een tweede oog en is weggehaald.
5. Silhouet leest als kolibrie: ok (bevroren silhouet; lange dunne snavel, V-vleugels, slierten).
6. Formaat: 783 px, box 56×54. Silhouet is bevroren; zie "Wat nog niet klopt".
7. Pose niet stijf: ok, drinkende zweefpose uit de foto.

## Harde eisen SPRITE_NORM
1. Leest op 1× als Pokémon: ok naast Venomoth/Fearow/Articuno op het vel; vooral als vogel-Ghost door het fluweelpalet en de bleke punten.
2. 3/4 links-voor: ok (zie §0.1).
3. Ledematen: n.v.t. als viervoeter; vleugels en staart vast aan het lijf, geen gat tussen vleugel en lijf (vleugelwortel ligt over de rug).
4. Geen Escher: nabije vleugel ligt over de verre (de voorrand van de nabije vleugel is over de wortel van de verre getekend); slierten: racket A ligt rechts naast sliert 2, racket B onder sliert 2 en rechts van sliert 3, racket C aan het eind van sliert 3; overal gescheiden door donker/bleek.
5. Lijf over een echt skelet: het silhouet komt uit Jordi's foto (bevroren); geen doosvormen.
6. Kop: klein, bovenhoofd plat (Ho-Oh/Fearow-stijl), geen ronde bol.
7. Ogen: ok (zie §0.4).
8. Kenmerken op 1×: snavel, kuifpuntjes, vleugelpunten en de drie racketpunten lezen op 1×. **Schubben bewust weggelaten:** een proef met 5 schubboogjes las op 1× als ruis (Making Fake Pokémon: "schubben zijn groot genoeg of er zijn geen schubben"). Het iriserende lijf zit nu in harde vlakken: lichte vlek aan nek en flank, schaduw onderaan.
9. Omlijning: per kleurgroep. Kop: bovenkant en voorkant `k`, de rest `K`. Lijf: rug `v`, buik `K`. Vleugels: voorrand `v`, achterrand bij de wortel `K`, punten `w` (lichter, zodat de punt doorschijnend oogt). Racketpunten: rand `m`. Geen open randen; geen antialiasing aan de buitenkant.
10. Geen Chernobyl: geen crème vlakken, geen losse delen.

## Dragonfly Cave-regels (SPRITING §1–§8)
- §1 Gereedschap: geen vormfuncties; elke pixel getypt in `teken.py`. Het script zet alleen de pixels.
- §2 Per onderdeel: volgorde vleugels → kuif/kop → lijf → staart; elk onderdeel apart bekeken op 8×.
- §3 Lijnen/curven: voorhoofd 1-1-2-2-2; buik bolle lijn; vleugelranden regelmatige trap (rechte veren); kuifveertjes als 1-px pseudo-omlijning.
- §4 Palet: per kleurgroep 3 tinten + omlijningstint (fluweel k/h/H + K; violet w/V/L + v; blauwgroen t/T); vleugeltinten m/p/P. Geen verlopen buiten die stappen.
- §5 Licht linksboven: hooglicht op kruin, nek en bovenkant van het achterlijf; schaduw op keel en buik; slagschaduw `w` op het lijf onder de vleugelwortel.
- §6 Glans en ogen: één witte glanspixel in het oog, lichtere reflectie eronder; glans alleen in de racketpunten (W) als zielelicht.
- §7 Texturen: veren glad; schubben weggelaten (zie eis 8).
- §8 Omlijning: zwart alleen aan de schaduwkant (buik, achterrand vleugelwortel, onderzijde slierten); belichte randen in de omlijningsbasis (`v`, `k`), vleugelpunten nog lichter (`w`). 1 px breed, geen klonten.
- Venomoth-effect: vleugel dekkend aan de wortel (`w` + blauwgroene dekveren), dan `m`, dan `p`/`P` met `m`-pennenlijnen, punt `P` met lichte rand. Bij de verre vleugel hetzelfde in donkerder stappen.

## Wat nog niet klopt (eerlijk)
- **Grootte (silhouetniveau, niet door mij te repareren):** 783 px is klein voor een eindvorm; Fearow, Articuno en Ho-Oh zijn twee keer zo massief. Het lijf is dun omdat het silhouet zo is goedgekeurd. Geen fout in deze sprite, maar Claude/Jordi moeten het weten vóór de ROM.
- **Donkere achtergrond:** op een heel donkere achtergrond (vel, derde vakje) valt de fluweelzwarte kop weg tegen de achtergrond; dat hoort bij "fluweelzwart" (zelfde als Murkrow/Honchkrow). Op lichte en middentoon-achtergronden (zoals in gevechten) leest hij goed.
- Verder geen punten die ik zwak vind. De dingen die ik onderweg zwak vond, zijn gerepareerd: schubben als ruis (weg), bleek vlekje achter het oog dat als tweede oog las (weg), blauwgroen als blok (smalle strook langs de voorrand), vleugel die te weinig doorschijnend oogde (sneller naar bleek, pennenlijnen), rechte buiklijn met bobbels (glad), kuifveertje recht omhoog (leunt nu naar achteren).

## Lessen
- Een bleke vlek naast een klein oog leest op 1× als een tweede oog; bij een donkere kop alleen de glanspixel gebruiken.
- Schubben op een lijf van 6–8 px hoog lezen niet; iriserend = twee harde tinten (Beautifly), geen patroon.
- Doorschijnende vleugels op een smal blad: de stap van dekkend naar bleek moet al rond het midden beginnen, anders oogt het als een gewone lila vleugel. Een lichtere omlijning aan de punt helpt.
- Blauwgroen als dekverenstrook langs de voorrand scheidt de vleugelwortel van het violette lijf; zonder die strook smelten wortel en lijf samen.
- Overlappende slierten en racketpunten in een bevroren silhouet: scheid ze met waarde (donkere sliert, bleke punt), niet met extra omlijning.
