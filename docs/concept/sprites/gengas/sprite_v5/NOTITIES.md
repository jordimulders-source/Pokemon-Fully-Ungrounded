# Gengas sprite v5 (15 nov) – ogen en mond niet ingedeukt, linkeroog netjes

Jordi (over v3): "ogen en mond zijn nog niet goed" · "lijkt net alsof ze indeuken" · "en linkeroog is slordig".
v5 = v4 + `v5.py` (83 pixelwijzigingen, elk met reden in `raster.txt.log`), alleen in de gezichtszone (rij 29-46, kol 8-32).
**Diff v4 → v5 buiten die zone: 0.** Grootte, plaats en vorm van de grijns blijven. Het linkeroog houdt plek en grootte (rood kol 14-17, rij 30-35).

## Wat het kuileffect gaf (gemeten in v4) en wat er veranderde
| oorzaak in v4 | v5 (zoals Gengar, `anim_front.png`) |
|---|---|
| ring van a (donker) en u (licht) direct om de ogen, deels m | om het oog één dunne lijn (K-wenkbrauw/pupil, a-lijn); daarbuiten de gewone bandtint b; de wig u blijft alleen in het midden tussen de ogen |
| lichtere m-pixels ONDER beide ogen (rij 36-37) en onder de rechtermondhoek | onderrij van het oog donkerrood (Gengar '666'), daaronder gewoon b |
| grijze bovenrij tanden (H/h) en grijze punten links/rechts | tanden wit; alleen de naden (kol 19, 23, 28, en 24 onderaan) in één lichte grijs H |
| onderlip a/u/m door elkaar, rechtsonder geen lijn | onderlip en rechterrand één tint a, linkerpunt kreeg een lijn (39,13) |
| linkeroog: rafelige zigzag van K/a/m, losse glans | Gengars linkeroog (anim_front rij 28-32, kol 19-23): donkerrode rand, lichtrode kern, pupil van 2 px, schuine bovenlijn van linksboven naar rechtsonder (spiegelt de wenkbrauw van het rechteroog); Gengar-rij 30 twee keer, zodat de modelhoogte blijft |
Ook hersteld: (44,8) was in v3 per ongeluk een lijfpixel geworden; is weer maangrijs G.

## Open punt (voorleggen, niet zelf gedaan)
- De donkere band van het model loopt dwars door het gezicht: links van het linkeroog, tussen de ogen en boven de grijns is het lijf b (donker). Die band laat ik staan, zoals het model en de opdracht vragen. Leest het daarna nog steeds als een kas, dan is de volgende stap de band vlak rond het gezicht één tint lichter maken (m). Dat verandert het model, dus eerst vragen.
