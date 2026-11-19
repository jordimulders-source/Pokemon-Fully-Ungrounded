# Opdracht maker: Hummlet (kolibrie fase 1) frontsprite naar Gemini r5 (19 nov)

## Jordi (19 nov, letterlijk)
- "hummlet is net niet genoeg een hummingbird chick, maar heb ik toen maar opgegeven zodat we resultaat konden boeken."
- Keuzes: wat mist: "wat betreft vraag 1 alles, maar wat wel goed vertaalt naar een sprite"; snavel "Langer en dun, dicht"; kleuren "Ja, kleuren blijven"; pose "Bolletje zoals foto 5".
- Aanvulling (19 nov): "de kleur van het model mag afwijken omdat je het kleurpalet van het origineel mag gebruiken, dat was het enige aan de originele sprite dat ik zeer goed vond. Ik ben het eens met je dat die klein moet blijven, 40px breed mag je proberen" → totale breedte **40 px**.
- Bij de keuze van r5: "ja, ik denk dat we perspectief toch vooral creëren door slim kleur en schaduwgebruik" · naast het origineel: "ja echt veel beter, ga maar bouwen" · "op alle fronten".

## Model (bevroren ontwerp)
`../referenties/gemini_gekozen_r5.png` (1024², pixelachtig Gemini-plaatje). Vorm, pose, onderdelen, oog, snavel, spikkels, vleugel, staart en pootjes komen uit dit model.

## MODEL OVERNEMEN, NOOIT HERTEKENEN (SPRITE_KERN, letterlijk mee te geven)
Bij een model (Gemini of ander) is de sprite de **verkleining van het model zelf**: natief raster terughalen → verkleinen met vlakgemiddelde + dichtstbijzijnde kleur uit het model → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten) en per pixel repareren wat de reductie kapotmaakt (oog, neus, tanden), steeds naar het model. Gezicht, vlakken, schaduw en poten komen uit het model, niet uit de hand van de maker. Een toegestane afwijking van Jordi komt als laatste, als bovenlaag. De maker meldt per zone hoeveel pixels afwijken van de kale reductie. **Kleur mag altijd afwijken van het model** (Jordi, 17 nov): vorm/silhouet/onderdelen uit het model, kleur, schaduw en volume naar Gen 3 en de keuringen.

## Toegestane afwijkingen (bovenlaag, na de onderlaag)
1. **Formaat (voorstel Claude, door Jordi niet afgewezen, "ga maar bouwen"):** pre-evo blijft klein, rond de maat van de oude sprite: totale breedte incl. snavel ±42 px (40–44), hoogte volgt uit het model. Op 64×64, onderaan geplaatst zoals andere Gen 3-sprites (pootjes ±onderste rij 56–60), horizontaal ongeveer gecentreerd.
2. **Kleuren = het oude palet** ("kleuren blijven"): `../af/normal.pal` / `../af/kolibrie_pre.png` (lila/grijsviolet lijf, lichte lavendelwitte buik, donkerder blauwviolette vleugel, oranje pootjes, gele mondhoek, donkere omlijning #140E1E). Map de modelzones op deze tinten; het model is fletser/grijzer.
3. **Licht en schaduw naar Gen 3** (Jordi: "perspectief ... door slim kleur en schaduwgebruik"): licht linksboven, sikkelschaduw die de ronde vormen volgt (onder de buik, onder de kop/kin, achter op het lijf, verre kant), hooglicht linksboven op kop en borst; stappen ±30–40 helderheid zoals Taillow; gekleurde selout aan de lichtkant, donker aan de schaduwkant. Vorm/silhouet blijft van het model.
4. **Oog:** neem het oog uit het model; leest het na de reductie niet, dan het Starly-oog van de oude sprite (`../af/kolibrie_pre.png`, zwart met witte glans, geen iris) pixel voor pixel.
5. **Pootjes:** in perspectief (verre poot iets hoger en verder naar achter), klein, omlijnd (SPRITE_KERN). Verder uit het model.
6. Spikkels: alleen enkele duidelijke pixels op de modelplekken, geen ruis/dambord.

## Werkwijze
- Lees eerst: `docs/lessen/SPRITE_KERN.md`, `docs/lessen/GEMINI.md` (vooral Krassault/Abra/sneeuwbolslak: natief raster, reductie), `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken".
- Gereedschap om te hergebruiken: `../../octillery_evo/sprite3/natief.py` (natief raster), `../../poedelmot/kleur_r20/stappen/px.py`, `box1x.py`, `lijnkaart.py`.
- Gen 3-vergelijking: `graphics/pokemon/taillow`, `starly`, `swablu`, `fletchling`; Dragonfly Cave: `docs/lessen/SPRITING.md` + `docs/lessen/bronnen/`.
- Werk in `sprite/r1/` (dan r2, ...): `onderlaag.png` (kale reductie), `hummlet.png` (64×64, geïndexeerd, ≤16 kleuren, index 0 transparant), `normal.pal`, scripts, `NOTITIES.md` (per zone aantal px afwijkend van de onderlaag, zelfgenoemde zwakke punten), `vel.png` (sprite 8× | model verkleind op dezelfde schaal 8× | oude sprite 8× | Taillow/Starly 8× | 1× op licht en donker | close-up kop 12× naast model).
- Zelfgenoemd zwak punt = eerst zelf repareren. Niets naar Jordi; Claude bekijkt het vel.
- Geen git commit/push (doet Claude).
