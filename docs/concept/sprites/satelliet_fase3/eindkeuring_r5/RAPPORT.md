# Eindkeuring r5 ruimtestation (Dragonfly Cave), 25 nov

Invoer: `../sprite/r5/sprite.png` (r4 + MOET-reparaties uit `keuring_r4/OORDEEL.md`). Uitvoer: `sprite.png` (transparency=0), `sprite_8x.png`, `vel.png` (r5 | gecorrigeerd met rode kaders om de gewijzigde pixels | model verkleind, 8×; eronder op 1× en 1,5× naast fase 2, fase 1, Metagross, Magneton en Claydol (`anim_front_gba`), op licht en op donker), `ek5.py` (script, controleert elke oude index), `wijzigingen.txt`.

## Oordeel: PASS

Er zijn 28 pixels gewijzigd, allemaal als indexwissel. Het silhouet is gelijk (alpha-diff 0), het palet is ongewijzigd en er zijn 16 kleuren inclusief transparant. Er is niets toegevoegd of weggelaten ten opzichte van het model, en de ogen hebben binnen de ring alleen iris en pupil. Metingen na de correctie (scripts van keuring_r4 op de nieuwe sprite):
- `lijnzijde`: 0 pixels zwart alleen aan de lichtkant (was 1, (1,38)) en 0 pixels navy alleen aan de schaduwkant.
- `bollen2`: grote oogbol 0,41, kleine oogbol R 0,38, kleine oogbol L 0,29 en bol RB 0,34. Alle bollen zijn ≤ 0,8 en geen pixel van de vrije rand is veranderd.
- `binnenzwart`: 35 → 19 pixels. De overgebleven pixels liggen allemaal aan een schaduwkant: de rechterlijn van de mast, de onderboog van de hub, de linkerlijn van de onderste mast tegen het buiseinde en de onderranden van de buizen tegen de panelen erachter. Fase 2 (goedgekeurd) doet het daar net zo: zwart tussen het lijf en het paneel aan de schaduwkant.

## Toegepaste gidsregels (letterlijk, `dragonflycave_spriting_guide.txt`)
- r. 96–97: *"The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites"*. Zwart blijft daarom alleen als outline shadow staan.
- r. 112–115: *"The outline base and outline highlight colors are also colors. … you must also recolor the outlines."* Lila (5) en wit (f) op de bolrand zijn vervangen door de outline base.
- r. 117–123 (regel 4): *"The outlines must be reasonably dark. … create a separate outline highlight color that's darker than the shadow color."* De outline base aan de lichtkant (navy 2, L 42) is duidelijk donkerder dan de schaduwtint c (L 181). Dat is in orde.
- r. 421–423: *"we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."* Dit is toegepast op het zwarte cluster van twee rijen onder de hub en op de kerf tussen de armen. De bovenrand van de grote oogbol is nu een rand van 1 px.
- r. 427–429 en 452–455: *"lighter pixels on the inside of the outline are a far better idea"* · *"Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts … place pixels of the outline highlight color on the inside of the outline rather than the outside."* De lichtste delen liggen al binnen de lijn (f direct binnen navy) en er zit geen anti-aliasing aan de buitenkant. Ik heb geen extra outline highlights gezet, omdat de maatstaf fase 2 ze ook niet heeft (gemeten op de lichtkant van fase 2: navy 61×, zwart 26×, verder paars op de antennes). Zie SPRITE_KERN: "Maatstaf = onze goedgekeurde sprites".
- r. 104–107 (regel 1/2): de relatieve helderheid blijft behouden en er komt geen vreemde tint binnen één onderdeel. Daarom is lila 5 in de paarse oogring vervangen door ringpaars 6.

## Drie onderdelen
1. **Belijning:** de buitenlijn is navy aan de lichtkant en zwart aan de schaduwkant, zoals in fase 2. De binnenlijnen tussen de onderdelen zijn nu 3 (63,52,90, donkerste eigen tint) in plaats van zwart, op de plekken waar zwart/3/zwart om en om stond of waar het model licht is. Zie de tabel.
2. **Schaduw:** het licht valt overal linksboven. De bollen lopen van f/e linksboven naar c rechtsonder, zonder pillow shading. Op de buizen loopt de lichtstreep in de lengte (cilinder), en dat is geen banding. Hier was niets te corrigeren.
3. **Kleurtinten:** de ramps verschuiven logisch van tint. Wit gaat van f (h270) via e (277) en c (262) naar 4 (256), dus de schaduw schuift naar blauw. Paars gaat van 8 (287) via 7 (283) naar 6 (279), teal van a (178) naar 9 (182). De stappen in wit zijn 24 / 44 / 51. De enige fout was de oogring: lila 5 (h263, en lichter dan 6) stond om en om met 6. Dat is opgelost.

## Gewijzigde pixels (x, y in sprite.png; oud → nieuw)
| pixel | oud→nieuw | reden |
|---|---|---|
| (1,38) | 1→2 | zwart aan de lichtkant (punt van paneel PD) |
| (38,28) | 1→3 | mastvoetring 8/1/8-dambord; holte in de donkerste eigen tint (model L58) |
| (33,40) | 1→c | zwart cluster van 2 rijen onder de hub; het model is hier licht (L181) |
| (34,40), (35,40) | 1→2 | idem; bovenkant van de mast in de eigen navy (model L78/66) |
| (13,43) | 5→2 | bovenrand van de grote oogbol (lichtkant): lila → outline base |
| (14,43) | 5→f | binnen de bolrand; het model is wit (L227) |
| (14,42) | f→2 | losse witte pixel boven de rand → bolrand van 1 px |
| (15,42), (16,42) | 1→2 | zwart aan de lichtkant (bovenkant van de oogbol) |
| (17,42) | 5→2 | lila paneellijn op de bolrand |
| (21,45) | 1→c | binnenlijn van 2 px dik; het model is hier bol (L179) |
| (22,45), (22,47), (22,48) | 1→3 | lijn bol/kraag: 4/1/3/1/1 om en om → doorlopend 3 (model L52–54) |
| (24,46) | 1→3 | binnenlijn kraag/buis, niet zwart (model L94) |
| (12,50), (13,51), (14,52), (16,51) | 5→6 | oogring: lila 5 → ringpaars 6 (model 111,72,127) |
| (16,52) | 5→c | het model is hier bol (L185) |
| (41,32) | 1→3 | zwart tussen twee kragen (6 erboven en eronder) |
| (42,33), (43,33), (44,33) | 1→2 | bovenrand van de rechterarm (lichtkant), cluster van 2 rijen; sluit aan op navy (45,34) |
| (38,35) | 1→6 | losse zwarte pixel tussen hub en kraag (model 126,86,143) |
| (46,28) | 1→c | zwart in de buis; het model is licht (L162) |
| (47,28) | 1→3 | binnenlijn buis/module, niet zwart (model L59) |

## Ter info voor Jordi (ontwerp/kleur, niet doorgevoerd)
- **Panelen zijn veel donkerder dan in fase 2.** In fase 3 is de vulling van de panelen navy 2, dezelfde tint als de lichtkant van de outline. De panelen hebben daardoor aan de lichtkant geen eigen rand en geen volume (één tint met lijnen). Op een donkere achtergrond verdwijnen ze bijna (zie `vel.png`). Fase 2 heeft blauwpaarse panelen met twee celtinten en lichte lijnen. Het model heeft ook donkere panelen. Gelijktrekken met fase 2 is een kleurkeuze. Daarvoor zijn twee paletplekken nodig; 11 en 13 worden elk maar 3 px gebruikt en kunnen samengevoegd worden.
- De onderste mast is op rij 41–42 één pixel smaller (1-2-1) dan eronder (1-2-2-1). Dat zit in het silhouet en is niet aangeraakt.
- Op 1× is het station kleiner en luchtiger dan fase 2 (64×42 door de verhouding van het model).
- Open uit de SPEC: de stang van het tweelingpaneel opnieuw zichtbaar maken.
