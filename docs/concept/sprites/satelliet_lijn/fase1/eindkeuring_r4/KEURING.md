# Eindkeuring Dragonfly Cave: satelliet fase 1, sprite r4 (23 nov)

Gekeurd: `../sprite_r4/sprite.png` (64×64, P, index 0 transparant, 10 kleuren, 985 px, box 46×41) tegen `../model/model_gekozen_natief.png` (×0,617) en de kale reductie `../sprite_r4/kaal.npy`. Verse keurder: eerst blind geoordeeld, daarna pas `../sprite_r4/RAPPORT.md` en `../eindkeuring_r3/KEURING.md` gelezen (geen tegenspraak). Alleen uitvoering, geen herontwerp.
Bestanden: `vel.py` → `vel.png` (r4 8× | model ×0,617 8×; r4 en r3 op 1×/2× licht en donker; Voltorb, Magnemite, Beldum, Lunatone, Shuppet uit `anim_front_gba.png` op 2× en 1×; uitsnede van het optionele voorstel), `voorstel.py` → `voorstel.png`/`voorstel.npy` (optioneel, 1 px).

## Eindoordeel: **PASS**
Beide eisen gehaald, en Jordi's punten ook. Eén optionele pixel (zie onder) is geen voorwaarde.

## Gids (letterlijk, waarop ik oordeel)
- r. 96–98: *"The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites"*
- r. 112–114 (regel 3): *"The outline base and outline highlight colors are also colors."*
- r. 117 (regel 4): *"The outlines must be reasonably dark."*
- r. 421–423: *"we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."*
- r. 425–429: *"the R/S sprite actually also features some anti-aliasing on the outside of the outline. This is a bad idea … lighter pixels on the inside of the outline are a far better idea"*
- r. 452–455: *"Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts … on the inside of the outline rather than the outside."*

## Eis 1: trouw aan het model: PASS
- Silhouet tegen de kale reductie: 24 px verschil, vrijwel alles de antenneverdikking (22 px, nodig voor "geen 1 pixel lijnen", Jordi zag dit al in r4) plus (43,11) en (50,25) voor de rondheid. Geen onderdeel verschoven.
- Onderdelen compleet: bol, oog (paarse ring, teal iris, zwarte pupil, oogrand zwart rechts/onder zoals in het model), gebogen naad (1 px P), voetjes rechtsboven en rechtsonder als knopjes, 4 antennes in de modelrichtingen (geen 5e), gat tussen voetje rechtsboven en antenne 2 (rij 22) zoals in het model.
- Op deze maat niet te tonen (telt niet): de donkere binnenring van het oog en het voetje linksboven als los knopje (nu een 3 rijen dikke wortel van antenne 1). Zie "ter info".

## Eis 2: Gen 3: PASS
| punt | meting | oordeel |
|---|---|---|
| Volume | bol: hooglicht W linksboven, basis w, l → m als sikkel rechtsonder die de bol volgt; voetjes licht p linksboven, zwart rechtsonder; oogring licht onder, donker boven/rechts zoals het model | volume, geen pillow, geen banding |
| Tinten per groep | lijf W/w/l/m = lum 255/225/183/138 (stappen 30/42/45; Magnemite 33/27/58); paars D/P/p = 64/93/143; teal T/t = 108/184 | gelijk aan r3 (PASS) |
| Tintvlakjes < 3 px | lijf (W/w/l/m) en teal: 0 losse clusters (8-buren). Kleine p/P-stukjes alleen in de antennes (2 vultinten, door Jordi goedgekeurd) en in de oogring (39,17); plus P (41,35), zie optioneel | ok |
| Buitenlijn | 1 px, 0 open randen (`zwart.py`); op de buitenrand alleen D en zwart (0 lichte pixels) | dicht |
| D/zwart om en om | één plek: zwart (23,35) in het kerfje tussen voetje en antenne 2; dat is de bovenpunt van de scheidingslijn voetje/antenne, staat zo in de kale reductie en in r3 (18,36, PASS) | geen dambord |
| Zwart | 159/985 = 16,1 % (checklist E3: 0,10–0,25); 2×2 zwart alleen in de pupil | binnen de band |
| Binnenlijnen | naad P (niet zwart); waar een onderdeel tegen de bol ligt zwart aan de schaduwkant, zoals Magnemite (`anim_front_gba`: F tussen magneet en lijf, rij 26–29 en 34–36) en r3 | consistent |

## Jordi's punten
- **"let erop dat de bol mooi rond blijft"** (`rond4.py`): centrum (23,5; 35,6), r = 14,23; max per kwadrant +0,33 / +0,70 / +0,38 / +0,71 px (r3: ≤0,78). Trappen links 1-1-1-1-1-2-2-9-2-2-1-1-1-1-1-1 (symmetrisch; Voltorb heeft er 8 recht bij r ≈ 13), onder 1-1-1-1-1-1-2-2-3-3-3-2. **Ok.**
- **"let op onnodige zwarte pixels ook"**: alle 40 zwarte pixels zonder lucht ernaast nagelopen: pupil (12); oogrand rechts/onder (10, model); onderkant antenne 1 op de bol (21,25–29) = schaduwkant van de antenne (Magnemite); scheiding voetje/antenne 2 (24,36); onderboog voetje rechtsboven (27,30), (28,31), (29,32–34); bolrand achter antenne 3 (37–38,37) en achter voetje rechtsonder (43,32–33), (45–47,30). De zwarte buitenrand zit alleen rechts, onder en linksonder (vanaf rij 38, net onder het midden), plus de onderkanten en punten van de antennes. Geen zwart aan de lichtkant, geen verdikkingen buiten de pupil. **Ok, geen onnodige.**
- **Antennes "zodat het geen 1 pixel lijnen worden"**: per kolom 3–4 px hoog met 2 px kleur (D boven, P/p, zwart onder); alleen de uiterste punten (kol 39–41, 53–54) dunner. **Ok.**
- **Oog zonder glans**: geen W in het oog; t (3 px linksboven in de iris) is het lichte deel van de iris uit het model, geen glimvlek. **Ok.**
- Antennes met 2 vultinten + lijn: door Jordi goedgekeurd, niet gekeurd.

## Optioneel (geen voorwaarde)
- **(41,35): P → m.** Losse paarse reflectiepixel in de schaduwsikkel rechts, net boven voetje rechtsonder (komt uit het model, waar daar een lichte rand binnen de lijn loopt). Getest in `voorstel.py` (assert op oude waarde, silhouet gelijk, diff 1 px; `zwart.py`: 0 open randen, 0 losse vultint; `rond4.py` ongewijzigd). Op 1× en 2× onzichtbaar; mag ook blijven.

## Ter info voor Jordi (geen reparatie)
- Het voetje linksboven is op deze maat geen los knopje meer maar een verdikking aan de wortel van antenne 1, en de donkere binnenring van het oog past niet; dat meldde de maker al bij de keuze voor r4.
