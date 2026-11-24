# Eindkeuring Dragonfly Cave: satelliet fase 1, sprite r3 (23 nov)

Gekeurd: `../sprite_r3/sprite.png` (64×64, P, index 0 transparant, 10 kleuren) tegen `../model/model_gekozen_natief.png` (×0,787) en de kale reductie `../sprite_r1/kaal.npy`. Verse keurder; eerst blind geoordeeld, daarna pas `../eindkeuring_r2/KEURING.md` gelezen. Alleen uitvoering, geen herontwerp.
Bestanden: `vel.py` → `vel.png` (r3 8× | model 8×; r3 1×/2× op licht en donker; Voltorb, Electrode, Magnemite, Beldum, Lunatone uit `anim_front_gba.png` op 2× en 1×), `voorstel.py` → `voorstel.png`/`voorstel.npy` (optioneel, 1 px).

## Eindoordeel: **PASS**
Beide eisen gehaald, en Jordi's vier punten ook. Eén optionele pixel (zie onder) is geen voorwaarde.

## Gids (letterlijk, waarop ik oordeel)
- r. 96–97: *"The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites"*
- r. 112–114 (regel 3): *"The outline base and outline highlight colors are also colors."*
- r. 115–116 (regel 4): *"The outlines must be reasonably dark."*
- r. 419–423: *"color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."*
- r. 425–428: *"the R/S sprite actually also features some anti-aliasing on the outside of the outline. This is a bad idea … lighter pixels on the inside of the outline are a far better idea"*
- r. 443–444: *"the wing "shadow color" is really used where the front wing overlaps the back wing"*

## Eis 1: trouw aan het model: PASS
- Silhouet tegen de kale reductie: 7 px verschil (3 erbij, 4 eraf), allemaal afronding op de bolrand en één antennepunt; geen onderdeel verschoven. Oppervlak 1548 px, box 52×59.
- Onderdelen compleet: bol, oog (paarse ring, teal iris, zwarte pupil), gebogen naad, 3 voetjes, 4 antennes (geen 5e), gaten tussen bol, voetje en antenne 2 (rij 17) zoals in het model. De lichte band onderaan de bol (rij 49–51) is de paarse reflectierand uit het model, in de lijftint vertaald (kleur mag afwijken).

## Eis 2: Gen 3: PASS
| punt | meting | oordeel |
|---|---|---|
| Volume | bol: groot hooglicht W linksboven, basis w, sikkel l → m rechtsonder die de bolvorm volgt; oogring licht linksboven, donker rechtsonder | ja, geen pillow, geen banding |
| Tinten per groep | lijf W/w/l/m = lum 255/225/183/138 (stappen 30/42/45); paars D/P/p = 64/93/143 (29/50); teal T/t = 108/184 | ≤ 4 per groep, stappen binnen ±30–50 (teal = oog) |
| Tintvlakjes < 3 px (8-buren) | alleen p (7,40), (33,54), (33,56): glimpixels op de antennes; (7,40) en (33,56) staan zo in de kale reductie | toegestaan als glans; (33,54) zie optioneel |
| Buitenlijn | open randen 0 (`check.py`); geen D/zwart om en om op één rand (script: 0 geïsoleerde wissels); 2×2 zwart alleen in de pupil | dicht, 1 px |
| Zwart | 209/1548 = 13,5 % (Gnomad r10 goedgekeurd 13,0 %; Beldum 13,5 %). Bovenrand en linksboven D; zwart rechts, onder en linksonder | alleen schaduwkant |
| Binnenlijnen | naad paars (geen zwart); voetjes: bovenkant D, schaduwkant zwart zoals Magnemite's magneten/schroeven op het lijf (gba: zwart F tussen magneet en lijf, kol 10–11) | consistent met Gen 3 en r2 |
| Lichte kleur op buitenrand | 0 | ok |

## Jordi's punten
- **"let erop dat de bol mooi rond blijft"**: `rond.py`: centrum (20,6; 33,7), r = 18,26; max afwijking per kwadrant −0,64 / +0,68 / +0,64 / +0,78 px (kale reductie: tot 0,86). Op 8× en 1× rond. **Ok.**
- **"let op onnodige zwarte pixels ook"**: elk zwart pixel nagelopen: pupil (18), oogboog rechts/onder (uit het model, Beldum-oogkas), lijf rechts/onder, linksonderboog (onze Gnomini-regel), schaduwkant van voetjes en antennes. Geen zwart aan de lichtkant, geen verdikkingen buiten de pupil. **Ok.**
- **Antennes "zodat het geen 1 pixel lijnen worden"**: kleurdikte per kolom (P/p): antenne 1 ≥ 2 behalve de punt (kol 41–43), antenne 2 ≥ 2 (punt kol 60 alleen lijn), antenne 3 ≥ 2 behalve punt (kol 58–59), antenne 4 ≥ 2 (punt kol 58–59 alleen lijn). **Ok.**
- **Oog zonder glans**: geen W in het oog; de lichte teal t (7 px, linksboven in de iris) is het volume van de iris, geen glimvlek. **Ok.**

## Optioneel (geen voorwaarde)
- Bovenrand antenne 3, rij 33: `p P p` (kol 54–56) is een mini-dambord. **(33,55): P → p** maakt er één glim van 3 px van. Getest in `voorstel.py` (assert op oude waarde, silhouet gelijk, diff 1 px); op 1× onzichtbaar. Mag ook blijven.

## Ter info voor Jordi (geen reparatie)
- Linksonder (kol 2–8, rij 37–47) is zwart volgens onze Gnomini-regel; de echte Gen 3-bollen Voltorb/Electrode/Lunatone (`anim_front_gba.png`) hebben daar de donkerste eigen tint (1 px zwart met lucht links). Let op: de `anim_front.png`-bestanden in de expansion zijn níet de GBA-sprites en hebben daar wél zwart; meet altijd met `_gba`.
- Formaat: 1548 px is ruim voor een fase 1 (FAKEMON_CHECKLIST D1: 700–950; de bol alleen is ±1050, de rest zijn antennes). Fase 2 en 3 moeten groter en complexer worden (Jordi: "groter en complexer"); in 64×64 is daar weinig ruimte meer. Iets om mee te nemen bij de satelliet- en ruimtestationmodellen.
