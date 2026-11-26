# Eindkeuring Dragonfly Cave, regionale Jynx (sirene): r2 → r3

Keuring op r2 en uitvoering als ronde 3 (25 nov). Getoetst: schaduw, belijning en kleurtinten (SPRITE_WERKWIJZE "Gemini-model namaken" punt 7, met de verplichte omlijningsronde volgens DC-gids r. 80–170 en 340–470).
Vergeleken met: model `gemini/r5.png` (op schaal en 12×), maatstaf-sprites Skinguin, Dundragoon, Zapacha en Princadee, en de Gen 3 `anim_front_gba.png` + `normal_gba.pal` van Jynx (rok en haar), Pidgeot en Articuno (vleugels) en Gardevoir (stof/jurk).
Bouwen: `cd docs/concept/sprites/jynx_regional && python3 sprite_r3/bouw.py` (variant: `... bouw.py kinschaduw`), vel: `python3 sprite_r3/vel_r3.py`.

## Eindoordeel: **PASS**
r2 was al bijna klaar. r3 verandert alleen 21 lijnpixels: de buitenlijn volgt nu overal de lichtrichting, en dubbele binnenlijnen uit de reductie zijn nu 1 px.
- Silhouet-diff 0 met r2 (assert in `bouw.py`).
- Gezicht (ogen, lippen, mond) 0 px gewijzigd (assert).
- Palet ongewijzigd. 16 kleuren incl. transparant, mode P, transparency 0.

## Bevindingen per punt

### Belijning (omlijningsronde volgens de gids)
- **Outline base per onderdeel:** veren/rok gebruiken veerlijn (120,48,24), haar gebruikt haar donker (84,50,28). Het gezicht heeft geen eigen donkere lijntint, dus de contour is haar donker; dat is een binnenlijn tegen het haar. Gemeten: geen lichte kleur op de buitenrand, zwart 7,3 %.
- **Outline shadow (zwart) alleen aan de schaduwkant:** gemeten met de randnormaal uit het afgevlakte silhouet. In r2 stonden 13 zwarte randpixels aan de lichtkant en 2 selout-pixels aan de schaduwkant.
  - Rechtgezet: 7 zwart → selout en 4 selout → zwart, zie de tabel.
  - Bewust zwart gelaten: de bovenkanten van de poten (8 px: (21,56) (20,57) (19,57) (16,58) (15,59) (37,56) (36,57) (35,58)). Ze liggen onder de overhangende rok, in de slagschaduw. Gen 3 houdt poten onder een lijf of een rok ook donker (Pidgeot-klauwen).
  - Gemeten in Gen 3-Jynx: bovenkanten krijgen selout, ook rechts op het haar (rij 7–9 `d`/`c`). De onderkant van de rokpunt is zwart (rij 53–54 `e`). r3 volgt dat.
- **Nergens zwart en selout om en om:** alleen blokovergangen op de hoeken.
- **Binnenlijnen niet zwart:** gemeten, buiten het gezicht staat geen enkele zwarte pixel binnenin.
- **1 px:** de reductie verdeelde op vier plekken één modellijn over twee pixels, wat dubbele lijnen of 2×2-klonten gaf.
  - Per plek bleef de pixel met de meeste modelzwart-dekking lijn (`dekking.py`); de andere werd het vlak ernaast.
  - Bij de kraag links stond D D l, 3 px donker tussen haarlok en kraag. Nu blijft de haarlijn (K44), want de lok ligt vóór de kraag; de veerlijn (K31) is kraag geworden.
  - Overgebleven 2-px-plekken zijn knooppunten van twee lijnen (vleugel links (9,21), V-punt kraag (24,33), vouwen bij de zoom (34,52)). Die staan zo in Gen 3-Jynx ook (rok rij 47–53).
- **Outline highlights binnen de lijn:** in orde. Licht staat binnen de selout op vleugels, linker rokpaneel en kruin, niet erbuiten.

### Schaduw
- Licht valt links/linksboven: links licht (vleugel links, kraag, linker rokpaneel), midden in het rokmidden, rechts schaduw (rokpaneel rechtsonder, achterhaar). De verdeling komt uit de modelhelderheid.
- Er staan geen met de hand verzonnen banden in. De enige band langs een rand (de lichtere strook langs het achterhaar rechts) staat zo in het model (81–92 tegen 57).
- Gemeten in het model:
  - De rok is vlak (145–146), de kraag ook (154–156).
  - De rok van Gen 3-Jynx werkt hetzelfde: vooral één basistint met vouwlijnen in de donkerste tint, de rechterkant in schaduw en weinig hooglicht. Onze rok leest daardoor als Gen 3, ook naast Skinguin en Dundragoon op 1×.
- **Haar:** het volume uit r2 (licht op de kruin, schaduw naast de strengen) is in orde.
  - Het achterhaar rechts is één donker vlak in haar donker (model 57–58, vlak). Dat is model en geen verlies van strenglijnen: het model heeft daar geen zwart (K 0 %).
- **Niet gedaan, want niet uit het model:** extra schaduw op rok of kraag. Zie de variant hieronder.

### Kleurtinten
- **Veren:** helderheid 172 / 141 / 106 / 67, stappen 31–39. Hue schuift richting rood in de schaduw (23° → 15°), net als Jynx' rok (28° → 8°).
- **Haar:** 160 / 123 / 89 / 58, stappen 31–37.
- **Gezicht:** 248 / 201. **Lippen:** 161 / 83 / 50.
- Alles ligt binnen ±30–40 per stap. Per groep ≤ 3 tinten + lijn. Niets aangepast.
- Kleine tintvlekjes < 3 px: alleen diagonale lijnstukjes en modeldetails (iris, tong, ooghoek), zoals in r2.

## Wat veranderd is (r3 t.o.v. r2: 21 px)
| zone | px | wat |
|---|---|---|
| haar bovenrand rechts (39,7) (40,7) | 2 | zwart → selout haar donker (bovenkant) |
| haarpunt rechts, bovenkant (53–56,40) | 4 | zwart → selout haar donker |
| haar links onder de vleugel (15,30) | 1 | zwart → selout (linkerrand) |
| rokpunt links, onderrand (10,54) (11,54) | 2 | selout → zwart |
| rokzoom boven de linkervoet (19,55) (18,56) | 2 | selout → zwart (onderkant) |
| kraag links (19,27–30) | 4 | dubbele lijn: veerlijn → kraag licht (haarlijn blijft) |
| rokvouw bij de zoom (22,53) (23,54) | 2 | lijn → rok midden (vouw 1 px diagonaal) |
| linkerpoot boven (22,56) (23,56) | 2 | lijn → veren schaduw (zoom is de lijn, poot vlak) |
| vouwknik rechts (34,48) (33,49) | 2 | lijn → rok midden (vouw 1 px diagonaal) |
Per zone: haar 7, lijf+rok 12, poten 2, vleugels 0, gezicht 0.

## Ter info voor Jordi (ontwerp/smaak, niet uitgevoerd in r3)
1. **Variant kinschaduw** (`jynx_regional_r3_variant_kinschaduw.png`, 11 px meer).
   - Wat: een gebogen slagschaduw van het gezicht op de kraag, in rok-midden, 1 px, langs de kinboog.
   - Dit is een voorstel van Claude. Het model heeft hier niets (kraag vlak 155); Gen 3-Jynx heeft wel zo'n schaduw onder het gezicht op de borst (rij 26–28).
   - De kraag is nu een vlak licht stuk van ±80 px. Kies alleen als je dat te effen vindt.
2. **Horizontale rokvouw rechts (rij 47, x33–46):** een rechte lijn van 14 px. Hij volgt de modelpunten (r2), maar in het model loopt hij iets schuiner. Alleen aanpassen als je hem te recht vindt.
3. **Klauwen in haar donker:** in r2 is de grijsbruine klauwtint geruild voor de lichte haartint. Op 1× lezen de klauwen goed; het model heeft grijsbruine klauwen.

## Bestanden
- `jynx_regional_r3.png` (kandidaat) en `jynx_regional_r3_8x.png`.
- `jynx_regional_r3_variant_kinschaduw.png` (variant).
- `bouw.py`, `vel_r3.py`.
- `vel.png`:
  - bovenaan r3 | r2 | model, 8×;
  - close-ups 12× van gezicht, haar, vleugels, rok en kraag/variant, telkens naast het model;
  - 1× op licht en donker naast Skinguin en Dundragoon, plus 2×.
