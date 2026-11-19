# Opdracht maker v2: Llamauler frontsprite naar het samengestelde model (19 nov)

Vervangt `OPDRACHT.md` (r1 is afgekeurd, r2 gestopt). Jordi letterlijk en het verloop: `OPDRACHT.md` en `../gemini/PROMPT.md`.

## Jordi (19 nov, letterlijk, nieuw)
- "pardon waarom gebruik je niet het model met handschoenen?" · "ja van r3"
- "de voorste poot is ook veel dikker dan de rest"
- Over Gemini r3: "dit is je referentie voor de voorpoten, maar ook voor de grootte van de achterpoten"
- Over r1: "daarnaast lijkt de sprite nog volledig 2d, leer van wat de palpaca agent (quirky brown) zojuist heeft gedaan"

## Model (bevroren)
`../gemini/poten/model_v3.png` (1024², script `../gemini/poten/model_v3.py`): lijf, kop, hals, wol, kleding, staart = Gemini r4; voorpoten met handschoenen = Gemini r3 (vanaf y 815); achterpoten = r12 (telgang), verbreed tot de breedte van de r3-achterpoten. De pootstand (telgang) en de handschoenen staan nu in het model; alles komt uit het model.

## Wat bij Palpaca werkte (Jordi: "ja de hele sprite is echt veel beter nu"; `origin/claude/quirky-brown-j1w8uv`, `docs/concept/sprites/alpaca/sprite/r4/NOTITIES.md` + `scripts/bouw_r4.py`, `px.py`)
Lees die met `git show origin/claude/quirky-brown-j1w8uv:<pad>`. Kern:
1. **Palet gemeten in het model** (natief raster, mediaan per zone/helderheidsband): wol in 4 tonen, zachte modellijn + donkerste modellijn, verre poten eigen tonen, handschoen, kleed, halsband, pompons. ≤16 kleuren incl. transparant.
2. **Binnenkant uit het model:** elke binnenpixel krijgt de toon van het model op die plek (helderheidsbanden → toonindex; donker genoeg → binnenlijn). Zo komen de wolbollen, binnenlijnen, schaduwkanten en het perspectief (volume, 3/4) uit het model en is de sprite niet plat. Jordi bij Palpaca: "Je mag echt veel meer het model gaan namaken" · "het gaat vooral om perspectief".
3. **Silhouet = model verkleind** (alpha ≥ ±0,45, niet gladstrijken): de wolbogen in de omtrek blijven als schulpen.
4. **Handwerk** alleen waar de reductie ruis geeft (oog, neus, mond, kwastjes, pompons), steeds naar het model.

## Formaat en vaste punten
- ±62 px hoog (oren t/m voeten), onderaan in 64×64, ongeveer gecentreerd; ≤16 kleuren, index 0 transparant.
- Gezicht: droog oog met zwaar vlak ooglid, platte mond (uit het model).
- Halsband: strepen ±1 px, pompons als stipjes met donkere rand.
- Verre poten donkerder dan nabije (zoals in het model).

## Lees eerst
`docs/lessen/SPRITE_KERN.md`, `docs/lessen/GEMINI.md`, `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken". Gereedschap: `docs/concept/sprites/octillery_evo/sprite3/natief.py`, `docs/concept/sprites/poedelmot/kleur_r19/stappen/px.py`, `kleur_r20/stappen/box1x.py`, en de Palpaca-scripts hierboven. Je mag ook kijken naar `sprite/r1/scripts/` (vorige maker), maar r1 zelf is afgekeurd (plat, gladde omtrek, lijntjespoten, effen kleed).

## Lever
`sprite/r3/`: `lama.png`, `normal.pal`, scripts, `NOTITIES.md` (palet met gemeten waarden, per zone px afwijkend van de modeltonen, zwakke punten), `vel.png` (model | r3 | r1 op dezelfde hoogte 8×; close-ups kop, lijf en poten 12× naast het model op spriteraster; 1× en 2× op licht en donker). Zelfgenoemd zwak punt eerst zelf repareren. Geen git commit/push.
