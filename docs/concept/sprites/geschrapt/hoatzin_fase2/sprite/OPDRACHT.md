# Opdracht maker: hoatzin fase 2 frontsprite naar het model (19 nov)

Lees eerst `../SPEC.md` (Jordi letterlijk).

## Model (bevroren ontwerp)
`../MODEL.png` (1024², pixelachtig Gemini-plaatje, wat zacht door meerdere bewerkingsrondes). Pose (vleugels hoog gespreid), kuif, gezicht, snavel, vleugeltekening, lijf, staart en poten komen uit dit model.

## MODEL OVERNEMEN, NOOIT HERTEKENEN (SPRITE_KERN, letterlijk)
Bij een model (Gemini of ander) is de sprite de **verkleining van het model zelf**: natief raster terughalen → verkleinen met vlakgemiddelde + dichtstbijzijnde kleur uit het model → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten) en per pixel repareren wat de reductie kapotmaakt (oog, neus, tanden), steeds naar het model. Gezicht, vlakken, schaduw en poten komen uit het model, niet uit de hand van de maker. Een toegestane afwijking van Jordi komt als laatste, als bovenlaag. De maker meldt per zone hoeveel pixels afwijken van de kale reductie. **Kleur mag altijd afwijken van het model** (Jordi, 17 nov): vorm/silhouet/onderdelen uit het model, kleur, schaduw en volume naar Gen 3 en de keuringen.

## Toegestane afwijkingen (bovenlaag, na de onderlaag)
1. **Formaat:** eindvorm; past in 64×64, zo groot mogelijk (hoogte ±62–63 px, breedte volgt uit het model), onderaan geplaatst zoals Gen 3 (tenen op de onderste rijen), horizontaal gecentreerd.
2. **Buik** (Jordi: "een tint paarser"): richting #8E6280, licht #A57A98, schaduw #7A5270 (nu ±#946869). Opvallen tegen het lijf, niet vloeken. Overige kleuren uit het model; mogen naar Gen 3 bijgesteld worden (contrast, ≤3 tinten per groep), niet van tint veranderen.
3. **Licht en schaduw naar Gen 3:** licht linksboven, sikkelschaduw die de vorm volgt, stappen ±30–40 helderheid; zwart alleen aan de schaduwkant, gekleurde selout aan de lichtkant. Vorm blijft van het model.
4. **Oog:** rood met zwart puntje (geen oogwit), uit het model; leest het na de reductie niet, dan per pixel repareren naar het model (glanspixel mag).
5. **Kuif:** dunne bruine veren uit het model; ≥ 1 px per streng, geen ruis. Dunne delen niet laten wegvallen tegen de pruimbruine vleugel erachter (kleurcontrast, geen vormwijziging).
6. **Vleugelstrepen** (lichte streepjes): minder/grotere op de modelplekken als ze een raster/zebra worden.
7. Geen zuur/slijm.

## Werkwijze
- Lees eerst: `docs/lessen/SPRITE_KERN.md`, `docs/lessen/GEMINI.md` (Krassault/Abra/sneeuwbolslak/Hummlet: natief raster, reductie), `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken".
- Native rasterpitch van de Gemini-reeks is ±10,25 px (offset ±−1,75); controleer zelf met `docs/concept/sprites/octillery_evo/sprite3/natief.py`.
- Gereedschap om te hergebruiken: `octillery_evo/sprite3/natief.py`, `half2.py`; `poedelmot/silhouet/sil.py`; `poedelmot/kleur_r19/stappen/px.py`, `poedelmot/kleur_r20/stappen/box1x.py`; voorbeeld van een complete ronde: `kolibrie_pre/sprite/` (Hummlet, zelfde werkwijze).
- Gen 3-vergelijking: `graphics/pokemon/` `pidgeot`, `skarmory`, `swellow`, `murkrow`, `xatu`; Dragonfly Cave: `docs/lessen/SPRITING.md` + `docs/lessen/bronnen/`.
- Werk in `sprite/r1/` (dan r2, ...): `onderlaag.png` (kale reductie), `hoatzin.png` (64×64, geïndexeerd, ≤16 kleuren, index 0 transparant), `normal.pal`, scripts, `NOTITIES.md` (per zone aantal px afwijkend van de onderlaag, zelfgenoemde zwakke punten), `vel.png` (sprite 8× | model verkleind op dezelfde schaal 8× | Pidgeot/Swellow 8× | 1× op licht en donker | close-up kop 12× naast model).
- Zelfgenoemd zwak punt = eerst zelf repareren. Niets naar Jordi; Claude bekijkt het vel.
- Geen git commit/push (doet Claude).
