# Keuring Hummlet r2 (19 nov), verse keurder

Gekeurd: `hummlet.png` (oog a) en `hummlet_oogB.png` (Starly-oog), naast het model `../../referenties/gemini_gekozen_r5.png`, verkleind naar dezelfde schaal (790×687 → 40×35 op x 12–51, y 24–58), en naast Taillow, Starly en Swablu. Hulpbeelden staan in `/tmp/claude-0/keurder_hummlet/` (`naast.png`, `kop.png`, `kop2.png` = kop na de MOET-reparaties, `test8.png`, `1x_3x.png`).

## Blinde indruk
Op 1× is dit een nette, schattige Gen 3-sprite van een rond kolibriekuiken: een bolletje met een lange naaldsnavel, een gespikkelde lichte borst, een grote blauwviolette vleugel, een staartje en kleine oranje pootjes. Hij staat goed naast Taillow en Starly. Hij leest als kolibriejong; Jordi zou hem willen zien.

Wat meteen opvalt:
- De snavel is een dun, getrapt lijntje. Bij de basis zit een zwarte klont, die op 8× leest als een boze wenkbrauw of snor onder de snavel.
- De staart is een rommelig blokje.
- De binnenlijn langs de voorrand van de vleugel is onderbroken.

## Eis 1: trouw aan het model
- **Silhouet:** sterk. 669 px overlappen. 19 px staan alleen in het model, 10 alleen in de sprite. Die afwijking zit vrijwel helemaal in de snavel en de staartpunt.
- **Kop, oog, vleugel, pootjes en mondhoek:** plek en maat kloppen.
  - Het geel in de mondhoek staat op (26,31), precies waar het model het heeft.
  - De rechterpoot staat lager dan de linker, zoals in het model.
  - De vleugel heeft boven lila en onder blauw, met veerlijnen.
- **Snavel:** wijkt af. Het model heeft een wig: ±3 px dik aan de basis (x 20–25), taps naar 1 px aan de punt. De sprite is overal 2 px, met zwart onder leisteen. Het donker dat het model aan de basis heeft, zit in de sprite als zwarte lijn-massa onder de snavel (rij 30–32) in plaats van als snavelvulling. Dat is de "donkere massa" die de maker meldde. Beide punten zijn één fout en worden met MOET 1 samen opgelost.
- **Staart:** in het model een waaier: een lichte lila veer boven, een blauwe veer eronder, met een ingesneden punt. In de sprite is het een blokje van 5×4 waarin 4, A en 8 elkaar per 2 px afwisselen. Op 1× leest dat als een vlakje (MOET 4).
- **Spikkels:** volgen de modelplekken redelijk (bijv. (25,42) = modelspikkel). (24,44) heeft geen tegenhanger in het model (MAG).

## Eis 2: Gen 3-techniek
- **Contrast:** lila 3→4→5→6 = ±100/143/182/223, dus stappen van ±40. Goed. Blauw 8/A is goed.
- **Licht en schaduw:** licht linksboven met glans op de kruin, een sikkel achter de kop en onder de buik. Goed. De buiksikkel (6→5→4) loopt licht parallel aan de onderrand (MAG).
- **Belijning: fout.** Zwart en selout (2) wisselen om en om op één rand:
  - bovenop de kop: (32,24)=1, (33,25)=2, (34,25)=1;
  - linksonder langs de buik: (21,43)=1 tussen tweeën, en (24,48)=2 tussen enen.
- **Binnenlijn vleugelvoorrand: fout.** Die is onderbroken en wisselt van kleur:
  - (32,39)=4 is een gat;
  - (32,42)=1 en (32,44)=1 staan om en om met 2 op (32,43);
  - (31,36)=2 is een losse donkere stip die donkerder is dan de andere spikkels.
- **Clusters < 3 px:** buiten de staart zijn het alleen spikkels, het oog, de mondhoek en diagonale lijnen. Die zijn toegestaan.
- **Pootjes:** klein, omlijnd en in de plaatsing van het model. Goed.

## Oordeel: TERUG
Het gaat om kleine, puur scriptbare reparaties. Silhouet, pose en kleur zijn goed. Ik heb alle MOET-punten hieronder op een kopie toegepast en bekeken (`test8.png`, `kop2.png`): de snavel wordt de wig uit het model, de "wenkbrauw" verdwijnt en de staart wordt rustig.

## MOET (coördinaten (x,y) op 64×64, palet `r2/normal.pal`; geldt voor beide oogversies, want geen enkele pixel valt in de oogzone)
1. **Snavel tot een wig aan de basis, uit het model** (lost ook de donkere massa onder de mondhoek op):
   - (20,29) 1→14, (21,29) 1→14, (20,30) 0→1, (21,30) 0→1
   - (22,30) 1→14, (23,30) 1→14, (22,31) 2→1
   - (24,31) 1→14, (25,31) 1→14
   - Ongewijzigd blijven (23,31)=1, (24,32)=1 en (25,32)=1: dat is de onderlijn van de snavel.
   - Silhouet +2 px, op plekken waar het model al massa heeft.
2. **Buitenlijn niet om en om:**
   - (33,25) 2→1
   - (21,43) 1→2
   - (24,48) 2→1
   - Daarmee is de linkerrand selout t/m rij 45 en zwart vanaf rij 46.
3. **Binnenlijn vleugelvoorrand doorlopend en in één kleur:**
   - (32,39) 4→2, (32,42) 1→2, (32,44) 1→2
   - (31,36) 2→3: wordt een gewone spikkel.
4. **Staart als twee veren, zoals het model (lila boven, blauw onder):**
   - (47,45), (48,45), (49,45), (50,45) → 4
   - (47,46), (48,46) → 10
   - (49,46), (50,46) → 8
   - (49,47) 10→8

## MAG
- Staartpunt ingesneden, zoals het model: (50,46) 8→1, (51,46) 1→0, (51,47) 1→0.
- Snavelrug: het model heeft een lichtere bovenrand. Bijvoorbeeld de bovenste snavelrij op x 18–23 in index 3 in plaats van 14. Pas toepassen als het op 1× niet gaat flikkeren.
- Spikkel (24,44) 4→6: staat lager dan de modelspikkels.
- (23,34) 6→5: losse lichte pixel aan de linkerrand van de keel, tussen 5 en 4.
- Buiksikkel: de 5-band onderaan iets laten verlopen (links breder, rechts smaller), zodat hij minder parallel aan de rand loopt.

## Oogadvies (advies, geen besluit)
**Oog a.** Het model heeft een donker, rond oog met een witte glans linksboven. Oog a geeft precies dat: een zwarte rand, een donkere leisteen-iris en een glans op (31,30). Op 1× leest het als een donker kuikenoog. Oog b (Starly) staat hier als een zwart kader rond een witte/lichte kolom (7 boven 5). Op 8× leest het als een hol "0" of een staroog, op 1× lichter en wat schrikkerig. Het past niet bij het donkere modeloog. Eventueel bij oog a als MAG: (32,31) 14→1 voor een donkerder pupil, maar het werkt nu al.
