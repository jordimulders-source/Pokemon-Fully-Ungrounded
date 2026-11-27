# Eindkeuring guaraná fase 2 (Dragonfly Cave: schaduw + belijning + kleurtinten), 27 nov

Getoetst: `sprite_r16/guarana2_r16.png` (door Jordi goedgekeurd: "kijk eindelijk, eindkeuring"), naast fase 1 (`../guarana/af/guarana.png`) en de fase 1-eindkeuring (`../guarana/eindkeuring/EINDKEURING.md`).
Alleen uitvoering; geen herontwerp.

Oogrand: Jordi (via coördinator): "geen idee waar je op doelt maar dit is prima" → oogranden blijven zoals in r16; alleen één versie (EK_B vervalt).

## Uitvoer
- `guarana2_ek.png`: de eindkeuringsversie (= EK_A).
- `normal.pal`: palet ongewijzigd (= r16 = fase 1).
- `voor_jordi_ek_8x.png`: fase 1 | EK | r16 op 8×, wit.
- `afstand.png`: fase 1 en EK, elk op 1× en 2×; bovenste rij op wit, onderste op donker.
- Scripts, te draaien vanuit `guarana_fase2/`:
  - `bouw_ek.py`: leest r16 in, zet alleen de benoemde pixels, met asserts;
  - `vel_ek.py`: maakt de vellen.

## Bevroren (bewezen met asserts in `bouw_ek.py`)
- **Silhouet:** alpha-diff 0 t.o.v. r16.
- **Oogwit:** diff 0.
- **Ogen:** geen enkele gewijzigde pixel grenst (ook niet diagonaal) aan oogwit. Daarmee zijn pupillen, kijkrichtingen, half dichte ogen en oogranden onaangeroerd.
- **Vruchtvormen en -posities:** ongewijzigd. Er zijn alleen tinten binnen bestaande vruchten veranderd, plus lijnpixels.
- **Palet:** ongewijzigd; geen nieuwe tinten (10 kleuren + transparant).

## Gids (letterlijk, `docs/lessen/bronnen/dragonflycave_spriting_guide.txt`)
- r. 96–97: "The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites".
- r. 106–107: "the relative luminosity of the shades on the original sprite should always be maintained on the new one."
- r. 112–113: "The outline base and outline highlight colors are also colors."
- r. 117: "The outlines must be reasonably dark."
- r. 419–422: "With the outlining all-black, it looks very 2D and cartoony ... we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 424–428: "the R/S sprite actually also features some anti-aliasing on the outside of the outline. This is a bad idea ... lighter pixels on the inside of the outline are a far better idea".
- r. 452–455: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts ... place pixels of the outline highlight color on the inside of the outline rather than the outside."

## 1. Schaduw: was BIJNA, nu aangepast → PASS
**Licht en schaduw:**
- Het licht linksboven is in r16 consequent:
  - hooglicht linksboven in de vruchten;
  - licht op de linkerkant van stam en ranken, donker rechts/onder.
- Geen pillow shading. Wel hadden een aantal vruchten aan de rechteronderkant geen sikkel: midden liep door tot aan de naad. Rood schaduw was 10,7 %.

**Wijziging:** 27 px midden (4) → schaduw (3), elk op een vruchtrand rechtsonder (tegen naad of zwart).
- Gekozen uit de automatisch gezochte kandidaten: middenpixel met lijn of zwart rechts/onder, niet naast een oog, niet al tegen een lijn links/boven.
- Alleen kandidaten die aansluiten op bestaande schaduw of op elkaar. Zo ontstaan er sikkels en geen losse puntjes.
- 8 kandidaten zijn weggelaten, omdat ze een los vlekje zouden geven.

| tros | pixels |
|---|---|
| middentros | (22,17) (21,18) (30,17) (28,20) (27,21) (27,23) (28,23) (25,24) (26,24) (29,28) (25,30) |
| linkertros | (7,27) (8,27) (4,31) (4,32) (3,33) (2,34) (2,35) (7,36) (6,37) (5,38) (9,41) |
| rechtertros | (51,27) (53,32) (53,35) (50,38) (47,41) |

Het groen (stam, blad, ranken) is niet veranderd: het volgt de lichtrichting al.

## 2. Belijning: aangepast → PASS
Omlijningsronde volgens de gids. Rand gemeten per buitenrandpixel: lichtkant = de normaal wijst naar linksboven.

**Lichte binnentint óp de buitenrand:** r16 had 13 px schaduwgroen aan de lichtkant en 15 px aan de schaduwkant. Dat is "anti-aliasing on the outside" en een lichte kleur op de buitenrand.
- Lichtkant en dunne puntjes/rankjes → lijngroen (6), zoals de 1-px-ranken van fase 1:
  - lus boven: (31,1) (32,1) (33,1) (32,2);
  - rankje boven midden, linkerrand: (36,7) (36,8) (36,9);
  - bladpunt boven de middentros: (19,8);
  - blad linksboven: (14,11) (15,11);
  - bladpunt links: (2,17) (1,18) (2,18);
  - bladpunt rechts: (61,19) (zat tussen 2 zwarte);
  - bladpunt rechtsonder: (60,24) (61,24);
  - grijprankje linksonder: (20,47) (20,48) (21,48) (21,49);
  - grijprankje onder midden: (33,50) (34,50).
- Schaduwkant van een groter vlak → zwart (outline shadow):
  - rankje boven midden, rechterrand: (37,6) (37,7) (37,8);
  - onderrand van het blad boven de linkertros: (15,21) (19,24).

**Zwart midden in een lichte rand:**
- (24,38), linkerrand van de stam → lijngroen;
- (49,10), bovenrand van de rechterlus → lijngroen.

**Lijnrood tussen zwart in de onderrand:** (6,39), linkertros → zwart. Dit was zwart/lijnrood om en om.

Na de ronde:

| | zwart | lijnrood | lijngroen | schaduwgroen |
|---|---|---|---|---|
| lichtkant | 21 | 30 | 134 | 0 |
| schaduwkant | 162 | 10 | 9 | 1 (zie hieronder) |

- Lichtkant: er zijn geen lichte tinten meer op de rand.
- Zwart aan de lichtkant zit alleen nog in hoeken linksonder (het begin van de zwarte boog), op puntjes van bladeren en ranken, en in de oogranden.
- Lijnrood aan de schaduwkant zijn **oogranden** (C, e, R1, q, F). Die blijven: Jordi vindt ze prima.

**Bewust gelaten:**
- (40,12): een stomp rankje van 1 px naast zwart. Zwart maakt er een blok van 2 px van.
- (42,29)/(43,30): zwart in de linkerrand van de rechtertros. Dat raakt de rand van oog R1, en oogranden blijven.
- (33,11): een hoekpixel.

**Binnenlijnen** (naden tussen vruchten, de getwijnde streng in de stam) zijn niet zwart en blijven ongewijzigd. Zwart binnen het silhouet staat alleen in ogen/pupillen en aan de buitenrand.

## 3. Kleurtinten: PASS (palet = fase 1)
Palet identiek aan fase 1. Rood met hue shift 357→3→8→14 en groen 102→99→88→81, al door de fase 1-eindkeuring goedgekeurd.

Verdeling (lijn / schaduw / midden / licht):

| | fase 1 | r16 | EK |
|---|---|---|---|
| rood | 39 / 17 / 34 / 11 % | 42,2 / 10,7 / 35,5 / 11,6 % | 42,1 / 15,3 / 31,0 / 11,6 % |
| groen | 32 / 19 / 35 / 15 % | — | 40 / 14 / 31 / 14 % |

- Rood EK zit binnen het doel ±40/15/35/10.
- Groen EK: meer lijn dan fase 1, omdat fase 2 veel meer dunne ranken en bladpunten heeft. Dat hoort bij de vorm en is geen tintfout.

## Pixeldiff
- **57 px anders dan r16:** 27 schaduwsikkel, 30 belijning.
- **0 px:** silhouet, oogwit, ogen (en alles eromheen).

## Ter info voor Jordi (niet uitgevoerd)
- **Oog R1, rechtertros:** de rand linksonder is zwart (42,29), daaronder lijnrood. Dat is oogrand, dus niet aangeraakt.
- **Lus bovenaan:** rij 2 (x31–35) is zwart, lijngroen, zwart, schaduwgroen, zwart, dus om en om. Het hoort bij de lusvorm uit r13 en is niet aangeraakt.

## Oordeel
**`guarana2_ek.png`: PASS.**
- Schaduwsikkels rechtsonder in alle vruchten.
- Rood schaduw 15 %.
- Buitenrand volgens de gids: lijntint aan de lichtkant, zwart aan de schaduwkant, geen lichte tinten op de rand.
- Ogen, vormen en silhouet bevroren.
