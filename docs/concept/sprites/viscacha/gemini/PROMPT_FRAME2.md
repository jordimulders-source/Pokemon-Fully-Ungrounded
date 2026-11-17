# Gemini-prompt: viscacha, tweede pose (frame 2), 16 nov

Bijlage: `../referenties/gemini_gekozen_ronde6.png` (het gekozen model). Gemini moet dat beeld **bewerken**, niet opnieuw tekenen, anders lopen frame 1 en frame 2 uit elkaar.

## Prompt (Engels werkt het best)

> Edit the attached image. Keep this exact same creature: identical art style, colors, line work, proportions, size, camera angle and position on the canvas. Keep the same ears, eye, whiskers, yellow cheek tuft, yellow jagged tail tuft, fur colors and belly patch. Do not add anything new and do not redesign it.
>
> Change only the pose, as a second animation frame of a Pokémon battle sprite: the creature cries out with its mouth wide open, head tilted slightly upward, and its raised front paw lifted higher toward its chest; the other front paw pushes off the ground. The hind legs and feet stay planted exactly where they are. The tail swings a little further up.
>
> Plain white background, no ground, no shadow, no electricity effects, no text.

## Wat we daarna doen
- Alleen de kop met open bek, de voorpoten en de staart uit dit beeld overnemen; de rest blijft frame 1 (`af/viscacha.png`). Werkwijze in `../../frame2_studie/STUDIE.md`.
- Wijkt Gemini af van het model (andere oren, kleuren, staart): opnieuw genereren, niet laten repareren (README: "Gemini is slecht in verbeteringen maken").
- De pose in de prompt is een voorstel naar het patroon bij Game Freak (bek open en een voorpoot beweegt mee, zoals Raticate, Rattata en Patrat). Jordi kiest; pas de tweede alinea aan als je een andere beweging wilt.
