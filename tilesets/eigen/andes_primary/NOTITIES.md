# Andes-primary (ronde 2)

Gedeelde primary voor La Paz, de altiplano en later andere Andes-gebieden (door Jordi bevestigd, 22 okt).
Opnieuw maken: `python3 tools/concept/tiles/andes_primary.py`. Voorbeelden: `voorbeeld_*.png` (echte Hoenn-kaarten
met deze primary: `python3 tools/concept/tiles/r2_preview.py <Kaart> <uit.png> [x0 y0 x1 y1]`).

## Opbouw
- **Kopie van General**: zelfde 512 tegels, metatiles, gedrag en animaties (water, bloemen, watervallen; de
  animatieframes in `data/tilesets/primary/general/anim/` blijven bruikbaar, het zijn indexen). Alle
  Hoenn-secondaries passen er dus op, en La Paz/altiplano kunnen Hoenn-metatiles 1-op-1 overnemen.
- **Paletten 0–5 omgekleurd** (de enige wezenlijke wijziging):
  - palet 2 grond: gras → goudgele puna (240,224,152 / 216,192,112 / 192,160,80 / 168,128,48); bomen iets olijfgroener.
  - **hoog gras → ichu** zonder pixelwijziging: de grastegel gebruikt de grondindexen 12/13/15 en omlijning 4.
  - palet 3: mauve rotsbergen en rotsgrond → rode klei (de hellingen van La Paz); grijze stenen blijven.
  - palet 5: Hoenn-zand → lichte onverharde weg.
  - palet 4: drie ongebruikte indexen (3–5) → rotsgrijs voor bergen.
  - index 15 van elk palet (Hoenn-gras) → puna-grond, zodat gebouwranden naadloos op de grond staan.
- **Nieuw** (in ongebruikte General-metatiles: nergens op een kaart, niet in `metatile_labels.h`): verre bergketen
  (4×3, naadloos) + effen lucht, straatlantaarn (1×2), bank, kantuta-struikje.

## Budget
- Tegels: 512, waarvan 44 nog vrij (47 nieuwe tegels in ongebruikte General-plekken).
- Metatiles: 512, waarvan 48 slots nog vrij voor nieuwe gedeelde dingen.
- Paletten: 0–5 (zoals General).

## Bij inbouw
- Het grasdeeltje (field effects `tall_grass`, `jump_tall_grass`, `cut_grass` in `graphics/field_effects/pics/`)
  is groen: omkleuren naar ichu.
- Hoenn-kaarten die nog meekomen krijgen met deze primary vanzelf de Andes-kleuren (zie de voorbeelden).
