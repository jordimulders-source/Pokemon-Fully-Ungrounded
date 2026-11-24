# r6 checklist (zelftoets maker)
Bron vorm: Gemini r5 ("hier wel de juiste vorm, maar niet de juiste kleuren"); kleuren van r10; benen "Zoals r5" (bruin).
Werkwijze: `r5_naar_sprite.py` telt per spritepixel het aandeel r5-crème en r5-zak (r5 gepast op de romp van r10_k8: bovenrand borststuk y480→32,
kruis y785→55, linker lijfrand x317→18,5, hand x603→43; alleen verhoudingen, niet de pose). `bouw.py` kleurt: crème ≥ 0,5 = tuinbroek,
rest van de oude broek = bruine benen uit de kale r10-reductie (`sprite_r1/basis.png`). Palet: crème 7 (248,232,200) ≈ r10 (245,229,197),
tan rand 6 (208,176,136) ≈ (206,178,137), naad F (176,138,96) ≈ (170,130,85).

| Punt | Uitslag |
|---|---|
| vorm r5: bandjes → borststuk → vierkant zakje midden → crème over buik/heupen tot het kruis, onderrand rond | ja; zak 12×7 px (x22-33, r38-44) met naad (F) erboven, tan omtrek, afgeronde onderhoeken; crème onderrand als boog tot x33-36 r53-54 (kruis) |
| bandjes over de schouders | linker x21-23 r31-33 (de rest zit achter de opgeheven arm, zoals in r5); rechter diagonaal r28-33 (x40-42 → x35-37), 3 px breed, licht links / tan rechts. Boven r28 houdt het op bij de kraagzone (diff 0). Zwak punt: bandjes lezen minder sterk dan in r5 |
| benen bruin, dijbollen zoals het model | links: dijbol (5) linksboven, schaduw (3) als sikkel rechtsonder; rechts: dijbol 5 en sikkel 3 uit de modelreductie. Tinten licht/midden/donker + lijn |
| kleurtinten en schaduw, geen effen vlak | crème: licht linksboven, sikkel (6) aan de schaduwkant rechtsonder die breder wordt, F alleen in de diepste hoek; zak lichter (7) zonder schaduw. Crème 286 / 6: 81 / F: 34 px. Licht crème 1 vlak van 284 px (8-buren) |
| geen banding | sikkel 1→4 px breed (rechts) en onderrand, geen evenwijdige banden |
| lijnen binnen het crème in de crème-ramp | naad F, zak- en bandjesrand 6; geen bruine lijnen in het crème |
| geen dubbele zoom/tailleband | tailleband r5 weg (crème loopt door tot het kruis, geen taille) |
| geen zwart/bruin om en om | linkerarm: (10,33) → zwart (bruin r27-31, zwart vanaf (9,32)); linkerbeen: selout bruin-lijn x15 r49-52, zwart vanaf (15,53), (16,54) → zwart |
| geen rechte lijnen behalve het zakje | over: bovenrand borststuk tussen de bandjes r34/35 x26-32 (7 px, lichte U, er is tussen de vachtbolletjes en de naad maar 2 rijen ruimte); verder alleen zak/naad (toegestaan) |
| rest diff 0 t.o.v. r5 | kraagzone 0, y<26 0, potlood/stam/staart/klep 0, silhouet gelijk |
| palet | 15 kleuren + transparant |

Gewijzigd t.o.v. r5: 482 px, buiten zones 0 (benen/romp 196, benen-sikkels 66, crème 110, zak 45, borst onder bolletjes 43, bandjes 12, buitenlijn 10).
