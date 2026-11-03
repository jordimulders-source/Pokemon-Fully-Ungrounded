# Kolibrie pre-evo – kleur r1 (silhouet B2 r1, bevroren)

Bestanden: `rijen.py` (elke pixel letterlijk per rij, met de hand) → `raster.txt`; `palet.py` → `normal.pal` + `kolibrie_pre.png` (geïndexeerd, index 0 transparant); `controle.py`; `vel.py` → `vel.png`; studie: `STUDIE.md`, `studie.png`.

## Controles (`controle.py`)
- **Alpha-diff met silhouet r1: 0** (687 px).
- Open randen: geen (rand = 1/2, of 3 als lichte selout op de borst links; pseudo-omlijning F/D/A alleen op de dunne delen: snavel 2 px en pootjes).
- Losse pixels: alleen (28,18) = de lichte onderkant van het Starly-oog en (24,44) = het lichte teenpuntje; beide bewust.
- Palet: ongewijzigd `maker/kleur_r10/normal.pal` (diff 0). Gebruikt: 1–7, A–F (8 en 9, roze en donkerrood, niet nodig).

## Per onderdeel
- **Kop:** kruin licht (5/4, licht linksboven), kap B als kleurgrens die als boog van de nek naar het voorhoofd loopt (rand per rij 28-26-23-19), geen lijn; achterkant kop in E (schaduw). Buitenrand 2 bovenop/links, 1 rechts.
- **Oog:** Starly-oog pixel voor pixel uit r10 (x21–25, y14–18) op x26–30, y15–19, waar de onderlaag het oog heeft.
- **Snavel:** r7b-kleuren op het verkorte bekje: bovensnavel F met 1 (onderkant donker, bovenkant licht), ondersnavel D met de gele mondhoek C naar binnen, onderrand 1. Donkere lijn op de verbinding snavel/gezicht: 1 bij de mondhoek (y17–19), 2 erboven en eronder (taps).
- **Kin/keel:** lavendelwit 6/7 onder de snavel; de zwarte onderrand van de ondersnavel en de witte kin halen snavel en kin uit elkaar.
- **Kop over borst:** één korte lijn in de schaduwtint van het wit (5) vanuit de kin-inham (y26, x21–24) die naar rechts in de nek oploopt. Geen zwart.
- **Borst/buik:** één witte bol (6), hooglicht 7 linksboven, schaduwband 5 binnen de boog; rechtergrens als gelijkmatige boog (per rij 26-28-29-30-31-31-31-31-30-29-28-26-24); daaronder lila 3 onder de buik. Linkerrand 3 (licht) → 2 → 1 onderaan.
- **Flank/nek:** lila 4 naast de borst, 3 naar de vleugel toe.
- **Vleugel:** plaat B, licht 4 alleen op de schouder (y24–25), E aan de schaduwkant rechts. Voorrand over de flank: boven in E (zacht), onder in 2, geen zwart. Veerstreepjes en lichte randpixels na eigen controle weggehaald (lazen als stippen/ruis).
- **Staart:** E/B, omlijning 1. **Pootjes:** A met een licht teenpuntje F; verre poot donker klompje.

## Checklist §0 / Jordi over r10
1. 3/4: silhouet B2 (lijf 32°, kop 44°). ok.
2. Ledematen geteld en verbonden: ok.
3. Rechte lijnen: de borstboog en kapgrens lopen gelijkmatig; de onderbuik (y40 lila band + y41 zwarte onderrand) is wel recht.
4. Oog: Starly, ongewijzigd. ok.
5–7. Formaat 687 px, pose zittend.
- "willekeurig geplaatste zwarte strepen": binnenin staat zwart alleen in oog, snavel, de mondlijn bij de mondhoek en de onderrand van buik/poten. ok volgens de studie.
- "vorm van de buik links": de linkerrand is het bevroren silhouet; binnenin is de buik nu één boog zonder knik.
- "belijnen van de vleugel te hard": voorrand E/2, geen veerlijnen meer.

## Zelf nog zwak (eerlijk)
- **Bovensnavel** is maar 9 px (1/F) en leest op 1× als een dun donker streepje, niet als grijze snavel; het silhouet laat niet meer toe.
- **Vleugel** is nu een vlakke plaat zonder veren (de streepjes lazen als stippen en zijn weg); netjes, maar minder afgewerkt dan Taillow.
- **Onderbuik**: een rechte lila band (y40) boven een rechte zwarte onderrand (y41, 12 px): stijf, niet rond.
- **Hooglicht 7** in de borst is een trapjesvlak, niet een zachte ronding.
- **Kop achter het oog**: B/E-banden staan verticaal en lezen als strepen.
- **Pootjes** zijn donkere blokjes zonder vorm (zoals r10).
- Het silhouet zelf (Jordi twijfelt): in kleur leest de bovenkant als een vogel met korte nek, maar de kop zit vrij ver naar achteren op het lijf; dat is aan het silhouet, niet aan de kleur.

## Lessen
- Een vlak tussen twee kleurzones (flank tussen borst en vleugel) in één schaduwtint wordt een dode plak; eerst basis 4, schaduw alleen naar de rand toe.
- Rijen als (y, x_start, string) schrijven en de lengte tegen het silhouet laten controleren voorkomt telfouten bij handwerk.
