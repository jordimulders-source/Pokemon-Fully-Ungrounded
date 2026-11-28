# Proefserie overige graphics (27 nov): Gumfish, Sunperor, Hexpress

Doel (Jordi, 27 nov): "ik wil onderzoeken hoe we dit met zo weinig mogelijk werk kunnen doen". Gemini via de app (Jordi), geen API.
Proefsoorten naast Zapacha (viervoeter): Gumfish (bol, geen poten), Sunperor (vogel, rechtop), Hexpress (object + geest). Gengas niet (Jordi: "daar hebben we al frame 2 voor").

## Wat we testen
- **Eén vast sjabloon per onderdeel**, per soort alleen de regel "Body plan". Werkt dat, dan kost een pakket voor een hele batch bijna niets.
- Elke prompt in een **nieuw gesprek**, met alleen de bijlage `<soort>_front_8x.png` uit deze map (geen voorbeeldsoort: bij de viscacha liep Raticate erin door).
- Niet laten bijsturen in hetzelfde gesprek (Gemini tekent dan alles opnieuw); bij een fout: nieuwe poging in een nieuw gesprek.
- Graag per prompt **2 pogingen** (twee nieuwe gesprekken), zodat je kunt kiezen. Opslaan als `<soort>_rug_p1.png`, `_p2.png`, `<soort>_frame2_p1.png` enz. in deze map.

## Frame 2: wie doet wat (indeling `frame2_studie/STUDIE.md` §12)
| Soort | Soort beweging | Wie |
|---|---|---|
| Gumfish | hele figuur (bol) | script, Claude |
| Sunperor | lokale pose | **Gemini** (prompt hieronder) |
| Hexpress | losse delen (geest, wolken) in tegenbeweging | script, Claude |

De overworld volgt pas als de rug er is (de prompt heeft front + rug als bijlage nodig).

---

## Sjabloon rug (per soort alleen "Body plan" anders)
> This is a Pokémon battle sprite of my creature, seen from the front. Draw its back sprite, the way Pokémon Ruby/Sapphire/Emerald draw the player's own Pokémon in battle.
>
> Viewpoint: seen from behind and slightly above on the left. The creature faces away from the viewer, toward the upper right. Zoomed in: the creature is a bit larger than in my image and the bottom is cut off by a straight horizontal line, with nothing below it.
>
> Body plan (keep it): <BODY PLAN>
>
> Keep my creature exactly as it is: same colors, same art style and dark outline, same proportions. Do not add anything new and do not redesign it.
>
> Gen 3 pixel art, plain white background, no ground, no shadow, no effects, no text.

### Gumfish: bijlage `gumfish_front_8x.png`
Body plan: `a round, soft fish lying flat on the sea floor, no legs; we see its back and the tail fin; the face is turned in profile at the right side so one eye and the lips are visible.`

### Sunperor: bijlage `sunperor_front_8x.png`
Body plan: `a large upright bird standing on two legs; we see its dark brown back and the back of the big red-orange fan crest; the head is turned in profile over its shoulder at the right side so one eye and the hooked beak are visible; the golden staff is held in the wing.`

### Hexpress: bijlage `hexpress_front_8x.png`
Body plan: `a rusty scrap locomotive held together by a green ghost; we see the rear and the side of the locomotive, the green ghost on top seen from behind, the green ghost wheels and green clouds trailing behind.`

---

## Frame 2 (alleen Sunperor): bijlage `sunperor_front_8x.png`
> Edit the attached image. Keep this exact same creature: identical art style, colors, line work, proportions, size, camera angle and position on the canvas. Do not add anything new and do not redesign it.
>
> Change only the pose, as a second animation frame of a Pokémon battle sprite: <POSE>. The feet stay planted exactly where they are.
>
> Plain white background, no ground, no shadow, no effects, no text.

Pose (voorstel Claude, patroon bij Game Freak: bek open + één lichaamsdeel beweegt mee; Jordi kiest of past aan):
`it cries out with its beak open, the raised wing lifted a bit higher and the fan crest spread a little wider`

## Hexpress rug: p2 en p3 (27 nov)
- p2 (prompt met "locomotive", AVOID-regel) → `hexpress_rug_p2.png`: gewone trein met cabine en ramen; Jordi: "nog minder, is je prompt goed genoeg? het is een mooi ontwerp verder wel, maar niet wat we nodig hebben".
- Les: het woord "locomotive/train" laat Gemini een gewone trein tekenen; van recht achteren verdwijnt het herkenningsteken (gezicht met mond); niet vragen om delen die niet in de front staan.
- p3-prompt (in de chat gegeven): zonder het woord trein, het wezen omgedraaid dat over zijn schouder terugkijkt (deel van het gezicht met de mond zichtbaar), alleen onderdelen uit de front, "no new parts, windows, doors, cabins or rails".

## Sunperor icoon via Gemini (27 nov)
Jordi: "misschien kunnen we met complexere ontwerpen wel nog gemini vragen, laten we het met sunperor proberen, want daar zie ik jou geen fatsoenlijk icoon van maken"; "Sunperor gaat al fout omdat die niet driekwart staat maar frontaal". Prompt in de chat gegeven (alleen front-bijlage, bouw in woorden, driekwart, AVOID-regel; lessen viscacha-icoon r1 en overworld r2).

## Rugsjabloon v2 (28 nov, getest op Bandolingo: geslaagd)
Na vergelijking met 12 Gen 3-ruggen (`pakketten/batch_01/af/ruggen_vs_gen3.png`): close-up van het bovenlijf van achteren/boven, geen poten. Resultaat `pakketten/batch_01/af/bandolingo_v2_vergelijk.png` (oud | v2 | Raticate).
> This is a Pokémon battle sprite of my creature, seen from the front. Draw its back sprite, the way Pokémon Ruby/Sapphire/Emerald draw the player's own Pokémon in battle.
>
> Viewpoint: a CLOSE-UP seen from behind and slightly above, like looking over the creature's back. We see only the UPPER BODY: the back of the head, the shoulders, the back and the tail. The legs are NOT visible: the body is cut off by a straight horizontal line just below the back. The head is at the upper right, turned in profile so one eye and <kenmerk gezicht> are visible. The creature fills most of the square.
>
> Body plan (keep it): <kort, alleen wat in de front staat>
>
> Keep my creature exactly as it is: same colors, same art style and dark outline, same proportions. Do not add anything new and do not redesign it.
>
> AVOID: a side view of the whole animal, visible legs or feet, a walking pose.
>
> Gen 3 pixel art, plain white background, no ground, no shadow, no effects, no text.
- **v2 afgekeurd** (Jordi, 28 nov: "want bij deze klopt het perspectief niet meer" · "de staart zit bijna onder de schouder"). Jordi's vraag: "als gemini gewoon het hele achterlichaam stuurt op een specifieke grootte dan kan jij het toch netjes afknippen?" → ja, als het beeld genoeg pixels heeft (Llamauler op 10,7 px wel, de 16-px-beelden niet). Test v1-sjabloon met de front op 4× op een wit vlak van 1024 (`batch_01/bandolingo_front_4x_canvas.png`), zodat Gemini op een fijner raster tekent.
- 4×-bijlagetest (28 nov): Gemini tekent toch weer op 16 px (Bandolingo 43×46). Het beeld is altijd ±64 hokjes; groter = het dier het hele beeld laten vullen ("fills the whole image from edge to edge, lower legs cut off by the bottom edge").
