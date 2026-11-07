# Hatun runa – kleur ronde 3

Basis: `../kleur_r2/raster.txt`. Handwerk: `stappen/e_kop3.txt` (kop) en `stappen/e_goud.txt` (nabije vleugel). `vel.png`: r3 | r2 | model op 8×, kop/vleugel 12×, 1×/2× licht en donker + model 1×.
**Pixeldiff met r2: 59 px (kop 24, vleugel 35), allemaal binnen de zones kop (x9–27, y46–55) en nabije vleugel (x28–43, y26–46); 0 erbuiten** (script onder in deze ronde gedraaid). Silhouet-diff 0 (971 px).

## Reparaties (benoemd door Claude)
1. **Oog:** opgebouwd zoals het Taillow-oog (`graphics/pokemon/taillow/anim_front_gba.png`: zwarte pupil met licht eromheen, geen losse glanspixel): pupil 2×2 op de gemeten plek (18–19, 47–48); erboven de wenkbrauw, links de witte voorkant van de wenkbrauw (model rij 47 wit x15–17.5), rechts de witte sikkel (20,47–48), eronder een grijsbruine iris E (18–19,49). De pupil staat zo los van het masker.
2. **Snavel en open bek:** bovensnavel als eigen wig (lichtgrijze bovenkant C rij 49, B eronder, zwarte onderrand); onderkaak als eigen schuine vorm (C op (17,51),(16,52),(15,53), B op (14,54)) met zwarte buitenrand; rode/zalm bek ertussen ((14–16,51), (15,52), (14,53)).
3. **Witte keel:** één wit vlak (x18/19–24, rij 50–53) zonder losse zwarte pixels binnenin; vloeiende grens naar het geel (rij 50–51 x25, 52 x24, 53–54 x23), lichtgrijze schaduw alleen onderaan; zwarte lijn onder het masker is nu masker (F).
4. **Masker:** één band F: snavelbasis (16–17,48–50) → onder het oog (rij 49–50) → achter het oog (x21–26, rij 47–49) tot de nek; de bobbel in de wenkbrauw is weg (rij 46 helemaal wit).
5. **Goudgele onderkant:** geen rechte banen meer: de veerlijnen lopen als korte bruine streepjes schuin door het goud (van de punten naar de vleugelbasis, bv. (35,35),(34,36) en (36,38),(35,39)), goud begint bovenaan als punt (34,27) zoals het model; de voorrand gaat van 5 (boven) via 4 naar 3 (onder) in plaats van één lichte baan.

## Afwijkingen van het model
- Oog: geen losse glanspixel in de pupil (Taillow-opbouw; een glans zou op 64 px met de witte rand versmelten); de witte rand rond de pupil is iets breder dan in het model.
- Verder als ronde 2 (verre vleugel 3 scheidingen, tapse lijnen, snavelselout B op (12,48)/(11,49)).

## Open punten
- Oog: op 1× een donkere stip in wit met het masker erachter; keurder graag laten oordelen of het genoeg oog is.
