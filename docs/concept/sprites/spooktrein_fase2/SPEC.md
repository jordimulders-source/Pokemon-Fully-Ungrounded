# Spooktrein fase 2 (Steel/Ghost), frontsprite

Model: `model/model_r5.png` (= `../spooktrein_fase1_2/gemini/r5/fase2_v6.png`, prompt v6). Lijn, besluiten en alle citaten: `../spooktrein_fase1_2/SPEC.md`; rondes en prompts: `../spooktrein_fase1_2/gemini/`.

## Jordi (letterlijk, 16 nov)
- Model: "ronde 5 dan, met dingen uit ronde 6 als je dat nodig hebt" (r6: `referenties/r6.png`).
- Design r5: "ik vind de rest van het design wel tof" (alles behalve het gezicht).
- Gezicht: "gemini gaat geen goed gezicht kunnen ontwerpen" / "dan maken we zelf het gezicht wel" / "de mond moet echt overdreven groot zijn en doe maar kleine pretoogjes" / "voor de mond zat ik aan een overdreven grote O mond te denken" / "zo groot dat alleen geesten dat kunnen hebben, niet in verhouding groot".
- Ogen: "de ogen mogen zijn zoals de geest links in het rood" (`referenties/ogen_geest_rood.png`, conceptschets van geesten; de rode geest links: twee gebogen, lichtgevend geel-crème ooglijnen boven een donker gezicht). Jordi: "het gaat alleen om de vorm" / "en prima dat ze groot zijn, ben van mening veranderd" / "want ze zijn namelijk niet lang" (vervangt "kleine pretoogjes").
- Mond: "de mond mag bijna swalot achtig worden" / "of gulpin" (`referenties/mond_swalot_kaart.png`, `mond_swalot_sv.png`: Swalot met de mond wijd open, een hoge ovale opening over bijna het hele lijf). Pixelbron in de repo: Swalot Gen 3 frame 2 (`graphics/pokemon/swalot/anim_front.png`, onderste helft: open mond, wel van opzij).
- Mondreferentie Gulpin (Jordi stuurde 16 nov een tekening, kwam niet als bestand binnen): Gulpin van opzij met de mond zo wijd open dat de opening bijna het hele lijf voorin beslaat; bovenlip als brede boog onder het streepjesoog, binnenkant paars met een tong (lichtere paarse tint, links), achterin een groot zwart ovaal gat (keel); dikke zwarte omlijning.
- Jordi (16 nov): "gemini kan dat gezicht niet maken, er komt een tong in ja". Pixelbron voor de mond zoeken in Gen 3-sprites: `referenties/mond_kandidaten_gen3.png` (voorstel Claude: Loudred, Haunter frame 2, Exploud, Swalot frame 2).
- "die onderdelen die losgeschoten zijn en erachter vliegen mag je wegggummen".
- Kleur geest: "de geest blijft dezelfde kleur" (als fase 3).

## Werkwijze
Gemini-model namaken (`docs/lessen/SPRITE_KERN.md`, `SPRITE_WERKWIJZE.md` → "Gemini-model namaken", `GEMINI.md`): eisen alleen (1) accuraat op het model, (2) Gen 3. Model overnemen, nooit hertekenen.
- Toegestane wijzigingen op het model (Jordi): losse vliegende onderdelen weg; gezicht apart (Claude tekent geen monden/ogen: bron nodig, overleg met Jordi).
- Open: wolkstaart loopt in het model tegen de rand; in de sprite moet hij binnen 64 px eindigen (Claude meldde "inkorten", Jordi maakte geen bezwaar).
