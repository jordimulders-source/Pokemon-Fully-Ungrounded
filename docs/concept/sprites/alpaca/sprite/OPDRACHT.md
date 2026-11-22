# Opdracht maker: Palpaca (alpaca, Fighting-starter fase 1) frontsprite naar het nieuwe model (19 nov)

## Jordi (19 nov, letterlijk)
- "palpaca heeft bijv nog steeds een beetje een gek aangezicht, daar gaat het mij vooral om"
- "Belangrijk hierin is dat de sprite moet zijn zoals een alpaca in het echt loopt, dat is anders dan een paard doet toch? Het design moet zo blijven alleen de pose moet natuurlijker, de hoek moet natuurlijker, hij moet netter"
- "nee hij moet een cute starter zijn"
- Bij het model: "hier kunnen we mee vooruit denk ik?"

## Model (bevroren)
`../model/model.png` (1024², Gemini r11: r4 + achterpoten van r10, naad door Gemini gladgemaakt). Pose, hoek, gezicht, alle vier de poten (telgang: nabije voorpoot met handschoen geheven, nabije achterpoot licht en naar voren onder de buik, verre achterpoot donkerder en naar achteren), kraag, oorkwastjes, staart: alles uit dit model. De gang is het hele punt van deze opknapbeurt: de pootposities en welke poot voor/achter zit (licht/donker, overlap) moeten exact blijven.

## MODEL OVERNEMEN, NOOIT HERTEKENEN (SPRITE_KERN, letterlijk)
Bij een model (Gemini of ander) is de sprite de **verkleining van het model zelf**: natief raster terughalen → verkleinen met vlakgemiddelde + dichtstbijzijnde kleur uit het model → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten) en per pixel repareren wat de reductie kapotmaakt (oog, neus, mond), steeds naar het model. Gezicht, vlakken, schaduw en poten komen uit het model, niet uit de hand van de maker. Een toegestane afwijking van Jordi komt als laatste, als bovenlaag. De maker meldt per zone hoeveel pixels afwijken van de kale reductie. **Kleur mag altijd afwijken van het model**: vorm/silhouet/onderdelen uit het model, kleur, schaduw en volume naar Gen 3.

## Toegestane afwijkingen (bovenlaag)
1. **Formaat:** zoals de huidige sprite: ±48 px hoog (oren t/m voeten), breedte volgt uit het model. Op 64×64 onderaan geplaatst zoals andere Gen 3-sprites, ongeveer gecentreerd.
2. **Kleuren = het palet van de huidige Palpaca** (`../ronde17/variant_kop/normal.pal`, sprite `../ronde17/variant_kop/anim_front.png`, frame 1 = bovenste 64×64): crème wol, rode handschoenen, kleurige kraag en manchetten, rode oorkwastjes, roze oorbinnenkant, donkere omlijning. Map de modelzones op deze tinten. Mist een tint (bv. de donkere verre achterpoot), leid hem af uit het oude palet; ≤16 kleuren totaal.
3. **Licht en schaduw naar Gen 3:** licht linksboven, schaduw die de ronde wolvormen volgt, gekleurde selout aan de lichtkant, donker aan de schaduwkant. De wol leest als enkele duidelijke krulvormen, geen ruis of dambord.
4. **Oog/gezicht:** uit het model; leest het na de reductie niet, per pixel repareren naar het model (één consistent 3/4-gezicht, klein neusje en mond).

## Werkwijze
- Lees eerst: `docs/lessen/SPRITE_KERN.md`, `docs/lessen/GEMINI.md` (Krassault/Abra/Hummlet: natief raster, reductie), `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken".
- Gereedschap om te hergebruiken: `docs/concept/sprites/octillery_evo/sprite3/natief.py` (natief raster), `docs/concept/sprites/kolibrie_pre/sprite/r*/scripts/` (Hummlet: oppervlakgewogen reductie + oud palet als bovenlaag), `docs/concept/sprites/poedelmot/kleur_r20/stappen/px.py`, `box1x.py`, `lijnkaart.py`.
- Gen 3-vergelijking: `graphics/pokemon/ponyta`, `mareep`, `skitty`, `torchic`; Dragonfly Cave: `docs/lessen/SPRITING.md` + `docs/lessen/bronnen/`.
- Werk in `sprite/r1/` (dan r2, ...): `onderlaag.png` (kale reductie), `palpaca.png` (64×64, geïndexeerd, ≤16 kleuren, index 0 transparant), `normal.pal`, scripts, `NOTITIES.md` (per zone aantal px afwijkend van de onderlaag, zelfgenoemde zwakke punten), `vel.png` (sprite 8× | model verkleind op dezelfde schaal 8× | oude sprite 8× | 1× op licht en donker | close-up kop en poten 12× naast het model).
- Let op (`SPRITE_WERKWIJZE`): `im.convert('RGBA')` op een geïndexeerde afbeelding negeert transparantie; eerst opslaan met `transparency=0`.
- Zelfgenoemd zwak punt = eerst zelf repareren. Niets naar Jordi; Claude bekijkt het vel.
- Geen git commit/push (doet Claude).
