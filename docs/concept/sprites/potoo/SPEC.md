# Great potoo: SPEC (Gemini-model, 7 nov)

Werkwijze: **Gemini-model namaken** (`docs/lessen/SPRITE_WERKWIJZE.md`, voorbeeld poedelmot) + `docs/lessen/SPRITE_KERN.md`. Twee eisen, verder niets: (1) heel accuraat op het model, (2) Gen 3 volgens onze eisen.

Eerdere potoo-rondes (5–6 nov, Ghost/Normal, één stage, foto's, poppetje, 3D) staan op branch `claude/laughing-darwin-7smba1` (`docs/concept/sprites/potoo/SPEC.md`); dat ontwerp is vervangen door dit model. Type en data later.

## Jordi's woorden (letterlijk)
- (6 nov, bij `referenties/gemini_v1_goed_oog_snavel.png`) "ik ben wel al tevreden over oog en snavel"
- (6 nov) "de tak hoort niet in de sprite, die moet helemaal weg"
- (6 nov) "de klauwen mogen best doen alsof ze op een tak zitten, dit beeld spiegelen kan je zelf, ik vind het lichaam iets te kort, mag net wat langer"
- (7 nov) "hij is best goed namelijk, snavel en hoofd kloppen, het lichaam moet net wat groter (wel in verhouding blijven) en de tak moet weg, voor de rest precies zo vertalen naar een gen 3 sprite"
- (7 nov, bij `referenties/gemini_model_jordi.jpg`) "dit is alles wat ik heb, ga maar los, volg de werkwijze van de poedelmot"; "met als uitzondering de wijzigingen die we besproken hebben, maar alleen die"

## Toegestane wijzigingen t.o.v. het model (alleen deze)
1. **Tak weg**: takeinde in de klauwen en het losse takje. Klauwen blijven gekruld alsof ze een tak vasthouden.
2. **Lijf groter, in verhouding**: kop, oog, snavel en muil ongewijzigd; lijf eronder groter in hoogte en breedte (`model/lijf.py`).
3. **Spiegelen** (kijkt links-voor).
Verder alles precies zoals het model (ook de kuif, het verenpatroon, de spikkels, de blauwpaarse muil, het oog met glans).

## Bestanden
- `referenties/gemini_model_jordi.jpg`: het model (Jordi). `gemini_v2_afgekeurd.png`: afgekeurd, niet gebruiken.
- `model/knip.py` → `model_los.png` (los van het nep-dambord, tak weg). Restpixels olijf aan de linkerkant van het klauwgat zijn tak, geen klauw.
- `model/lijf.py` → `model_lijf_10/20/30.png` (gespiegeld). Vergelijking: `model/lijf_maten_vel.png`.

## Open
- Lijfmaat: +10, +20 of +30% (Jordi kiest).
