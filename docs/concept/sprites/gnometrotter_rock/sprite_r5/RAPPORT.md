# Gnometrotter Rock: sprite r5 ("netjes maken", 23 nov)

Basis: `sprite_r4/gnometrotter_rock.png`. Jordi: "ik vind ze alle 5 heel slordig. de gesp is nergens goed gelukt, rock heeft willekeurige pixels in de hoed, het lijnenwerk is slordig, nergens is het kleurgebruik/schaduwgebruik met tinten perfect gelukt" · "het silhouet is prima" · "je mag de gesp trouwens bij rock en ijs weglaten" · "kijk vooral ook naar andere pokemon" · "kijk vooral hoe je de vorm kan creëren zonder de kleur te veranderen van het roze en blauw".

Leveringen: `gnometrotter_rock.png` (64×64, P, zelfde palet als r4, index 0 transparant), `gnometrotter_rock_8x.png`, `vel.png` (r5 | r4 | Gnomad op 8×, eronder 1× en 2×).

## Controles (script)
- **Silhouet: alpha-diff 0 met r4.** Palet byte-gelijk aan r4 (15 kleuren gebruikt).
- Losse-pixelscan (8-buren, per index): 1 over, (15,14) = bewust hooglicht op het bovenste haarplukje links.
- Om-en-om-randscan (buitenlijn: zwart tussen lijnkleur of lijnkleur tussen zwart): 0.
- Zwart 12,6 % (r4 9,7 %, Gnomad 12,2 %); zwart staat aan de schaduwkant van de buitenlijn, rond de riem (zoals Gnomad), als boog linksonder rond neus en vuist (Popplio-regel), en onder de vuist/stok.
- Tinten per groep: steen 3/4/5 + lijn 2; licht steen (baard/haar) e/d/c + lijn 4; roze f/8/7 + lijn 6; blauw b/a + lijn 9.

## Afwijking t.o.v. r4 per onderdeel (pixels)
muts+rugkam 127 · haar L 12 · haar R 23 · baard 96 · neus 7 · lijf 125 · arm L+vuist 21 · arm R 6 · hand R 12 · riem (+gesp) 141 · stok 29 · broek 101 · zool L 16 · zool R 17. Totaal 733.

## Per onderdeel
- **Muts:** alle losse pixels weg (de 2-pixels midden in het vlak, de 3-pixels in de omlijning). Nu: hooglicht 5 als één blob linksboven (rij 2–10), 4 als hoofdvlak, 3 als sikkel rechts; lichtrand van 4 binnen de omlijning links (zoals Gnomad). Alleen de modellijnen in 2: de vouw tussen voorkant en punt ((35,6)→(36,9)) en de onderrand van de overslaande voorkant ((36,9)→(27,12), taps). Rand eronder als lichte band (5 links → 3 rechts), oogstrook dicht met 3 (Jordi "1 akkoord"), onderrand in 2. Punt rechts in 3, scheidingslijn 2 naar de stenen rugplaat; rugplaat met licht vlak 5 links, 4, 3, en het kleine facet (48–49, 19–20) uit het model. Gat: zwart aan de schaduwkant, 2 aan de lichtkant.
- **Haar L / haar R:** plukken in e/d/c met lijn 4; bovenrand 4, onderkant van haar L zwart (buitenrand), onderkant van haar R in 4 (binnenlijn tegen het lijf, zoals de snor van Gnomad).
- **Neus:** schone cirkel: 6 bovenom en rechts, zwarte boog van linksmidden via linksonder tot ondermidden, hooglicht f linksboven (5 px), sikkel 7 rechtsonder.
- **Baard:** e/d/c met lijn 4; de V-lijn uit het model (vanaf (20,24) naar rechtsonder, doorlopend als de streng op x27 tot rij 32) en de korte linkertak naar het schouderplukje; schaduwband c rechts (x28–29), donkere strengen linksonder en het puntvormige donkere stuk onder midden als c-vlakken (geen extra lijnen), lichtstreep e uit het model. Rechterrand recht op x30 zoals het model (lijf schuift daar 1 px op). Linkerrand tegen arm/lijf in 4 i.p.v. zwart.
- **Lijf (alleen roze 6/7/8/f, geen grijs):** stenen platen uit het model als vlakken met 6-lijnen: bovenplaat onder de oogstrook, donkere plaat naast de baard, plaat onder haar R (7, in de schaduw), grote borstplaat met hooglicht f linksboven en sikkel 7 rechts, lichte plaat linksonder (f-hooglicht), plaat rechtsonder (7) en onderplaat. Schouderovaal: bovenvlak 8 met f, onderrand-lijn 6, rand 7 eronder, boog linksonder in 6.
- **Gesp: weggelaten** (Jordi). Riem doorlopend: zwarte boven- en onderlijn (zoals Gnomad/Machoke), lichte bovenrand 5 → 4 → 3 en vulling 4 → 3 → 2 van links naar rechts (volume, rechterflank in de schaduw). Bovenlijn op één hoogte onder de baard (rij 37); de baard eindigt daarboven in c.
- **Vuist + arm L:** twee lobben gescheiden door 6, hooglicht f linksboven, 7 rechtsonder, zwarte boog linksonder; arm: bovenrij 8, onderrij 7, 6 boven, zwart onder.
- **Stok:** per rij 2 | 5 | 4 | 3 | 1 (licht links, schaduw rechts), bovenkant breder onder de vuist; alle losse pixels weg.
- **Arm R / hand R:** ovaal met f-hooglicht (3 px), 7 linksonder; bal met f-hooglicht bovenin, 7 onderin, 6 boven, zwart rechts en onder. De 1-px duimplooi is weggelaten (las als losse lijnpixel).
- **Broek (alleen blauw):** linkerdij met naadje uit het model (9) en b-hooglicht linksboven; kruis met middennaad (9); rechterdij met b-hooglicht als blob linksboven, binnenrand 9; voetballen met b-hooglicht en 9 als voet/scheen-lijn. Losse 9-pixels onder de riem weg; linkerbuitenrand volledig 9 (geen zwart/9 om en om meer).
- **Zolen:** bovenvlak 5 → 4, zijband 3, zwarte onderrand; rechts de rand rond de voet 5 (licht) en 4.

## Werkwijze
Model overnemen, niet hertekenen: vorm, plaats en lijnen per onderdeel van het model op dezelfde geometrie (`sprite/kijk.py`), r4 als onderlaag; alleen binnen het bevroren silhouet de tinten en lijnen per pixel opnieuw gezet. Steen bestudeerd aan Regirock (platen: lichte rand linksboven, donkere breuklijnen, schaduw rechtsonder); Graveler is te korrelig als voorbeeld.

## Eigen kanttekeningen
- De riem is op de rechterflank (stijgend deel) een diagonale streep zwart/3/2/zwart; netjes maar donker.
- Het lijf heeft meer platen/lijnen dan Gnomad; dat is het steenontwerp (vorm via lijnen en tinten binnen roze).
- Zwart 12,6 %, iets boven Gnomad.
