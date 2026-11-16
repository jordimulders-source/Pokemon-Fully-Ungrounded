# Gemini-prompt: spooktrein fase 3 (Steel/Ghost), startprompt v1 (15 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Trein-/spooktrein-Pokémon).
Geen bijlage (eerste fase die we maken).

## Jordi (letterlijk)
- "bij het concept moet ik ook een beetje aan phantom express denken in cuphead, maar deze moet anders worden"
- "Hij gaat van puur steel naar steel ghost in fase 2 en 3."
- "hij wordt dan semi frontaal, dus je kijkt er iets frontaler dan driekwart op, waardoor de andere wagons dan erachter verdwijnen, maar we kunnen er ook een slimme vorm van maken waardoor je ze niet allemaal hoeft te zien"
- "eerst fase 3, daar heeft de spirit dus al een oude stoomtrein overgenomen, het moet duidelijk zijn dat deze in volle vaart is in de sprite"
- Fase 3 = de hele trein (locomotief met wagons): "exact".
- Spirit: "beetje rotom achtig, de locomotief heeft een gezicht waarin je kan zien dat het een geest is, en er zijn ook hints van geest op andere plekken"
- Vaart: "trein helt naar voren en de wielen zijn zoals in een stripboek mee aan het bewegen"
- Kleur: "idd roestbruine 1e fase, maar de 3e is alweer functioneel, dus hooguit tinten van roest"
- Geest: "en de geest heeft dan een mooie contrastkleur, misschien groenig?"
- Wagons: varianten a (verdwijnen achter de locomotief), b (lossen op in rook/spooknevel) en c (buigen in een bocht mee): "alle drie proberen, kijken wat gemini doet"

## Keuzes Claude (Jordi heeft hier niets over gezegd; schrappen of aanpassen mag)
- **Anders dan de Phantom Express:** geen schedel- of demonengezicht, geen spookconducteur of losse spookfiguren, geen cartoon/rubberhose-stijl.
- **Steel:** als textuur (oud ijzer, klinknagels), geen losse platen (GEMINI.md).
- Richting: naar links, zoals alle frontsprites.

## Prompt (basis; plak er één WAGONS-blok onder, per variant een nieuw gesprek)

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

TYPE: Steel / Ghost. Final stage of its line.

CONCEPT: an old steam train that has been taken over by a spirit, a bit like how Rotom possesses machines.
- The locomotive is the head: it has a face in which you can clearly see that it is a ghost (the spirit shows through the locomotive's front).
- There are also small hints of the ghost elsewhere on the train.
- The metal reads as old iron through texture (rivets, old iron), not as separate armour plates.
- The train is functional again, not a wreck: at most some tints of rust.
- The ghost has a nice contrasting color, greenish, against the iron of the train.

FULL SPEED (this must be obvious)
- The whole train leans forward, as if charging ahead at full speed.
- The wheels are drawn in motion like in a comic book.
- Show the speed with the train itself, not with effects around it.

VIEW
- Semi-frontal: slightly more frontal than a three-quarter view, facing left. The locomotive is in front and closest to the viewer.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature filling most of the canvas (final stage), compact silhouette that fits a square, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Plain white background. NO rails, floor, shadow, glow, speed lines, sparkles or effects outside the creature. One single creature, no extra views.

AVOID
- No skull or demon face on the locomotive, no ghost conductor or separate ghost characters riding the train.
- Not a cartoon / rubber-hose style, not a children's TV train with a friendly human face, not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

### WAGONS-blok variant a
```
WAGONS: there are wagons behind the locomotive, but because of the semi-frontal view they mostly disappear behind it; only a bit of them is visible.
```

### WAGONS-blok variant b
```
WAGONS: behind the locomotive the wagons dissolve into smoke and ghostly mist, so the back of the creature becomes a trail of smoke instead of a row of wagons.
```

### WAGONS-blok variant c
```
WAGONS: the wagons curve along behind the locomotive as if the train is taking a bend, so the silhouette stays compact and you don't need to see every wagon.
```

## Tips
- Rails of snelheidslijnen erbij: "NO rails, NO speed lines" bovenaan zetten, nieuw gesprek.
- Te breed (lange trein): "compact, fits a square 64x64 sprite" herhalen; variant c of b proberen.
- Niet bijsturen in hetzelfde gesprek na 1–2 keer (GEMINI.md): beste resultaat als bijlage in een nieuw gesprek.
