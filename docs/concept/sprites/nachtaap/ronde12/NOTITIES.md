# Nachtaap ronde 12: A6 (+ variant spiraal)

Basis: `../ronde11/anim_front.png` (goedgekeurd, zonder elleboog; de PNG is leidend, `ronde11/bron` bouwt nog de elleboog). Openstaand uit `checklist_keuring/KEURING.md` §3. Niet gedaan: de elleboog (afgekeurd), B1 (kop draaien; mocht niet). Palet ongewijzigd (15 kleuren), transparency=0. Romp en armen zijn in beide frames gelijk. Script: `bron/nachtaap12.py`.

| Punt | Wat | Waar (frame 1) | Pixels |
|---|---|---|---|
| A6 zuil breken: knikje | De onderarm van de verre arm (y49–50) schuift 1 px naar buiten, naar de hand toe (die stond al op x33–36). De romp-zijkant (heup) wordt daar 1 px breder: `3` op x32, scheiding `1` op x33, arm x34–35, omlijning x36. Er is geen bult en de pols gaat niet terug, dus dit is niet de afgekeurde elleboogvorm. | x32–36, y49–50 | 8 |
| A6 zuil breken: schaduw | De schaduwkant van de verre arm (rechterkolom x34, y42–48, en x35 op y49–50) wordt een tint donkerder (`3`→`2`). De arm wordt een eigen rond lichaamsdeel (licht links, donker rechts) en is niet meer één vlak met de romp-zijkant `33`. | x34–35, y42–50 | 7 |

Totaal 15 px per frame. **Pixeldiff buiten de zones: 0.** Open randen: 0 nieuw. Oppervlak 1033 → 1035.
**Zelfcheck** (1× en 3× naast ronde 11, `TOEGEPAST2.png`): op 3× is de verre arm nu een aparte, ronde arm die onderaan iets uitwaaiert naar de hand. Op 1× is het verschil klein. De uitdrukking en het gezicht zijn ongewijzigd. Eerlijk: de zuil is gebroken, maar het blijft een kleine ingreep. Meer kan alleen met een andere armvorm, en die is net afgekeurd.

## variant_spiraal/ (groot, ter keuze): D1 ≤ 950
Ronde 12 met een kleinere staart. Kop, lijf en armen zijn pixel voor pixel gelijk; alleen de staart verandert (alle wijzigingen liggen in x36–60, y21–48). Script: `bron/nachtaap12_spiraal.py`.
- **Spiraal met de hand verkleind** in dezelfde opbouw: bovenband `2/5/4/3/1`, zijkanten `2-4-1`, binnenpunt en onderband. Het formaat gaat van 13×12 naar 10×9 px. De binnenpunt is nu 1 px breed (`2`), was 3.
- **Stam 6 rijen korter:** de spiraal zakt langs de stam en staat nu rechts naast de kop (y32–40) in plaats van erboven.
- **Stam 3 px dik** (`2-4-1` in plaats van `2-4-3-1`), passend bij de kleinere spiraal. De aanzet bij de heup blijft gelijk.
- Oppervlak **950** (frame 1; frame 2: 934); de box wordt 44×36 (was 49×36), dus ook D4 (≤ 48) klopt nu. Open randen: 0 nieuw.
- Op 3× leest de spiraal nog als krul, met de binnenpunt zichtbaar. Op 1× is het een kleine krul. **Nadeel:** het tegenwicht staat niet meer rechtsboven maar rechts op ooghoogte (A3 zwakker), en de staart is als kenmerk (A2) minder dominant. Daarom alleen als variant.
