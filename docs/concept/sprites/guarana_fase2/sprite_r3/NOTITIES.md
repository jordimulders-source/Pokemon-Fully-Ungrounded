# Guaraná fase 2, ronde 3 (verse maker): Jordi over r2 + benoemde reparaties van de coördinator

Bestanden: `guarana2_r3_A.png` (oogrand rechts/onder lijnrood) en `guarana2_r3_B.png` (oogrand rechts/onder zwart, zoals fase 1), `normal.pal` (JASC, 16),
`vel.png` (r3A | r2 | model op 8×, de drie trossen op 12× naast het natieve model, 1× op 5 achtergronden + B op 1×), `voor_jordi_r3_8x.png` (A | B op 8×, wit).
Bouwen vanuit `guarana_fase2/`:
`python3 sprite_r3/kaal.py && ZWARTRAND=1 python3 sprite_r3/bouw.py && python3 sprite_r3/bouw.py && python3 sprite_r3/controle.py && python3 sprite_r3/vel.py sprite_r3/guarana2_r3_A.png sprite_r3/vel.png sprite_r3/guarana2_r3_B.png`
(`kijk.py SPRITE x0 y0 x1 y1 out [zoom]` = uitsnede met raster naast het model op spriteschaal.)
Basis = de r2-scripts (natief raster 5,12 px, kale reductie, lijnregels), stap 1–6 ongewijzigd; nieuw: stap 7–9 en de oogstempels.

## Wat ik deed
1. **Ogen kijken linksonder** (Jordi: "kijken de ogen eigenlijk vrijwel nergens echt naar linksonder"; "soms mag je afwijken van de 4 pixel pupil").
   Zelfde plekken en maten als r2, witvorm = fase 1-oog (3-5-5-3, afgeronde hoeken). Pupil in elk oog linksonder, raakt de onderrand (overlap mag):
   groot `..OOO.. / .OwWwK. / OWWWWWK / OPPWWWK / .PPWWK. / ..KKK..` (pupil 2×2), middel `.OOOO. / OWWWwK / OPWWWK / .PPWK. / ..KK..` (pupil 3 px, L-vorm),
   klein `OWWK / OPWK` (1 px), half dicht `lid / OPPWWK / onderrand` (2 px) en `lid / OPWWK` (1 px). `w` = grijs 11 in de bovenhoeken (wit rond maken onder het lid).
   A: rand rechts/onder lijnrood (zwart alleen op de buitenrand aan de schaduwkant); B: rand rechts/onder zwart. 79 px verschil tussen A en B.
2. **Vruchten als ronde bollen** (`vruchtseg.py`, `vrucht.py`): elke vrucht uit het natieve model (samenhangend vruchtvlees L≥60 + het oogwit en de pupil erin;
   vruchten die bij het plakken half achter/half voor samensmolten gesplitst) → ellips uit de momenten (gemiddelde + covariantie) op spriteschaal, grens d²≤6,5.
   34 vruchten, getekend van achter naar voor (geplakte achtertros eerst, dan de meest bedekte). Alleen binnen het r2-trosgebied: **silhouet = r2 (alpha-diff 0)**.
   Per vrucht 1 px eigen lijn: aan de schaduwkant lijnrood 2, aan de lichtkant schaduwrood 3 (outline highlight, DC-gids). Vulling = bol met licht linksboven
   (normaal uit de ellips): schaduw 3 (sikkel rechtsonder) / midden 4 / licht 5 / glans 12 (nieuw: 248,184,148, alleen op de top van de bol). Achtertros een stap donkerder
   (14 diep rood / 3 / 4 / 5, geen glans). 13 trosgaatjes die door geen ellips gedekt worden = diep rood 14.
   De vormen komen uit de modelvruchten (positie, grootte, stand); niets met de hand getekend.
3. **Liaan, lussen, blad en ranken met volume** (`schaduw.py`): groene delen uit het natieve model (groene cellen L≥85, gescheiden door de modellijnen en de
   donkere nerven: elke getwijnde streng, lus, bladcluster en grijprank apart). Per deel: normaal uit het vervaagde deelmasker (= ronde buis), licht linksboven,
   plus 0,35 × de modelhelderheid (licht vervaagd) zodat de lichte/donkere bladhelften van het model meekomen. Ramp 7 / 13 / 8 / 9 (licht 9 = hooglicht);
   donkere delen (gemiddelde modelhelderheid < 108: strengen achter, schaduwkant) een stap donkerder: 15 (nieuw: 70,102,56) / 7 / 13 / 8.
   Waar twee strengen elkaar raken: 1 px groene binnenlijn (6) op de pixel met de meeste modellijn → de twist leest als strengen.
4. **Ruis**: groene tintvlakjes < 3 px → meest voorkomende groene vultint eromheen; in rood alleen losse pixels zonder gelijke 8-buur (kleine bollen houden hun 1–2 px-tintjes).
5. Lichte tint op de buitenrand: 0. Zwart aan de lichtkant: 0. Silhouetpixels veranderd t.o.v. r2: **0** (randen niet gladder gemaakt, zie zwakke punten).

## Kleuren (16 incl. transparant)
0 transparant · 1 zwart · rood: 2 lijn 120,28,32 · 14 diep 140,36,40 · 3 schaduw 176,56,48 · 4 midden 224,80,56 · 5 licht 240,136,104 · 12 glans 248,184,148 ·
groen: 6 lijn 58,86,46 · 15 diep 70,102,56 · 7 schaduw 84,122,64 · 13 midden 104,146,86 · 8 licht 122,160,80 · 9 hooglicht 166,198,108 · 10 oogwit · 11 oogwit-grijs.
Basistinten = fase 1 (2–11); index 12 is veranderd (r2 oranjerood 236,112,80 → glans), 14 en 15 zijn nieuw.

## Niet-model-pixels (benoemd)
- Ogen: 201 px (stempels op de r2-plekken, pupil linksonder). - Tinten: alle vulpixels van vrucht en groen zijn berekend (bol/buis + modelhelderheid), niet uit de kale
  reductie; anders dan r2: 695 px (tros L 133, M 177, R 152, rest 248), anders dan de kale reductie 1194 px. - Vruchtlijnen: positie uit de ellipsen van de modelvruchten.

## Zwakke punten die ik zelf zie
- **Nog druk naast de maatstaf** (dundragoon/skinguin hebben grote rustige vlakken): veel binnenlijnen (groene lijn 294 px, zwart 265), vooral in de stam waar de
  strengen 1–2 px breed zijn; de twist leest, maar als veel kleine stukjes.
- **Bladclusters** lezen nog niet als losse blaadjes met nerf; het is een groene massa met lichte en donkere vlekken (het model is op 64 px hier ook zo).
- **Middelste tros**: de bovenste vruchten liggen dicht op elkaar en de ogen M2/M3 (half dicht) lezen als donkere streepjes; in A zijn de ogen zachter
  (rood rondom), in B duidelijker maar donkerder.
- **Randen niet gladder gemaakt**: het silhouet is 1-op-1 r2; trapjes in de buitenrand van de trossen en de lussen zijn gebleven.
- Achtertros (14) is maar 5 px: de diepte komt vooral uit de vruchtlijnen en schaduwtinten, niet uit een duidelijk donkerdere achterlaag.

## Vraag voor Jordi
- Oogrand rechts/onder: A (lijnrood) of B (zwart)?
