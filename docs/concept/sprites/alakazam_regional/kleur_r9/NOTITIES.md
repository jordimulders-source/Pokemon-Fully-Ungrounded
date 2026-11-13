# Charlatan-Alakazam: kleur r9 (linkerhand: model nagemaakt + vuistvoorstel)

Basis: `basis_r8.txt` (= `../kleur_r8/raster.txt`: links A, rechts A, pupil 1 px). Rechterhand A en pupil 1 px blijven. Bouwen en bewijzen: `python3 maak9.py`, daarna `python3 vel.py`.

Jordi: "rechterhand is wel oke, maar links is echt nog niet mooi, alle varianten niet, kan je het model niet namaken?" Over het vuistvoorstel van Claude: "je voorstel kunnen we proberne".

## L1: model nagemaakt (`onder_L1.py` → `var_L1.txt/.png`)
- Onderlaag per spritepixel uit `meet5.npz` (geometrie `../silhouet/geo.py`), zone x3–20, y34–46. Regels: `o` waar fo ≥ 0,3 of L < 60 (lijnen, schoppen); kaart (L ≥ 185) w/a; hand b (L ≥ 150), c (≥ 115), d. Silhouetrand o, aan de lichte kant van de kaart d.
- Uitzondering: de **onderarm** blijft zoals in r8. In het model is hij zwart; in de SPEC staat grijs ("onderarmen en bovenbenen wil ik sowieso niet zwart hebben").
- Technisch opgeschoond (`FIX` in `onder_L1.py`): de kaartranden aan de lichte kant d. De kaartindex (5,38) en (6,39) is w geworden, want 2 losse grijze pixels. De lijnen (15,39), (16,40), (20,39) en (19,40) zijn o. (11,43), (12,43) en (13,44) zijn d op de onderrand. Benen (x18–20, y44–46) terug naar r8.
- Vingers wijzen omlaag zoals in het model: de lijnen x10 (rij 39–42), x12–13 (rij 39–40) en x14 (rij 41–42). Het kaartwit is zichtbaar links onder de eerste vinger, op (8–9,41) en (9,42).
- Pixeldiff buiten x3–20, y34–46: 0. Alpha-diff 0.
- **Lijnkaart in de zone: 0 rood, 8 blauw** (`lijnkaart_L1.png`), steeds met de model-L:
  - schoppen (8,38) 35, (9,38) 36, (8,39) 30, (9,39) 45: het model tekent ze donker (k), niet als lijn.
  - onderarm/hand (15,38) 33, (16,39) 33, (19,40) 32: het model is daar zwart. De grijze onderarm uit de SPEC heeft een omlijning tegen de hand nodig.
  - (20,45) 136: beenomlijning uit r8, geen hand.
- Clusters < 3 px in de zone: 3. De kaartschaduw (10,37–38) a en de lijntaper (13,38) d (model L95). Verder de schaduw onder de onderarm (15–16,41) d (model L106/93).

## L2: vuist, voorstel Claude (`l2.py` → `var_L2.txt/.png`)
- Een ronde vuist van x8–19 bij rij 39–46 (model: ±x10–18 bij 38–44), op dezelfde plek. De opbouw volgt de Alakazam-lepelhand. Drie vingerbanden met licht linksboven en korte lijnen vanaf de voorrand: (9–11,41/42) en (9–11,43/44), elk met een d-taper. Het stukje kaart dat tussen de vingers door piept staat op (8,41) w.
- De kaart steekt boven (links, met schoppen) en onder uit de vuist (x11–16, rij 47–48). De vingers liggen vóór de kaart.
- Alpha-diff: **29 px erbij, 0 eraf**, allemaal onder de hand (x8–16, rij 43–49). Pixeldiff buiten x3–20, y34–49: 0.
- Lijnkaart: wijkt bewust af van het model (19 rood, 15 blauw), want dit is het voorstel en geen namaak.
- Clusters < 3 px in de zone: lijntapers (12,41) en (12,43) d, schaduw (16–17,41) d, kaartrand (12,47)/(11,48) d en (15,47)/(14,48) a.

## Niet gedaan
- **L2R2** (een vollere rechtervuist) is niet gemaakt: rechts A is door Jordi goedgekeurd ("wel oke"), en een vollere vuist maakte het niet netter.

## Zwakke punten
- L1 is zo trouw dat ook de onrust van het model meekomt: de dubbele lijn x12–13 en een vinger van 1 px op x11. Op 1× leest de hand als een grijze vlek met lijnen.
- Bij L2 is het kaarteinde onder de vuist maar 2 rijen hoog. Op 1× leest het als een wit streepje.
