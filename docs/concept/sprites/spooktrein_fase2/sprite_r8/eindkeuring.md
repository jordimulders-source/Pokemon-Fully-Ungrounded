# Eindkeuring spooktrein fase 2, sprite_r8 (Dragonfly Cave, 16 nov)

**Oordeel: PASS.** Naar Jordi mag.

Vergeleken op 1×, 2× en 8× naast haunter, banette, shuppet, magneton en koffing (`anim_front.png`, bovenste 64×64) en het model (`sprite_r2/model_geschaald.png`).

- **Leesbaarheid op 1×:** juichende groene geest in een roestige wagon met twee wieltjes en een wolk. Het leest meteen, en de massa en het detailniveau passen bij haunter en magneton.
- **Trouw aan het model:** de gemiddelde helderheid per zone ligt dicht bij het model (kop 187/171 tegen 201/185, arm 180/187, hand 148/163, wolk 141/143). Alles is iets donkerder, maar de verhoudingen kloppen.
- **Kleur:** 13 indexen. Groen 217/174/142/103 (stappen 43/32/39), brons/bruin 137/95/48, ijzer 162/123/74. Dat zit binnen de Gen 3-norm van ±30–40, en per kleurgroep zijn er hooguit 3 tinten plus lijn.
- **Lijnen:** de buitenlijn is overal 1 px en gesloten. Geen enkele lichte vulpixel raakt transparant (gemeten). Selout (5) zit links en boven, zwart (1) rechts en onder, met licht van linksboven.
- **De drie opschoonpunten uit r7b zijn opgelost** (diff 18, buiten de zones 0, gezicht 0, volgens `telling.txt`):
  1. Staartpunt: rand 5 tot en met (61–63,53), daarna 1. De inham (61–63,54) is dicht en volgt het model.
  2. Onderrand links: de tandjes (16,57) en (18,57) zijn weg. De lijn loopt (13,54) → (14,55) → (14–17,56) → (18,57) zonder om-en-om.
  3. Rij y46, x23–27: één tint (3).

## Reparaties
Geen verplichte reparaties. Optioneel en op 1× nauwelijks zichtbaar, dus geen FAIL-reden:
1. **(45,14)=1 grenst aan (46–47,15)=5:** op de bovenrand van de schouder, tussen de kop en de opgestoken arm, komt zwart direct naast selout. Het is één overgangspixel, maar de regel is "nooit zwart en selout om en om op één rand". Mogelijke fix: (45,14) → 5.
2. **Onderkant van de arm (x12–19, y23):** de rij 2,4,2,2,3,2,2,3 bestaat uit snippers van 1 px op de naad met de wagen. De regel is "geen tintvlakjes < 3 px". Neem hier één tint uit het model over.

## Ter info voor Jordi (geen keurpunt)
- De donkere strepen in de wolk zijn bijna recht en horizontaal: y52 x13–20, y53 x16–20 en y56 x20–30. Die laatste is de onderkant van het spookwiel. Ze volgen het model (schaduw van de wagen, de wielvorm), maar op 2× lezen ze als een liniaal. Wil je de wielbasis ronder?
- De lichte veegstrepen onderin de wolk (y58 x29–35, y59 x40–48) liggen parallel aan de onderrand. Ze komen uit het model, maar kunnen lezen als licht van onderen.
- De kop is heel licht (vooral tint 2, met een smalle sikkel van 1 px in tint 4 rechts). Dat is trouw aan het model, maar vlakker dan Haunter of Banette. Wil je een bredere schaduwsikkel rechts, dan is dat een stijlkeuze.
- Het donkerbruin (8 = 95) en het ijzergrijs (13 = 74) schelen maar 21 in helderheid. Ze blijven leesbaar door het verschil in tint.
