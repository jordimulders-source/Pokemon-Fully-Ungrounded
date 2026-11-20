# Opdracht maker: Llamauler (lama, Fighting-starter fase 2) frontsprite naar het nieuwe model (19 nov)

## Jordi (19 nov, letterlijk)
- "llamauler is idd erg plat, niet helemaal goed in verhouding, niet goed aangekleed, handschoenen kunnen beter en de kop is net niet llama genoeg"
- "ja de handschoenen behouden, hij wisselt juist van vechtstijl en dat vind ik prima"
- Over Gemini r4: "op de achterste handschoen na vind ik dit het beste ontwerp"
- Over de handschoenen: "r3 is de enige met goede handschoenen"
- Over de loopfoto: "deze lama heeft de juiste pose toch, maar dan gespiegeld?" → r12 "eindelijk"
- Nu: "kan je hier een sprite van maken? Dan plakken we weer de correcte poten met handschoenen erop"
- Verloop en alle citaten: `../gemini/PROMPT.md`.

## Model (bevroren)
- **Lijf, kop, hals, wol, kleding, staart:** Gemini r4, `../gemini/r4/r4_prompt_v4.png` (1024²). Boven de poten is het naadplaatje `../gemini/r13/r13_naad.png` vrijwel gelijk; gebruik r4.
- **Poten (de gang):** `../gemini/poten/r4_poten_r12.png` = r4 met de vier poten van r12 (lama naar een echte loopfoto), al omgekleurd naar karamel (nabij licht, ver donker). Telgang, van links naar rechts: nabije voorpoot schuin vóór, verre voorpoot (donker), nabije achterpoot (licht) vóór onder de buik, verre achterpoot (donker) achteraan. Pootposities, hoeken en welke poot voor/achter zit moeten exact blijven: dat is het hele punt.
- **Handschoenen:** die van Gemini r3, `../gemini/r3/r3_prompt_v3.png` (beide voorvoeten, rond y 850–1000; dicht, rood, zwarte polsband, wijzen naar links, verre donkerder, teennageltjes vóór). Zet ze op de voorvoeten van de nieuwe poten (op spriteformaat, als bovenlaag), wijzend naar links in de looprichting. Geen vingers, duim of open handpalm. Achtervoeten = gewone hoeven.

## MODEL OVERNEMEN, NOOIT HERTEKENEN (SPRITE_KERN, letterlijk)
Bij een model (Gemini of ander) is de sprite de **verkleining van het model zelf**: natief raster terughalen → verkleinen met vlakgemiddelde + dichtstbijzijnde kleur uit het model → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten) en per pixel repareren wat de reductie kapotmaakt (oog, neus, mond), steeds naar het model. Gezicht, vlakken, schaduw en poten komen uit het model, niet uit de hand van de maker. Een toegestane afwijking van Jordi komt als laatste, als bovenlaag. De maker meldt per zone hoeveel pixels afwijken van de kale reductie. **Kleur mag altijd afwijken van het model**: vorm/silhouet/onderdelen uit het model, kleur, schaduw en volume naar Gen 3.

## Toegestane afwijkingen (bovenlaag)
1. **Formaat:** zoals de huidige Llamauler (`../af/lama.png`: box 41×62, 1184 px): ±62 px hoog (oren t/m voeten), breedte volgt uit het model; onderaan in 64×64, ongeveer gecentreerd.
2. **Kleuren:** uit het model, ≤16 kleuren totaal (index 0 transparant). Ter vergelijking het oude palet `../af/normal.pal`.
3. **Licht en schaduw naar Gen 3:** licht linksboven, schaduw die de ronde wolvormen volgt, gekleurde selout aan de lichtkant, donker aan de schaduwkant. Wol als enkele duidelijke bollen (Mareep/Flaaffy), geen ruis of dambord.
4. **Gezicht:** uit het model (droog oog met zwaar vlak ooglid, platte mond); leest het na de reductie niet, per pixel repareren naar het model.
5. **Halsband en pompons:** de strepen worden ±1 px per streep; pompons als stipjes met donkere rand zodat ze niet wegvallen in de wol (Claude, akkoord van Jordi: "Halsband is even de vraag of het anders naar een sprite te vertalen is").

## Werkwijze
- Lees eerst: `docs/lessen/SPRITE_KERN.md`, `docs/lessen/GEMINI.md` (Krassault/Abra/Hummlet/ijskomeet: natief raster, reductie), `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken".
- Gereedschap: `docs/concept/sprites/octillery_evo/sprite3/natief.py` + `half2.py` (natief raster), `docs/concept/sprites/kolibrie_pre/sprite/r*/` (Hummlet-reductie), `docs/concept/sprites/poedelmot/kleur_r19/stappen/px.py`, `kleur_r20/stappen/box1x.py`, `docs/concept/sprites/poedelmot/silhouet/sil.py`.
- Gen 3-vergelijking: `graphics/pokemon/mareep`, `flaaffy`, `ponyta`, `girafarig`, `stantler`; Dragonfly Cave: `docs/lessen/SPRITING.md` + `docs/lessen/bronnen/`.
- Werk in `sprite/r1/` (dan r2, ...): `onderlaag.png` (kale reductie), `lama.png` (64×64, geïndexeerd, ≤16 kleuren, index 0 transparant), `normal.pal`, scripts, `NOTITIES.md` (per zone aantal px afwijkend van de onderlaag, zelfgenoemde zwakke punten), `vel.png` (sprite 8× | model verkleind op dezelfde schaal 8× | oude sprite 8× | 1× op licht en donker | close-up kop en poten 12× naast het model).
- `im.convert('RGBA')` op een geïndexeerde afbeelding negeert transparantie; eerst opslaan met `transparency=0`.
- Zelfgenoemd zwak punt = eerst zelf repareren. Niets naar Jordi; Claude bekijkt het vel. Geen git commit/push (doet Claude).
