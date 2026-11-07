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
- (7 nov, letterlijk) "middelste op, ga maar mee aan de slag" → **gekozen: 60%** = `referenties/model_gekozen.png` (kopie van `model/laag_60.png`). **Dit is nu het model (bevroren).**
- (7 nov, letterlijk) "houd er rekening mee dat dit een zwakke 1e vorm is, dus die evolved op lvl 15-20 max"
  → Formaat als Wurmple/Caterpie/Grubbin (gemeten: 600–800 px; Grubbin 39×25): **40 px breed**.

## Besloten
- Silhouet: `silhouet/silhouet.png` (gekozen model direct verkleind, `silhouet/sil.py`; 40×30, 778 px, x 12–51, y 33–62, schaal 13,55 modelpx per spritepixel, links 12, boven 33). Rode omtrek over het model: `silhouet/silhouet_over_bron.png`. Kleurgids (gemiddelde kleur per pixel, géén sprite): `silhouet/gids_gemiddeld.png`. Bevroren; alleen dunne delen (sprietkrullen) mogen met de hand.

## Af (7 nov)
- (7 nov, letterlijk) "ik vind ronde 2 wel goed, maar je moet hem spiegelen idd" en "en dan is de sprite eigenlijk al af wmb"
- `af/poedellarve.png` = `kleur_r2/poedellarve.png` horizontaal gespiegeld (kijkt nu naar links, zoals Gen 3; pixel voor pixel exact gespiegeld, box x 12–51 blijft gelijk), + `normal.pal` en `af/poedellarve_8x.png`. De belichting is mee gespiegeld (licht nu rechtsboven); niet opnieuw belicht, Jordi vond hem zo af.
- Alpha t.o.v. het silhouet (vóór spiegelen): 4 px bewust gewijzigd (krulpunt links, bolletjes 2–4; zie `kleur_r2/NOTITIES.md`). Keuring: Claude op 8× + Jordi akkoord; de onafhankelijke keurder van r2 is gestopt omdat Jordi hem al goedkeurde.

## Open
- Naam, type en data later (Jordi, 5 nov).
