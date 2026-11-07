# Sprites vanaf een Gemini-ontwerp (Jordi, 7 nov: "pas de regels maar aan voor gemini modellen die sprites gemaakt worden")

Wanneer Jordi een ontwerp in Gemini laat maken en kiest, gelden deze regels **in plaats van** stap 1–3 van `SPRITE_KERN.md` (ontwerp, bron, silhouet). De rest van SPRITE_KERN (netheid, belijning, ogen, keurslot) blijft gelden.

## Ontwerp in Gemini
- Claude schrijft de prompt (Engels); Jordi plakt hem in Gemini en stuurt het resultaat. Voorbeeld en rondes: `docs/concept/sprites/viscacha/gemini/README.md`.
- Vast in elke prompt: echte diersoort als anatomie (foto meesturen), "official Gen 5 front sprite", 3/4 naar links, geen elektriciteit/gloed/effecten, **geen rots/ondergrond/schaduw**, witte achtergrond, ≤16 kleuren, 64×64, een AVOID-regel (Neopets/knuffel, konijn, enz.).
- **Gemini is slecht in verbeteren:** korte bijstuurfeedback werkt hooguit 1–2 keer; daarna drijft hij af (viscacha werd Raichu). Beter: de beste versie als bijlage in een **nieuw gesprek** met een nieuwe startprompt.
- "Meer Pokémon"/"cuter" laat Gemini naar bekende soorten glijden (Pikachu/Raichu); noem expliciet wat níet mag lijken.
- Jordi's keuze = **bevroren ontwerp**: pose, verhoudingen (kopgrootte, oren), kenmerken en kleuren. Opslaan als `referenties/gemini_gekozen_*.png`, feedback per ronde in `gemini/README.md`, Jordi letterlijk in SPEC.

## Van Gemini-plaatje naar sprite
- De sprite is een **vertaling** van het Gemini-plaatje naar 64×64, geen nieuw ontwerp. Silhouet = masker van het plaatje verkleind (massa heilig), kleuren = de Gemini-kleuren.
- Kwantiseren naar het palet mag als **onderlaag** (Gemini-plaatjes zijn al pixelachtig); daarna met de hand opschonen volgens SPRITE_KERN (tinten, sikkelschaduw, selout, ogen van een echte sprite). Geen kale scriptuitvoer opleveren.
- Afwijken van Gemini alleen waar iets op 1× anders leest dan in het plaatje (een vlak dat op 64 px als kraag leest, losse haren, effectjes); meld elke afwijking.

## Keuren
- De keurder toetst **trouw aan het Gemini-plaatje + spritetechniek**, niet het ontwerp. Ontwerppunten (kop klein, oren smal, minder cute) zijn géén FAIL en geen reparatie; hooguit "voor Jordi".
- Vergelijk op 8× naast het Gemini-plaatje (verkleind) én 2–3 echte sprites.
- De regel "na 2 mislukte rondes stoppen" telt hier alleen bij ontwerp- of vertaalproblemen; rondes met alleen benoemde pixelreparaties (contour, toonvlakken) gaan door, doel ≤ 5.

## Lessen
- **Gezicht apart vergelijken** (viscacha r4, 7 nov: Jordi "kijk eens goed naar het gezicht ... neus, whiskers, mond"; twee keurders en Claude misten het): maak altijd een close-up van de kop van sprite en Gemini op dezelfde schaal naast elkaar en vink per onderdeel af: neus, mond, snuitvorm, kin, snorharen, oog, oren. Snorharen uit Gemini niet weglaten: 1 px lijntjes zoals Raticate/Sandshrew.
