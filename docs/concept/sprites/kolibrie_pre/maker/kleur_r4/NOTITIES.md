# Kolibrie pre-evo – kleur ronde 4: afwerking tot Gen 3 (maker, 2 nov)

Jordi over r3, letterlijk: "prima, nu moet de belijning nog beter etc, moet nu echt een gen 3 sprite worden".
Ontwerp, kleuren en onderdelen van r3 zijn bevroren als ontwerp; deze ronde is alleen afwerking. Palet ongewijzigd t.o.v. r3.

## Bestanden
- `rijen_r4.txt`: met de hand, één teken per paletindex.
- `raster.txt`, `kolibrie_pre.png`, `normal.pal`.
- `vel.png`:
  - r3 en r4 op 8× met raster (lijnvergelijking);
  - r4 op 3× en 1× naast Taillow, Swablu, Wingull, Natu, Pidgey en Zigzagoon, op licht en donker.
- Scripts: `bouw.py`, `palet.py`, `controle.py`, `vel.py`.

## Studie Gen 3-afwerking (8×, indexraster van Taillow, Swablu, Pidgey; Natu, Wingull en Zigzagoon op het vel)
| aspect | wat Game Freak doet | toegepast op r4 |
|---|---|---|
| omlijning | 1 px overal. Bijna-zwart aan de schaduw- en onderkant (Taillow 16,16,16; Swablu 16,16,16). Aan de lichtkant een gekleurde donkere tint van het vlak (selout: Taillow donkerblauw boven op de kop, Pidgey donkerbruin, Swablu grijs aan de wolk). | buitenlijn overal 1 px: lichtkant (links, boven) in 2 (donker violet), schaduw- en onderkant in 1 (bijna-zwart violet). Rugrand is alleen 1, met de vleugelschaduw E ernaast. |
| binnenlijnen | lichter dan de buitenlijn: een donkere tint van het vlak zelf, niet zwart (Taillow: vleugel tegen het lijf in donkerblauw, Pidgey: veren in middenbruin) | vleugel tegen het lijf: lichte voorrand 4 met een binnenlijn 3; kapnaad via B tegen 4/5 zonder lijn; slagpen in E; keelglans en buikgrens via tinten, geen lijnen |
| curves | trapjes met een oplopend of aflopend ritme (1-1-2-2-3), geen uitschieter tussen gelijke stappen, geen dubbele pixel in een hoek | buitenlijn nagelopen; 3 px toegevoegd om twee haperingen in het ritme op te lossen (zie onder). Kruin links nu 2-2-2-1-1, nek en rug nu 2-1-1-1-1-1 en daarna halve stappen |
| shading | 3–4 tinten per groep in harde vlakken die de vorm volgen, licht linksboven, geen verloop rond de rand (geen pillow shading) | kap: hooglicht 4 als sikkel langs de linkerbovenrand, basis B, schaduw E als sikkel aan de achterkant, smal boven en onder. Buik: hooglicht 7 als ovaal linksboven op de borst, basis 6, schaduw 5 als boog rechts en onderin. Flank onder de vleugel als één hard schaduwvlak 3. Vleugel B met E aan de rugkant. |
| anti-aliasing | spaarzaam, alleen op binnenhoeken (Swablu-hals, Taillow-snavel) | alleen bij de mondhoek (D/C) en de ooglidhoekjes (2) |
| ruis | geen losse pixels in vlakken; details (veertjes) als korte groepjes | streep- en dambordpatronen uit r3 weg (vleugel "4B4E", buikstroken, flankstrepen) |

## Wat ik deed per onderdeel (diff tegen r3: 65 px)
| onderdeel | px | wat |
|---|---|---|
| borst, buik, flank | 41 | Buik als bol: hooglicht 7 als ovaal linksboven (was een lange strook), schaduw 5 als één gebogen band. De flank tussen buik en vleugel is één vlak 4, met daaronder één hard schaduwvlak 3 in plaats van strepen 5-4-3-4. |
| vleugel en rug | 13 | Slagpen als één schone diagonale lijn E zonder het 4-B-4-dambord. De vleugelrand en de rugrand zijn nu 1 px omlijning met E erbinnen. |
| kop en kap | 11 | Kaphooglicht als sikkel langs de linkerbovenrand. Kapschaduw E als sikkel die naar de nek smaller wordt (was een rechte verticale band van 3 px). De gezichtsschaduw 3 onder het achterhoofd is een gebogen vlak. |
| oog, bek, keel, pootjes, staart | 0 | Ongewijzigd: ze waren al schoon en goedgekeurd. |

## Omtrek tegen silhouet r2 (max ±20)
**3 px toegevoegd, 0 weggehaald:**
- (17,12): kruin links. Het trapje 2-2-1-2-1 wordt 2-2-2-1-1, een gelijkmatige curve.
- (34,21) en (35,22): nek naar rug. Het trapje 1-1-2-1-1 (een uitschieter halverwege) wordt 2-1-1-1-1, met de grootste stap direct na de nekknik zoals een curve hoort. De nekknik zelf blijft.

## Checks (`controle.py`, strenge versie: alles behalve 1/2 naast transparant telt, uitzonderingen A en D met reden)
- **Alpha-diff tegen silhouet r2: 3** (de 3 pixels hierboven, bewust).
- **Open randen: 0.**
- **Losse pixels:** alleen bewuste accenten (ooglidhoekjes, glans, keelveertjes, snavelpixel, licht puntje op de poot, de selout-pixel boven op de rug, hoekjes van de onderrand). Geen ruis in vlakken.
- **Rechte stukken in de buitenlijn:** alleen op de breedste plekken van bolle vormen (achterhoofd, borst), met oplopende en aflopende trapjes ervoor en erna.
- 735 px; aandeel zeer donker 0,137. 15 kleuren plus index 0, palet als r3.
- **Zelf bekeken op 8× (naast r3), op 3× en op 1×, licht en donker, naast Taillow, Swablu, Wingull, Natu, Pidgey en Zigzagoon:**
  - Omlijning, vlakverdeling en hooglicht linksboven gedragen zich als bij Taillow en Swablu.
  - Op 1× past hij ertussen: de kap, het donkere kraaloog, de gele bedelbek, de witte bolle borst en de vleugelplaat lezen als losse delen.

## Wat nog niet klopt
Ik zie geen open punten.

## Lessen
- Afwerking is vooral weglaten: strepen van vier tinten naast elkaar (5-4-3-4) en dambordjes in de vleugel lezen als ruis. Eén hard vlak per tint, dat de vorm volgt, leest als Gen 3.
- Schaduw en hooglicht als sikkel langs de rand (smal aan de uiteinden, breed in het midden) maken een bol. Een band van gelijke breedte maakt een cilinder.
- Een trapje dat 1-1-2-1-1 loopt leest als een deuk. Een omtrekpixel verplaatsen naar het begin van de curve (2-1-1-1) lost het op zonder de vorm te veranderen.
