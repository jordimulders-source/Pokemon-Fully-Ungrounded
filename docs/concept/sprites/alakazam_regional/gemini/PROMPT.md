# Gemini-prompt: regionale Alakazam (charlatan), startprompt v1 (10 nov)

Regels: `docs/lessen/GEMINI.md`. Twee varianten, verder identiek, elk in een **nieuw gesprek**: A = twee toverstafjes, B = twee speelkaarten.

## Jordi (10 nov, letterlijk)
- "illusionisten/goochelaars, wat natuurlijk oplichters zijn. Deze lijn is er erg goed in, maar moet ook duidelijk geniepig zijn, veel meer dan de originele"
- "Ik zat eerst aan een toverstaf te denken, maar twee toverstafjes is een beetje raar, desondanks wil ik toch kijken hoe dat eruit ziet, plus een versie met speelkaarten."
- "Alakazam heeft een vrij iconisch ontwerp, dus dat motief blijven we aanhouden, alleen maken we er echt een charlatan van, de lange snor blijft, maar wel wat meer moustache twirling (zonder dat hij er zelf aan zit."
- "Ik wil een pose in drie kwart maar waar hij deels zijwaarts staat, met zijn voorkant naar de rechterkant van het scherm toe, dat is een vrij onbetrouwbare pose namelijk. Hij is skilled, maar gelijk als je hem ziet denk je hier klopt iets niet."
- "hij wordt donkerder, zwart/wit/grijs zou ik zeggen. De blik in de ogen wordt ook geniepig, ik zou zeggen 1 meer open en 1 half gesloten."
- "smoking uit eigen lijf goed. Violet tint op het hoofd ook prima. Rood misschien voor een soort stropdas of een soort kleur in zijn smoking bij dat zakje waar mensen soms een bloem in doen, maar misschien is dat te gimmicky."
- "1 hand toont hij naar ons toe, de ander houdt die achter zijn rug, daar zie je dan dat hij een kaart vast heeft ook/of toverstaf, perfecte pose is dat"
- "en die hand toont die dan nonchalant"
- Geen hoge hoed (advies Claude; Jordi twijfelde). Geen derde kaart, geen regionaal anker (Jordi).

## Bijlage
1. `bijlage1_alakazam.png`: de Gen 3-frontsprite van Alakazam (anatomie en motief).

## Nog open (Jordi kiest vóór het plakken; vul in op de plek van [...])
- Rood accent: [A red bow tie marking at the collar, part of its body like Rowlet's bow tie / A small red marking at the breast-pocket spot of the tuxedo / No red]. Advies Claude: strikje (uit het eigen lijf, zoals Rowlet); de zakbloem is een los voorwerp.

## Prompt (variant A: toverstafjes)

```
Design a regional form of Alakazam and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
A Dark/Psychic Alakazam that is a stage illusionist and a swindler: very skilled, but the moment you see it you feel something is not right. It must look much more sneaky and untrustworthy than the normal Alakazam. It is still clearly Alakazam (see the attachment): same body, same big head with the long ears swept back, same long mustache, same thin arms and legs, same shoulder pads, one object in each hand.

POSE
- Three-quarter view, but turned partly sideways: the FRONT of its body faces the RIGHT side of the image (the opposite of a normal front sprite). A shifty, untrustworthy stance.
- It has exactly two arms. One hand is held out toward the viewer, showing its object nonchalantly, casual and relaxed. The other hand is held behind its back, and the viewer can still see that this hidden hand holds the same object too.

FACE
- A sneaky look: one eye more open, the other eye half closed.
- The long mustache stays, with the tips curling upward on their own into a twirl, like a villain twirling his mustache, but its hands do NOT touch the mustache.

COLORS
- Black, white and grey instead of yellow and brown.
- A tuxedo made from its own body, not clothes: the chest and belly plates are white like a dress shirt; the big shoulder pads are black and stand up high like the collar of a magician's cape.
- A violet tint on the head.
- [RED ACCENT]

OBJECTS
- In each hand one magic wand, both exactly the same: a classic black wand with white tips. One in the shown hand, one in the hand behind its back, like Alakazam holds one spoon in each hand.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, rock, shadow, base, motion lines, glow, sparkles or effects. One single creature, no extra views.

AVOID
- No top hat, no cape, no cloth clothing, no gloves: the tuxedo is only the colors of its own body.
- Not a human magician, not a person in a costume. No plush toy, chibi or mascot look.
- No extra objects: exactly one wand in each hand, nothing else.
```

## Prompt (variant B: speelkaarten)
Gelijk aan variant A, alleen het blok OBJECTS en de laatste AVOID-regel vervangen door:

```
OBJECTS
- In each hand one playing card, and both cards are exactly the same card (the same suit and the same value), which a real deck never has. Held between the fingers: one in the shown hand, one in the hand behind its back, like Alakazam holds one spoon in each hand. Big, simple card faces that stay readable at 64x64.
```
```
- No extra objects: exactly one card in each hand, nothing else.
```

## Tips
- Bijsturen hooguit 1–2 keer met één zin, bijv. `same design, make the mustache tips curl more`.
- Rondes en Jordi's keuze vastleggen in `README.md` hier; gekozen ontwerp als `../referenties/gemini_gekozen_*.png`.
