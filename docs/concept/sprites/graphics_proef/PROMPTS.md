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
