# Great potoo: SPEC (Gemini-model, 7 nov)

Werkwijze: **Gemini-model namaken** (`docs/lessen/SPRITE_WERKWIJZE.md`, voorbeeld poedelmot) + `docs/lessen/SPRITE_KERN.md`. Twee eisen, verder niets: (1) heel accuraat op het model, (2) Gen 3 volgens onze eisen.

Eerdere potoo-rondes (5–6 nov, Ghost/Normal, één stage, foto's, poppetje, 3D) staan op branch `claude/laughing-darwin-7smba1` (`docs/concept/sprites/potoo/SPEC.md`); dat ontwerp is vervangen door dit model. Type en data later.

## Jordi's woorden (letterlijk)
- (6 nov, bij `referenties/gemini_v1_goed_oog_snavel.png`) "ik ben wel al tevreden over oog en snavel"
- (6 nov) "de tak hoort niet in de sprite, die moet helemaal weg"
- (6 nov) "de klauwen mogen best doen alsof ze op een tak zitten, dit beeld spiegelen kan je zelf, ik vind het lichaam iets te kort, mag net wat langer"
- (7 nov) "hij is best goed namelijk, snavel en hoofd kloppen, het lichaam moet net wat groter (wel in verhouding blijven) en de tak moet weg, voor de rest precies zo vertalen naar een gen 3 sprite"
- (7 nov, bij de eerste lijfmaten) "je hebt hem dikker gemaakt, niet langer"
- (7 nov, bij `referenties/gemini_model_jordi.jpg`) "dit is alles wat ik heb, ga maar los, volg de werkwijze van de poedelmot"; "met als uitzondering de wijzigingen die we besproken hebben, maar alleen die"

## Toegestane wijzigingen t.o.v. het model (alleen deze)
1. **Tak weg**: takeinde in de klauwen en het losse takje. Klauwen blijven gekruld alsof ze een tak vasthouden.
2. **Lijf langer**: kop, oog, snavel en muil ongewijzigd; lijf eronder alleen in de hoogte opgerekt, breedte gelijk (`model/lijf.py`; eerste versie maakte hem ook breder: "dikker, niet langer").
3. **Spiegelen** (kijkt links-voor).
Verder alles precies zoals het model (ook de kuif, het verenpatroon, de spikkels, de blauwpaarse muil, het oog met glans).

## Bestanden
- `referenties/gemini_model_jordi.jpg`: het model (Jordi). `gemini_v2_afgekeurd.png`: afgekeurd, niet gebruiken.
- `model/knip.py` → `model_los.png` (los van het nep-dambord, tak weg). Restpixels olijf aan de linkerkant van het klauwgat zijn tak, geen klauw.
- `model/lijf.py` → `model_lijf_10/20/30.png` (gespiegeld). Vergelijking: `model/lijf_maten_vel.png`.

- (7 nov) "de meest rechtse, ga maar los" → **lijf +30% langer** (`model/model_lijf_30.png`).

## Silhouet (bevroren, 7 nov)
- `silhouet/silhouet.png` = model_lijf_30 direct verkleind (`silhouet/sil.py`, alpha ≥ 0,45): 1229 px, x 17–46, y 1–63. Rode omtrek: `silhouet_over_bron.png`; kleurgids (gemiddelde, géén sprite): `gids_gemiddeld.png`; `model_64_box.png`, `model_12x.png`.
- Meetgereedschap (`gereedschap/`, kader in `kader.json`): `px.py` (model per spritepixel), `box1x.py` (model | sprite op 1×-niveau vergroot), `overlay.py` (spritelijnen over het model).

## Varianten
- (7 nov, bij r6) "ik vind hem eigenlijk al heel goed, probeer eens eentje met een groot zwart oog? zonder wit erin"; "ter vergelijking" → `varianten_oog/` (A: glans zwart; B: ook ring zwart, groter oog).
- (7 nov) "ja b is beter, alleen het oog mag nog wel wat schaduw" → `varianten_oog/schaduw.py`: C1–C4.

## Eindkeuring (7 nov)
- Jordi: "ja c4 is het beste, ga maar door naar eindkeuring qua schaduw en kleuren, volgens dragonflycave en vergelijking met andere pokemon".
- `eindkeuring/RAPPORT.md` (REPARATIES, 35 indexwissels) → toegepast in `eind_r1/potoo.png` (`repareer.py`, controle op oude waarde). Ter info open: klauwen lezen als zwarte vlek; snorharen niet taps.

## Open
- Naam, type en data later.
