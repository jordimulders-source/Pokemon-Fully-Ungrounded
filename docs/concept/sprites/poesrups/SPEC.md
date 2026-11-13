# Poesrups (tussenvorm Pupoodle → Lanymph): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md` (Gemini-model namaken) + `docs/lessen/SPRITE_KERN.md` (BELANGRIJKSTE REGEL: alleen (1) heel accuraat op het model, (2) Gen 3 volgens onze eisen) + `docs/lessen/GEMINI.md`. Lijn: Pupoodle (`../poedellarve/`) → **poesrups (fase 2 van 3)** → Lanymph (`../poedelmot/`). Echte soort: puss caterpillar, rups van de flanelmot (Megalopyge). Gemini-rondes: `gemini/README.md`.

## Jordi's woorden (13 nov, letterlijk)
- "Het moet dus vooral een harige rups zijn, mysterieus en cryptid, maar dus ook pluizig, het gaat dus om die harige rups vorm"
- (op Gemini ronde 1) "hij doet nu dit maar die lijkt neit op de poesrups"
- (op ronde 2) "vind het nog niet genoeg de puss caterpillar" / "hij is sowieso nog niet insect genoeg"
- (op ronde 3, twee plaatjes) "hij deed eerst de tweede, daarna zei ik dat die meer bedekt moest worden en je alleen de ogen mocht zien. Die zijn nu iets teveel zoogdier nog. Maar we hebben een model verder, met alleen nog de ogen die iets anders moeten, doe maar zoals jij initieel van plan was en bouw de sprite"
- (op kleur r1, terwijl r2 liep) "prima, begint al ergens op te lijken"
- (op kleur r2, op de vragen oog A/B/C en of de kam groter mag dan in het model) "ik zie tussen A en C geen verschil, beide prima., de kam mag prima groter" → **oog A** (keuze Claude tussen A en C); **kam mag groter dan in het model.**
- (op kleur r3) "ja dit is te overdreven. Ik vind ronde 2 al uitstekend, wat wilde je er nog aan veranderen?" → **r3 vervalt; r2 is de basis.** Ronde 4 (kam als volle plukken) gestopt. Variant ter keuze: `kleur_r2b/` = r2 met alleen de 24 px buiten de kam uit r3 (derde ronde pootje, minder loklijnen, randje bij het verre oog).

## Bron
- `referenties/model_gekozen.png`: **het model (bevroren)**: de bedekte versie (alleen de ogen zichtbaar onder de vacht). Kijkt al naar links.
- `referenties/gemini_eerdere_versie_kop_zichtbaar.png`: de versie ervoor (kale kop zichtbaar); alleen ter info, niet de bron.

## Ogen (het enige dat van het model afwijkt)
- Jordi: de ogen van het model zijn "iets teveel zoogdier"; "doe maar zoals jij initieel van plan was".
- Claude's plan uit de prompts (letterlijk): "two dark, glossy eyes ... visible between the strands", "Near-black eyes with one small white highlight", "No nose, no mouth, no eyebrows". Dus: bijna-zwarte, ronde, glanzende ogen met één witte glans, zonder oogwit, ooglid of wenkbrauw; op de plek van de modelogen, tussen de haren.

## Besloten
- Formaat (keuze Claude, fase 2 van 3 tussen de larve 40 px/778 px en de mot 62 px/1782 px): **54 px breed**.
- Silhouet: `silhouet/silhouet.png` (model direct verkleind, `silhouet/sil.py`; 54×33, 1046 px, x 5–58, y 29–61, schaal 16,648 modelpx per spritepixel, links 5, boven 29; modelbox x 69–968, y 240–794). Rode omtrek over het model: `silhouet/silhouet_over_bron.png`; kleurgids: `silhouet/gids_gemiddeld.png`. Bevroren; alleen dunne delen (krullen van de kam, pootjes) mogen met de hand.

## Open
- Naam, type en data later (Jordi, 5 nov).
