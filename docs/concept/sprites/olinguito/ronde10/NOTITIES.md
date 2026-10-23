# Olinguito ronde 10: klauw repareren (basis ronde 9)

Ronde 9 met één hoofdreparatie (Jordi) en twee lichte extra's. Het masker blijft (Jordi: leuke touch); de foto is inspiratie, geen blauwdruk.

## Wat er veranderde
- **Dichtbije klauw** (`klauw_voor` in `bron/delen.txt`): het massieve blok (±6 px breed, 13 px hoog) is vervangen door twee slanke, gebogen klauwen van 2–3 px breed, met dezelfde lengte (±11 px, tot y 54–55). Eén klauwvorm (helling 1-1-2-4, dan een haakpunt naar rechts, zoals bij Sandslash en Sneasel) staat twee keer, verschoven (+3, +1). De voorste klauw ligt over de achterste, zodat er maar één zwarte scheidingslijn tussen zit (pseudo-omlijning). Wortels onder de poot, licht van linksboven (a/9, schaduwrand 8, zwart rechts). De dichtbije klauw is nu nog ±7 px breed, de verre (ongewijzigd) ±6 px: dat past bij een 3/4-aanzicht.
- **Oren** 1 px lager en ronder (koepel 3→5 en 4→6 px), het verre oor kleiner dan het dichtbije.
- **Staart:** de zwarte ringen zijn vage ringen in de schaduwtint (`122220`/`132220` in plaats van `011110`), waardoor hij meer als één pluim leest. Het silhouet bleef gelijk.
- Verder niets: masker, ogen, kleuren, lijf, voeten, verre arm en de framebeweging zijn identiek aan ronde 9.

## Controle
- Open randen: geen (beide frames).
- Rechte randstukken > 4 px: geen (in ronde 9 had de klauw er een van 7 px).
- Zwart-aandeel rand: 0,61 / 0,62 (ronde 9: 0,62–0,64; doel 0,35–0,6, nog net te hoog door het donkere lijf).
- Oppervlak: 1050 / 1062 px (ronde 9: 1099).
- Frames consistent: de klauw, kop, armen en staart gaan in frame 2 samen 1 px omhoog.

## Bestanden
- `anim_front.png`, `normal.pal`, `compare.png` (ronde 9 en 10, beide frames, 1× en 3×).
- `bron/delen.txt` (bewerkt), `bron/bouw9.py` (ongewijzigd; `python3 bron/bouw9.py <ronde10-map>`), `bron/vergelijk10.py`, rasters en palet.
