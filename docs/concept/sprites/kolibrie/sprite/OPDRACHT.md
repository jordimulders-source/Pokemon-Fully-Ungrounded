# Opdracht maker: Soulibri (kolibrie, Ghost/Flying) frame 1 + frame 2 naar Gemini (19 nov)

## Jordi (19 nov, letterlijk)
- Opknapronde: "het model blijft, in tegenstelling tot curiqui ben ik volledig tevreden met het design van soulibri en picapau." · **Soulibri:** "mag nog wat meer een typische kolibrie pose, maar behoud de kleuren en design"
- Gemini r1: "deze is al bijna helemaal prima, alleen de snavel is nu te kort" → snavel +2 modelpixels met eigen pixels verlengd: "+2 is perfect. Dan is de sprite al zo goed als af toch? Gemini heeft het een keer in de goede artstijl gedaan"
- Te breed (66 px): "we laten gemini de pose net iets anders maken" · "knippen wordt niet mooi denk ik"
- r3: "ok dit is een hele andere pose, niet erg overigens, want we hebben nu een frame 2, maar dit is niet de frame 1 pose die ik bedoelde"
- r4 (staart krult): "prima zo" · "moet er aan frame 1 en 2 nog gewerkt worden of kunnen ze zo geimporteerd worden?" · "nee we hebben nu frame 2 toch al" (= frame 2 nu meteen meedoen).

## Modellen (bevroren)
- **Frame 1:** `../referenties/gemini_gekozen_r4.png` (= `../gemini/r4_staart.png`). Raster gemeten 15,5 px per spritepixel, figuur 63×53 → 1-op-1 naar 64×64.
- **Frame 2:** `../gemini/r3_frame2_kandidaat.png`. Ander, niet-vierkant raster (gemeten ±13,2 × 12,0 px per blokje), figuur ±58×45 blokjes.
- Oude sprite (design/kleur-naslag, niet de vorm): `../af/kolibrie.png`.

## MODEL OVERNEMEN, NOOIT HERTEKENEN (SPRITE_KERN, letterlijk)
Bij een model (Gemini of ander) is de sprite de **verkleining van het model zelf**: natief raster terughalen → verkleinen met vlakgemiddelde + dichtstbijzijnde kleur uit het model → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten) en per pixel repareren wat de reductie kapotmaakt (oog, neus, tanden), steeds naar het model. Gezicht, vlakken, schaduw en poten komen uit het model, niet uit de hand van de maker. Een toegestane afwijking van Jordi komt als laatste, als bovenlaag. De maker meldt per zone hoeveel pixels afwijken van de kale reductie. **Kleur mag altijd afwijken van het model** (Jordi, 17 nov): vorm/silhouet/onderdelen uit het model, kleur, schaduw en volume naar Gen 3 en de keuringen.

## Eisen
1. **Frame 1 eerst:** natief raster (pitch/fase meten, celmidden/mediaan per cel), 1-op-1 → 64×64. Kleuren "behouden": het palet van de huidige Soulibri (`../af/kolibrie.png`: fluweelzwarte kop, iriserend violet lijf, blauwgroene schouderglans, bleek lavendel vleugels/zielvlammetjes, blauwgroen oog) — kies ≤15 kleuren + transparant die beide frames dekken. De vleugels lopen in het model van midden naar buiten lichter (Venomoth-effect, SPEC): houd dat als 2–3 tintstappen, geen ruis.
2. **Opschonen naar Gen 3:** ≤3 tinten per kleurgroep, geen tintvlakjes < 3 px behalve glans, buitenlijn 1 px (zwart aan de schaduwkant, gekleurde selout aan de lichtkant, niet om-en-om), geen banding/pillow shading, licht linksboven. Oog klein houden (Jordi eerder: "Oog moet wel klein blijven").
3. **Frame 2:** zelfde palet (GBA: beide frames één palet), zelfde formaat als frame 1: breng het frame 2-model op dezelfde spritepixelgrootte als frame 1 door de maat van vaste onderdelen te vergelijken (kop/oog/snavel/kuif/vleugels in spritepixels). Komt die maat al overeen in natieve blokjes, dan 1-op-1; anders herschalen op het natieve raster en daarna alleen de rafels schoonmaken (vorm bevroren). Past binnen 64×64. Plaats zo dat kop/lijf aansluiten op frame 1 (geen sprong in de animatie behalve de bedoelde pose).
4. **Lever** in `sprite/r1/`: `frame1.png`, `frame2.png` (elk 64×64, P, index 0 transparant, opslaan met `transparency=0`), `anim_front.png` (64×128, frame 1 boven, frame 2 onder), `normal.pal` (JASC), `onderlaag_f1.png`/`onderlaag_f2.png` (kale reductie), scripts, `NOTITIES.md` (per frame en zone: px afwijkend van de onderlaag, schaalbesluit frame 2 met metingen, zwakke punten), `vel.png` (frame 1 en 2 op 8× naast hun model op dezelfde schaal, oude sprite, Crobat/Ninjask/Beautifly 8×, beide frames op 1× licht/donker, een gif `anim.gif` die afwisselt).
- Lees eerst `docs/lessen/SPRITE_KERN.md`, `docs/lessen/GEMINI.md` (natief raster, sneeuwbolslak/Krassault/Abra), `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken", en `docs/concept/sprites/frame2_studie/STUDIE.md` §12.
- Zelfgenoemd zwak punt = eerst zelf repareren. Geen git (doet Claude).

## Jordi over sprite r1 (19 nov, letterlijk)
"frame 2 moet alleen nog klein beetje scheiding tussen de rechtervleugel en de staart, qua belijning/schaduw/kleur. Verder uitstekend"
→ reparaties 1–3 van Claude (kop, kuif, vleugelvlekken frame 2) vervallen; r2 = r1 + alleen die scheiding.
