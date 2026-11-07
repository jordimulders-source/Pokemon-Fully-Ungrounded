# Poedellarve (voorvorm van de poedelmot): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md` (Gemini-model namaken) + `docs/lessen/SPRITE_KERN.md` (BELANGRIJKSTE REGEL: alleen (1) heel accuraat op het model, (2) Gen 3 volgens onze eisen). Eindvorm: `../poedelmot/` (fase 2 van 2; deze larve is fase 1).

## Jordi's woorden (7 nov, letterlijk)
- "Hier is de pre-evo voor de poodle moth. 100 keer gevraagd aan gemini maar hij kan hem niet minder lang maken, kijk of jij dat kan zonder het design te verknallen, als dat niet kan dan maken we dit maar het design en dan mag je hier een sprite van maken met de lessen geleerd van het poodle moth proces"

## Bron
- `referenties/jordi_gemini.png`: het model (Gemini). Witte, pluizige larve: poedelkop met twee krullende, geribbelde voelsprieten (roze-grijs), donkere grote ogen, zwart neusje, glimlach; dik voorlijf met twee pluizige voorpootjes; telescoperende achterlijfsegmenten met ronde pluisbolletjes bovenop en ronde pootjes eronder.

- (7 nov, letterlijk, op de eerste versie die het achterlijf smaller maakte) "nee het stuk onder het hoofd moet korter, hij moet niet smaller"

## Korter maken (Claude, 7 nov)
- `model/laag.py <factor> 330 500`: de band onder de kop (y 578–690: borst en voorpootjes) verticaal ingedrukt; kop, sprieten en bolletjes schuiven onvervormd omlaag; voetjes en onderrand onveranderd; het achterlijf (x ≤ 330) blijft precies zo, met een geleidelijke overgang tot x = 500.
- Varianten: `model/laag_60.png` en `model/laag_40.png`; naast het origineel in `model/vergelijking.png` (onderaan ±1× sprite, 2× getoond). Claude kiest 60% (bij 40% worden de voorpootjes platte boontjes).
- **Wacht op Jordi:** 60% of 40%. Daarna: silhouet = gekozen model verkleind (fase 1: kleiner dan de poedelmot, ±48–52 px breed), meetgereedschap uit `../poedelmot/kleur_r19/stappen/` en `kleur_r20/stappen/`, één maker.

## Open
- Naam, type en data later (Jordi, 5 nov).
