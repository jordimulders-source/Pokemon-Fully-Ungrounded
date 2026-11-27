# r15 – benen per ring zoals de Gen 3-Hitmonlee + rondere koepel

Basis: `r14/r14.png` (= ek2 + arm taps). Opdracht (Claude na r14, met Jordi's woorden "de benen hebben slordige rechte lijnen ipv de vorm die hitmonlee hoort te hebben ... kijk naar de oorspronkelijke hitmonlee hiervoor"): ringaantal van het model is op 64 px geen harde eis, de Gen 3-bouw wel; koepel-top hooguit ±4–5 px vlak.
Bestanden: `r15.png` (64×64 geïndexeerd, palet ek2 ongewijzigd, 15 kleuren + 0), `r15_8x.png`, `diff_ek2_r15.png`, `vel.png` (ek2 | r15 | model | Gen 3-Hitmonlee op 8×, diff, 1×/2× licht/donker), `rechte_lijnen_overlay.png` (uit r14, de check op ek2), `log.txt` (alle 138 px die van ek2 afwijken, met zone), `bouw.py`, `vel.py`.

## Benen (Gen 3-bouw)
Gen 3-Hitmonlee (`anim_front_gba.png`): spiraal = segmenten van ±3 px met licht → mid → donker dwars over de cilinder, 1-px donkere scheiding, en per ring een eigen stap in de buitenrand (geribbeld). Toegepast op ons model, als tabel per rij in `bouw.py` (KB/SB):
- Elke ring = 3 rijen: bovenrij volle breedte met ramp (trapbeen 15-7-6-5-4, standbeen 7-6-5-4), middenrij (de boog: midden 3-2-2, lichtkant 8, schaduwkant 5/4), onderrij 1 px ingekeept aan beide kanten met donkere ramp (6-5-4 / 5-4). De scheiding is dus een boog: uiteinden in de inkeping, midden 1 rij lager (zoals de bogen in het model).
- Buitenrand: per ring een bolletje (volle breedte) en een inkeping; links selout 2 (lichtkant), rechts zwart (schaduwkant).
- Trapbeen: 4 ringen tussen de voetlijn (rij 11, ongewijzigd) en het doorschijnende deel (laatste boog loopt in rij 23 door); been buigt 2 px naar links naar de romp toe (rij 12–15 kol 42–48, 17–18 kol 41–47, 20–21 kol 40–46), zoals model/ek2. Breedte op de bolletjes = modelbreedte (7).
- Standbeen: 3 ringen + een halve onder de romp (rij 44–53), loopt 1 px naar rechts (model/ek2).
- Ringaantal: trapbeen 4 (model ±6), standbeen 3½ (model ±5): bewust, het modelaantal past op 64 px alleen als 1-px ladder.

## Koepel
Model gemeten (uniform gefit, subpixel bovenrand per kolom): kol 19–25 op 20,8–20,9, kol 17/18/26 op 21,3–21,4, daarna 22, 22,9, 24,8. Nu: toprij 20 = 5 px (kol 20–24, modeldekking 0,19), rij 21 kol 18–26, dan trapjes 2-2-2-1-1-1 links en 2-2-2-1-1 rechts. Binnenkant rij 21 kol 20–24 in de tinten van rij 22 (12,12,11,11,11).

## Afwijkingen van ek2: 138 px (silhouet 40)
koepel 14, arm 8 (r14), trapbeen 66, standbeen 50. Elders diff 0 (`diff_ek2_r15.png`).
Niet uit het model: de ringtabellen (Gen 3-bouw, tinten uit ons palet volgens de modelmeting bleek links / oranjerood rechts), de inkepingen (modelribbels zijn subpixel), de 5 toppixels van de koepel (dekking 0,19).

## Rechte-lijnencheck r15
Over: zool trapvoet (9, plat in het model), toprij koepel 5, onderkant romp 42/46, linkerwand kol 10 (5) en 12 (7), verre arm kol 37 (6): alle ook recht in het model gemeten (zie r14/NOTITIES). Geen runs meer in de benen.

## Twijfelpunten
1. Trapbeen leest door de inkepingen iets dunner/kraleriger dan het model (bolletjes = modelbreedte, inkepingen 2 px smaller).
2. Toprij koepel ligt 1 rij hoger dan de 0,5-drempel van het model (dekking 0,19); alternatief is pixels wegsnijden uit rij 21 (dekking 0,75–1), dat wijkt meer af.
3. Linkerwand ongewijzigd (model recht).
4. Nog niet onafhankelijk gekeurd.
