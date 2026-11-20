# Hoatzin fase 2: Gemini-prompt v7 (19 nov)

Op v6 r1, Jordi: "laten we een beetje zuur uit de mond lopen? Zoals bij gloom? Ja wat paars tinten, maar dan wel een paars tint die goed past bij het roestachtige bruin, verder misschien op het rode oog en blauwe gezicht na de kleuren zo doen dat het er dark/poison uit ziet, maar niet vloekt".
Nieuw gesprek; bijlage: v6_r1.

```
Attached: a Pokémon sprite (hoatzin-based, Poison/Dark type).
Keep every shape, outline and pixel position exactly the same: same pose, wings, crest, face, tail and feet. Make only these changes:
1. Add a little acid drooling from the beak, like Gloom's drool: a short drip hanging from the tip of the beak.
2. Recolor the bird so it looks Dark/Poison type without clashing colors:
   - Keep the bare BLUE face and the RED eye with black pupil exactly as they are.
   - Use purple tones that go well with the rusty brown of the wings (warm purples, not a bright magenta).
   - The belly is one shade lighter purple than now.
   - Everything works together as one harmonious, dark and poisonous palette.
Official Gen 3 front sprite pixel art, max 16 colors, white background, no other changes.
```

Uitslag v7 r1 (`v7_r1.webp`), Jordi: "beter, maar het acid is net iets teveel, 1 druppel is genoeg. De vleugels zijn twee verschillende kleuren, de achterste vleugel mag hetzelfde als de voorste vleugel, dan vind ik hem prima, ondanks dat het niet klopt met mijn eerdere suggestie".
Bijsturen (zelfde gesprek, of nieuw gesprek met v7_r1):
```
Keep this sprite exactly as it is. Make only these two changes:
1. The acid at the beak: make it just ONE single drop hanging from the tip of the beak.
2. The back wing (the dark purple feathers behind the head) gets exactly the same rusty brown colors and pale streaks as the front wing.
Everything else stays pixel for pixel the same, including the crest, face, body, belly, tail and feet.
```

Jordi daarna: "of misschien de vleugels 1 tint meer richting paars, bruinpaars weet niet of dat bestaat". Variant bijsturing:
```
Keep this sprite exactly as it is. Make only these changes:
1. The acid at the beak: make it just ONE single drop hanging from the tip of the beak.
2. Both wings (the front wing and the back wing behind the head) get the same color: the current rusty brown shifted one shade toward purple, a plum brown / purple-brown, with the same pale streaks.
Everything else stays pixel for pixel the same, including the crest, face, body, belly, tail and feet.
```

Uitslag v7 r2 (`v7_r2.webp`, bruinpaarse vleugels, 1 druppel), Jordi: "de druppel moet wel aan de zijkant van de mond komen, dus een beetje eroverheen lopen. De buik vind ik nog een beetje vloeken, kan die misschien 1 tint meer richting de rest van het lichaam?"
```
Keep this sprite exactly as it is. Make only these two changes:
1. The acid drop comes from the SIDE of the mouth (the corner where the upper and lower beak meet), running a little over the edge of the beak before it hangs down as one drop.
2. The purple belly: shift its color one shade toward the colors of the rest of the body, so it clashes less.
Everything else stays pixel for pixel the same.
```

Jordi: "en ik ben nu weer bang dat de kuif teveel wegvalt, dus die weer meer bruin?" Prompt met 3 wijzigingen:
```
Keep this sprite exactly as it is. Make only these three changes:
1. The acid drop comes from the SIDE of the mouth (the corner where the upper and lower beak meet), running a little over the edge of the beak before it hangs down as one drop.
2. The purple belly: shift its color one shade toward the colors of the rest of the body, so it clashes less.
3. The thin crest strands on the head: make them rufous orange-brown again (like a real hoatzin's crest), so they stand out against the wings behind them. Keep their shape.
Everything else stays pixel for pixel the same.
```

Uitslag v7 r3 (`v7_r3.webp`), Jordi: "de kuif en buik zijn goed, maar de top van de vleugel is nu verknald en het slijm gaat helemaal fout". (Achterste vleugeltoppen werden kuifbruin; slijm loopt als groene lijn langs de snavel.)
Ronde A (1 wijziging; bijlagen: v7_r3 + v7_r2 als voorbeeld van de vleugel):
```
Attached: (1) the current sprite, (2) an earlier version.
Keep sprite (1) exactly as it is. Change only one thing: the tops of the back wing behind the head have become orange-brown by mistake. Give those wing feathers the same plum-brown color as the rest of the wings, like in image (2). The thin orange crest strands in front of them stay orange. Everything else stays pixel for pixel the same.
```
Ronde B (daarna, 1 wijziging):
```
Keep this sprite exactly as it is. Change only the acid: remove the green line along the beak. Instead, one single small acid drop sits at the corner of the mouth (where the beak meets the blue face) and hangs down from there. Everything else stays pixel for pixel the same.
```

Jordi: "al zou ik de kuif wat bruiner willen en de buik iets lichter, zodat het opvalt". Ronde C (na A en B):
```
Keep this sprite exactly as it is. Change only two colors:
1. The thin crest strands on the head: a bit more brown (less orange).
2. The belly: a bit lighter, so it stands out from the rest of the body.
Everything else stays pixel for pixel the same.
```

Jordi: "dit werkt niet, zet de 3 dingen samen in een prompt, zonder extra referentiemateriaal en ik start een nieuw gesprek". Bijlage alleen v7_r3:
```
Attached: a Pokémon sprite. Keep it exactly as it is (pose, shapes, outlines, face, eye, tail, feet). Make only these changes:
1. Back wing: the tops of the wing feathers behind the head are orange-brown by mistake. Give them the same plum-brown color as the rest of the wings. The thin crest strands in front of them stay separate.
2. Acid: remove the green line along the beak. Instead, one single small acid drop sits at the corner of the mouth (where the beak meets the blue face) and hangs down from there.
3. Colors: the thin crest strands a bit more brown (less orange); the belly a bit lighter, so it stands out from the rest of the body.
Everything else stays pixel for pixel the same. Official Gen 3 front sprite pixel art, white background.
```

Uitslag v7 r4 (`v7_r4.webp`; vleugel en kuif opgelost), Jordi: "het slijm snapt die niet".
Voorstel: eerst slijm weg, dan Jordi zet zelf een groene stip waar de druppel moet komen en Gemini maakt er een druppel van.
Stap 1:
```
Keep this sprite exactly as it is. Change only one thing: remove all the green acid, so the beak is clean. Everything else stays pixel for pixel the same.
```
Stap 2 (bijlage: resultaat met een groene stip/streep van Jordi):
```
Keep this sprite exactly as it is. I drew a rough green mark where an acid drop should be. Turn ONLY that mark into one small, clean pixel-art acid drop in exactly that spot and that size. Everything else stays pixel for pixel the same.
```

Uitslag v7 r5 (`v7_r5.webp`, stap 1 slijm weg), Jordi: "dit is niet de juiste bek?" Gemini tekende een nieuwe snavel (lichtgrijs, langer, recht, zonder donkere omlijning) en het plaatje werd zachter. Opnieuw vanaf v7_r4, nieuw gesprek:
```
Keep this sprite exactly as it is. Change only one thing: remove the green acid line and drop, so the beak is clean. The beak itself must stay exactly the same: short, thick, dark grey, slightly hooked, with its dark outline. Do not redraw or recolor anything else; keep the pixels as sharp as they are.
```

v7 r6 (`v7_r6.webp`): Gemini tekende een roofvogelsnavel; Jordi: "hij is het kwijt", "heb je de snavel nog van voor het slijm? plak die erop".
`v7_r4_snavel.png`: v7_r4 met de snavel van v6_r1 pixel voor pixel erop geplakt (alleen grijze snavel/omlijning/witte achtergrond in het snavelvak; slijm daarmee weg; rest onaangeroerd). Jordi: de resolutie wordt per Gemini-ronde slechter.

Jordi: "nee we doen gewoon een prompt waar hij deze opnieuw tekent en netter maakt en de buik weer een tint paarser maakt, geef een kleurcode mee". Buik nu ±#946869 (licht #A77881, schaduw #82595B); een tint paarser: #8E6280 (licht #A57A98, schaduw #7A5270). Bijlage: v7_r4_snavel.png.
```
Attached: a Pokémon sprite. Redraw it as a clean, sharp official Gen 3 front sprite (Ruby/Sapphire/Emerald style): crisp pixels, clean dark outlines, flat color areas with simple shading, no blur or soft edges, max 16 colors, white background.
Keep the design exactly the same: same pose, wings, crest, blue face, red eye, beak, body, tail, feet and all colors.
Only one color change: the belly becomes one shade more purple: main color #8E6280, highlight #A57A98, shadow #7A5270.
No acid, no effects, nothing added.
```

Uitslag hertekenen (`v8_r1.png`: vleugelstrepen weg, alles één mauve), Jordi: "dit is nog slechter he? Misschien met de vorige maar gaan bouwen en tijdens het spriten aan de kleur werken".
**Model bevroren: `../MODEL.png` (= v7_r4_snavel.png).** Buikkleur (richting #8E6280) en eventueel de zuurdruppel in de spritefase.
