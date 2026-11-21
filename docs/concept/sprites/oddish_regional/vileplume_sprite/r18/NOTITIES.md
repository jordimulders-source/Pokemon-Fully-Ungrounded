# Vileplume r18 (maker-agent): alleen de poten (y42-62)
Jordi: "kan je niet pixel voor pixel net model nadoen?", pootkleur "tussen deze 2 in", op r17 "nee doe even beter je best", "het moet consistent zijn".

## Werkwijze (`bouw.py`, draaien vanuit `vileplume_sprite/`)
- Rest = r17 pixel voor pixel (assert op y0-41 en y63); 79 px anders, allemaal in y42-62.
- Per spriterij: natieve modelrijen (cellen per 2) die de rij raken, gewogen op overlap. Pad = gewogen midden van de poot; 3 px breed, eerste x = round(midden - 1,5).
- Opbouw per rij [linkerrand | licht | rechterrand], tinten van de dominante modelrij (meeste overlap), dichtstbijzijnde paletkleur (RGB): 1 zwart, 6 (44,64,68), 7 (124,154,155), 8 (162,191,191), 9 (194,216,214), 10 (232,243,235). Bij 4 modelcellen (rand, licht, half licht, rand) wint het lichtste voor het midden.
- Volledige tabel per rij (model v, modelranden, modeltinten → spritepixels): `uitvoer.txt`.

## Per rij (natieve tinten → sprite)
Linkerpoot (x23-27):
- y42 v124 [157,172,174,32] → [7,8,1] x25-27 (aanzet onder het lijf)
- y43-44 v126/128 [145,242,243,(196),24] → [7,10,1] x24-26
- y45-46 v130/132 [145-151,238-241,34-47] → [7,10,6] x23-25 (knie naar links, zoals model)
- y47-48 v136/138 [58,205,51] → [6,9,6] x23-25
- y49-51 v140-144 [137-146,205,50-53] → [7,9,6] x24-26 (grijze knieband links)
- y52-55 v146-154 [61-68,206,(166-174),24-29] → [6,9,1] x24-26
- y56-58 v156-162 [52-58,176-182,24-26] → [6,8,1] x24-26
- y59 v164 [19,20] → voet [1,1] x25-26
Rechterpoot (x33-40):
- y42-43 v124/126 [27-30,177-183,31-32] → [1,8,8,8,1] x33-37 (aanzet 4,3-4,5 px breed in het model, sluit aan op y41)
- y44 v128 [42,181,181,30] → [6,8,8,1] x34-37
- y45-48 v130-138 [38-62,237-240,(120-159)/73-76] → [6,10,6] x35-37
- y49 v140 [110,223,76] → [7,10,6] x36-38
- y50-52 v142-146 [101-146,214-219,71-72] → [7,9,6] x36-38 (grijze knieband links, zelfde hoogte als links)
- y53-58 v150-162 [64-76,205-210,42-48] → [6,9,6] x37-39
- y59 v162/164 → [6,9,6] x38-40
- y60-61 v166/168 [73,189-194,14-18] → [6,8,1] x38-40
- y62 v170 [12,17] → voet [1,1] x39-40

## Afwijkingen van de kale meting (4)
- Rechterpoot y45-46 rechterrand: model 120/159 (→7) wordt 6: lichte pixels op de schaduwkant, los van de rest.
- Linkerpoot y42 rechterrand: model 32 (→6 in RGB) wordt 1: anders één losse 6 boven de zwarte y43-44.
- Rechterpoot y45 op x35-37 i.p.v. x34-36 (midden 35,82): anders inkeping rechts (x37→36→37).
- Rechterpoot y59: model is daar een smalle enkel ([155,47]); zelfde opbouw [6,9,6] als de rijen erboven.

## Consistentie
- Beide poten: rechterrand zwart bij de aanzet (y42-44), donker blauwgrijs in het midden, zwart onderaan (links vanaf y52, rechts vanaf y60, zoals het model); midden 8 → 10 (hooglicht boven) → 9 → 8 vlak boven de voet; grijze knieband op de linkerrand op dezelfde hoogte (y49-51/52). Overgangen zijn blokjes van ≥2 rijen; pad verspringt steeds 1 px.
- Wat het model níet consistent heeft en zo blijft: de linkerpoot is bovenaan links grijs (licht van linksboven), de rechterpoot bovenaan donker (schaduw onder het lijf); de linkerpoot heeft onderaan langer een zwarte rechterrand.
