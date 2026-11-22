# Kelp-Oddish frontsprite, ronde 2 (kandidaat)

Bestanden: `oddish_r2.png` (64×64, geïndexeerd, index 0 transparant, 12 kleuren incl. transparant), `vel.png` (r2 8× | r1 8× | model op dezelfde schaal 8× / close-ups kop, kelp, hechtvoeten 12× naast het model / 1× op licht en donker + model 1×), `bouw.py`.

## Wat uit het model komt
Alles zoals r1 (zie `../r1/NOTITIES.md`): natief raster 57×60 → 33×35 met oppervlakteweging, plek en voethoogte van de Oddish uit de game (x21–53, y14–48). Figuur 33×35 px, 623 px.
Gezicht: ogen 1×2 en mondje 2×2 op de gemeten modelplek en in de modelroden.
Hechtvoetjes: kale reductie; turquoise puntjes links (linkervoet) en linksonder (rechtervoet) uit het model, met de modeltinten (selout, licht).

## Pixels die niet uit de kale reductie komen (94 px totaal; per zone: kelp 60, lijf+gezicht 20, voeten 14)
- gezicht 8 px (oppervlak-gemeten modelplek, zie r1)
- buitenlijn 59 px (lichte/open rand → zwart aan schaduwkant, groepsselout aan lichtkant)
- ontkorrelen 20 px (tintvlekjes < 3 px → buurtint)
- zebra 5 px (ladder van twee lijnen op 2 px → kortste wijkt)
- losse pixels 4 px (lichte kelppixel ingesloten door zwart → donkerste vultint; losse zwarte pixel in een vlak → buurtint)
Geen pixel is getekend; alle vormen, lijnen, schaduw en hooglicht komen uit het model.

## Wijziging t.o.v. r1
- Hooglichtdrempel 0,3 → 0,2: hooglicht op het middenblad iets groter (r1-zwak punt).
- Ingesloten lichte pixel aan de punt van het rechteronderblad → donkerste vultint.

## Metingen
- Kleurgroepen: zwart; turquoise selout/schaduw/midden/licht (L ±80/117/152/193); kelp selout/schaduw/midden/licht (L ±66/118/156/193); 2 roden. Stappen 35–52.
- Zwart 19,4 % van de figuur (Oddish uit de game 14,3 %; Gen 3 ±12–19 %): het model heeft veel zwart aan de schaduwkant en tussen de bladen.
- Geen tintvlekjes < 3 px behalve: turquoise hooglicht in de voetpuntjes (glans, uit het model) en 8 losse O1-pixels die smalle strookjes tussen twee modellijnen zijn (bladpunten, 1 vingertje rechtervoet).
- Geen lichte kleur op de buitenrand.

## Resterende twijfels (eerlijk)
- Aan de voet van de bladwaaier (x28–34, y23–28) staan de modellijnen op 1–2 px van elkaar: leest als nerven/strepen. Het model heeft daar zoveel lijnen; verder uitdunnen zou modellijnen weglaten.
- Het onderste teentje van de linkervoet (x28–30, y45–47) is op deze maat alleen zwart (model: 1–2 natieve px olijf + zwart).
- De ogen zijn 1×2 (model 2×3 natief); de Oddish uit de game heeft 1 px. Keuze voor modelmaat.
- Zwart 19 % ligt aan de bovenkant van Gen 3.
