# Capykart (fase 2 van 2, Normal; evolutie van Capybarrel)
Lijnbesluiten: `docs/concept/IDEEEN.md` → "Capybarrel"; fase 1: `docs/concept/sprites/capybarrel/SPEC.md`. Prompts en rondes: `gemini/PROMPTS.md`.

## Vast (Jordi, letterlijk)
- Naam: **Capykart** (24 nov: "volgende, capykart, de evolutie van capybarrel").
- Type: puur Normal (23 nov: "normal plus niks").
- 23 nov: "wanneer die evolved, evolved het hout ook en wordt het een soort houten autotje, dus krijgt de capybara een soort van kart vorm waar delen van zijn lichaam uitsteken".
- 24 nov: "Dat is de fase 2 dus het hoofd is iets volgroeider en hij steekt uit een houten speelgoedwagentje, op de achterkant staan drie of vier toy blocks van hout opgestapeld".
- 24 nov (op r3): "ja het enige wat ik nog mis is een driehoekig toyblock op de bovenste"; "en de blauwe mag dezelfde vorm zijn als de andere twee"; "een groene driehoek erbovenop".
- 24 nov (op r2): "beter, alleen de toyblocks moeten opgestapeld, misschien leuk om de vorm iets meer een derby car te maken, of een van de andere foto's, dat het net wat natuurlijker is dat het hoofd zo eruit komt" (foto's in `referenties/`).
- 24 nov (op r1): "het moeten een houten speelgoedautotje zijn", "de toy blocks opgestapeld", "De capybara is de auto trouwens he. Zijn hoofd steekt er alleen uit, het autotje is zijn lichaam".
- 24 nov (op r4): "we kunnen de kleuren veranderen he"; op Claude's voorstellen "1 en 2 akkoord, 3 idd netjes laten overgaan, 4 is niet nodig imo" → gezicht + palet van Capybarrel (spritefase), hoepels terug, geen zitopening (netjes overgaan), niets van het lijf achterin.
- 24 nov, nog niet besloten: "Ik denk dat hij ook nog iets volgroeider moet lijken dan capybarrel, ... misschien maken we de capybara zelf een wat lichtere tint, meer richting beige en doen we de vorm van het hoofd net wat ronder, zodat die meer lijkt op een ventje in een toy car".

- 24 nov (op r5): "dit is als silhouet prima" → model `referenties/model_r5.png`, silhouet bevroren.

- 24 nov (op r3b): "nee beige werkt niet, het hoofd is nog wel iets teveel een kopie van capybarrel" → vacht B (dieper); kopvarianten V1–V3 (gezicht meer uit het model) in sprite/r4/.

- 24 nov: "v2 maar de tanden zijn teveel rechthoekjes, mogen ook net wat groter" → tanden uit Bibarel (T1; "t1"); blok: "wat het beste uitkomt" → blauwgrijs.
- **Frontsprite af (24 nov):** `af/capykart.png` = `eindkeuring/capykart_r7.png` (r6 + Dragonfly Cave-omlijning).

- 24 nov (op r7, "af"): "Je kan me niet vertellen dat deze door de eindkeuring is, weinig tint, vrijwel geen schaduw, vooral niet op de blokken, de lijnen op de auto, dit moet echt nog beter, dragonflycave" → schaduwrondes r8–r12.
- 24 nov (op r12): "het is nu niet echt een geheel meer, beetje blurry, de zwarte barrel lines zijn nog niet goed, de blokken staan niet echt in goed perspectief en lijken niet daadwerkelijk opgestapeld op de auto" → r13 (blokken mogen van vorm veranderen).

- 24 nov (op r15b): "ik vind niet dat mijn punten verwerkt zijn", "blokken kloppen niet, de lijnen van de capybara kloppen niet met gen 3 sprites, het kleurwerk in de auto is dramaitsch", "zoveel rechte lijnen nog", "het lijkt net alsof elke spritesessie eerst op dezeldfe manier fout moet gaan", "en de blokken kloppen niet qua kleuren waardoor ze volledig 2d lijken" → r16: auto + kop opnieuw uit de modelhelderheid; toren via een nieuw Gemini-model.

- 24 nov: "Waarom? je hebt ze nog geen enkele keer goed ingekleurd", "ik kan 20000 ontwerpen tonen maar als jij weigert ze goed in te kleuren", "nu zie ik het, de blokken zijn opnieuw getekend", "en helemaal niet overgenomen vanuit het model" → r17: hele sprite opnieuw volgens de Dundragoon-methode (kale reductie per materiaal uit model_r5, tinten uit de modelhelderheid), toren 100 % uit het model.

- 24 nov: "probeer maar zoveel mogelijk het model over te nemen, vergeet wat we eerder zeiden" → r17 = kale reductie van model_r5 met modeltonen, ook gezicht en toren; daarna: "behalve de speecifieke wijzigingen die we besproken hebben he", "tanden etc", "dan doen we daarna nog een laatste eindkeuring" ; "het Capybarrel-gezicht, de morrillo, de Bibarel-tanden — deze blijven" → die drie blijven; kleuren = modeltonen.

- 25 nov (op c): "het oog is heel raaar, de neus is effen ... oren zijn ook anders dan het model en grijze streep is ook weg", "de morrillo is anders dan je eerst deed toch? oog is nog steeds slecht, snuit nergens als in het model", "De tanden zitten ook helemaal niet meer vast aan de mond", "doe maar gewoon hetzelfde oog als capybarrel" → d = c + Capybarrel-oog exact (E3), tanden 2 rijen omhoog vast onder de snuit, philtrum donkerbruin (`eindkeuring_dc/capykart_d.png`, `kop_keuze/`).

## Open (niet door Jordi gezegd)
- Evolutiemethode/level.
