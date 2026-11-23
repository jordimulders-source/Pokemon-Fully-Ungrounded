# Gnometrotter (Grass, hybride) – frontsprite r1 (23 nov)

Model (bevroren): `../hybride/model_hybride.png` (omtrek = r4; lijf met verticale planknerf en geribbelde benen uit de eerste versie). Lever: `gnometrotter_grass_hybride.png` (64×64 P, index 0 transparant, 16 kleuren), `gnometrotter_grass_hybride_8x.png`, `vel.png` (hybride | gewone Grass r2 | model op schaal 8×; 1× licht/donker; 1× en 2× naast Gnomad, Rock r2, Grass r2).

## Werkwijze
Exact de pijplijn en het palet van Grass r2 (`../sprite_r2/`), alleen het modelpad anders: gedeelde reductie (figuur x 3–60, y 0–59, 2056 px, gelijk aan Grass en op dezelfde voetlijn als Rock), zelfde 21 onderdelen (knoesten bestaan in de hybride niet), zelfde lijn-, volume- en DC-regels, alle r2-reparaties (neus als bal, voetballen, schouderovaal, bladmuts met alleen grote bladgrenzen).
Twee toevoegingen voor het donormateriaal (beide gemeten, niet getekend):
- **Planknerf lijf**: per kolom het aandeel modelpixels dat duidelijk donkerder is dan de omgeving (`donker.npy`); kolommen met mediaan ≥ 0,4 over het lijf en lokaal maximum worden een verticale lijn in 6: **X 29, 31, 35, 43** (de dubbele naad 29/31 staat zo in het model; de stippelrijen van het model op X 37–41 zijn te zwak en vallen weg).
- **Ribbels benen**: waar de donkere modelribbel ≥ 0,35 dekt en dwars een lokaal maximum is, schaduwtint 10 (geen lijn, geen zwart): 52 px.

## Afwijking t.o.v. de kale reductie (`tel.py`)
Totaal 1085 / 2056 (lijn 580, DC 3, vlaktint/volume/ribbels 502). Silhouet: 9 px erbij aan stok en twijg (drempel 0,35, zelfde als Grass), 0 eraf. Pixels buiten de regels: hooglichtjes 15 (neus, vuist, hand R, schouderovaal), 5 px onderdeelkaart muts→haar R/rugplank, 4 outline highlights, 2 px om-en-om (zelfde plekken als Grass).

## Controle
64×64 P, transparant 0, 16 kleuren, zwart 9,5 %, geen losse zwarte pixels; lichte kleur op de buitenrand alleen de outline highlights.

## Zwakke punten
- Het modellijf is dieper rozerood; de sprite houdt het gedeelde roze (indexen 6–8, 15 gelijk aan Rock/Grass).
- Ribbels in de benen lezen op 8× als korte streepjes 10; op 1× als lichte structuur. Wil Jordi een rustige broek (Rock-keurpunt), dan valt deze stap weg (1 regel in `maak.py`).
- Elleboog- en schouderstuk zijn in het model langwerpige geribbelde cilinders op de ronde omtrek; in de sprite blijven het ronde schijfjes met rand.
