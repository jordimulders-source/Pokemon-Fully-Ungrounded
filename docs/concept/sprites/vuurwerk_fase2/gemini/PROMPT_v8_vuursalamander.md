# Gemini-prompt: vuurwerklijn fase 2, v8 (19 nov): kop, vuursalamander benadrukt

Nieuw gesprek. **Bijlage 1: een foto van een echte vuursalamander (*Salamandra salamandra*) van opzij/schuin, door Jordi te kiezen.** **Bijlage 2: `../../vuurwerk_fase1/af/vuurwerk_fase1_8x.png`** (fase 1, alleen voor stijl en kleur).

## Jordi
- Over r7: "ik vind ze eigenlijk alle 4 lelijk".
- "benadruk de vuursalamander nog wat meer in een nieuwe prompt".

## Keuzes Claude (open)
- Echte anatomie: brede, ronde, platte kop, korte ronde snuit, grote bolle zwarte ogen, duidelijke klierbulten (parotiden) achter de ogen, glanzende huid. GEMINI.md: echte soort + foto werkt het best.
- Halfgeloken oog en grijns uit v7 weggelaten (gaven een zelfvoldaan mensengezicht); een vuursalamander heeft grote ronde zwarte ogen. Zelfvertrouwen via de houding later. Wil Jordi het halfgeloken oog terug: regel "Optional" in de prompt gebruiken.
- Het gele vlekkenpatroon van de echte vuursalamander niet gevraagd (niet door Jordi genoemd).

## Prompt

```
Design only the HEAD of an original Pokémon, as official Gen 3 pixel art (Ruby/Sapphire/Emerald style). Draw FOUR variants side by side on one sheet. Only heads and a bit of neck, no bodies.

The Pokémon is a FIRE SALAMANDER (Salamandra salamandra, see the attached photo) whose body is made of fire. Its head must clearly be a real fire salamander's head, simplified into a Pokémon:
- broad, flat, rounded head, wider than it is tall
- short, blunt, rounded snout
- big, round, glossy black eyes that bulge out on the sides of the head
- two clearly swollen gland bulges (parotoid glands) right behind the eyes, the most typical feature of a fire salamander
- a wide, simple mouth line
- smooth, glossy skin

It is the middle stage of an evolution line; the second attachment is its first stage (a fire axolotl). Use that sprite only for the colors and the pixel style, not for the head shape.
- Colors: cream-white face, pink and red flames.
- Instead of gills: flames that sweep backward from the back of the head.
- Three-quarter view facing left. Not Charmander, no dragon, no lizard, no human expression.

Each head about 32x32 pixels, max 16 colors, 1 px dark outline, flat Gen 3 shading, no dithering, plain white background. No sparkles, no text.
```

Optional (halfgeloken oog terug): voeg toe onder "big, round, glossy black eyes": `- the upper eyelids slightly lowered, a calm, confident look`.
