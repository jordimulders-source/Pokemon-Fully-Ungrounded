# Hoatzin fase 2, ontwerp 2, s9 (20 nov): kleur en lijn op s8

Jordi: "de vorm van de poten is beter, het gaat erop vooruit, maar nog steeds te blurry, snavel heeft nu wel opeens dezelfde kleur als de nek" · "buik mag ook de zwarte lijn omheen zachter worden".
`sh alles.sh` (bouw9.py op s8 + `../s7/groep.npy`). Silhouet = s8 (0 px anders), oogpixels gelijk; 336 px anders dan s8.

- **Snavel/poten eigen neutraal grijs:** 6 (184,184,180) licht, 15 (128,128,126) midden, 4 donker. Crème deelt niets meer met grijs: 5 licht, 7 (178,164,136) schaduw. De crème-middentint is vervallen.
- **Vrije paletplek:** gezichtsblauw = de lichtste vleugeltint 2, die daarvoor lichter en iets blauwer is gemaakt: (110,132,194).
- **Waardebereik:** 4 bijna zwart navy (34,32,58).
- **Zwarte buitenlijn rondom:** een randpixel wordt zwart als het onderdeel erachter nog ≥ 2 px kleur houdt. Dunne plukken, tenen en het oog houden hun kleur. De poten houden de omlijning van s8 (pootvorm ligt bij Jordi).
- **Krop/buik zachter:** geen zwarte lijn, maar de donkerste kroptint aan de buitenrand en tegen lijf en nek. Binnen is de krop een tint lichter, anders wordt het een blok.
- **Sikkels:** lijf (licht ≤ 3 px van linksboven, schaduw 2 px rechtsonder), nabije vleugel (lichte voor-/bovenrand ≤ 2 px), nek (schaduw rechtsonder en direct onder de kop).
- **Klein:** (40,40) en (41,40) zijn 3.

Controle: dambord 0 · om-en-om 0 · klonten 0 · barcode 0. `naast.png` (1×/2×) en `zes.png` (6×, naast Honchkrow en pitahaya fase 3).

## Eerlijk
- Rafelige trapjes in de contour (punt 2e) zijn niet glad te maken zonder de vorm te veranderen. Met de zwarte lijn vallen ze wel minder op.
- De nek heeft 2 tinten met weinig schaduw.
- De nabije vleugel heeft nu een lichtblauwe voorrand: helderder dan het model.
