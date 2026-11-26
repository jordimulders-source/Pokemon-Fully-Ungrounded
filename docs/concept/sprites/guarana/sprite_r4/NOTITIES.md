# Guaraná fase 1, ronde 4: reparaties uit `sprite_r3/KEURING.md`, silhouet bevroren

Bestanden: `guarana_r4.png` (hoofdversie), `r4_ogen_groter.png` (Weepinbell-ogen), `kaal.png`, `vel.png` (r4 | r3 | model, close-ups, 1×), `vel_ogen_groter.png`, `varianten.png` (r4, r4-ogen, r3, r2; 8× en 1× op wit/crème/donker), `bouw.py` (r3 + r4-wijzigingen; zonder-puntjes werkt nog via `VARIANT=zonder_puntjes`).
**Alle waarden hieronder zijn na het bouwen in de png gemeten** (niet uit het script overgenomen).

## Waarom r3 een paar reparaties miste
- **Groene pixels (47,45), (23,46), (48,46), (52,46):** de r3-code zette alleen een andere *vul*tint (7/8/9) van de buren; die pixels hebben alleen lijnburen, dus er gebeurde niets. In r4: buurtint = meest voorkomende vultint van de 4-buren, anders de lijntint. Nu alle vier lijngroen (6).
- **Bocht (16,27)/(17,26):** stond wél in de png (beide lijnrood 2), maar samen met (17,27) en rij 28 vormt hij een blokje. De keurder meet dat het model hier zelf recht is; ik heb het niet verder veranderd.

## Reparaties r4 (gemeten in de png)
1. **Kolom 21, y30–33:** nu middenrood (4) op alle vier pixels.
   - Modelmeting: L 95 / 98 / 98 / 92, lijndekking 23 / 3 / 0 / 9 %. Dat ligt op de grens schaduw/midden (drempel 100).
   - (21,31–32) heb ik op midden gezet; (21,30) en (21,33) werden daarna bij het ontkorrelen ook midden, omdat ze losse schaduwpixels waren. Geen schaduwband meer naast lijnkolom 22.
2. **Sikkel linkervrucht:** (13,27) midden (model L 125, 0 % schaduw); (14,27), (15,27) en (16,26) schaduw (model 0–32 % schaduw, zoals de keurder voorstelt). De sikkel loopt van rechtsboven (16,26) naar links omlaag uit. Hij is diagonaal en wordt na het ontkorrelen expliciet teruggezet, anders zou hij als ruis verdwijnen.
3. **Losse pixels → buurtint** (meest voorkomende vultint van de 4-buren, anders de lijntint):
   - (15,22), (15,23), (16,23) → midden 4
   - (18,34) → licht 5 (sluit aan op het hooglicht (19,33–34))
   - (27,27), (28,29), (13,29), (14,29) → lijnrood 2 (alleen lijnburen)
   - (47,45), (23,46), (48,46), (52,46) → lijngroen 6
   - (13–14,29) zit nu als lijn onder rij 28; daar is de lijn 2 px dik over 2 pixels.
   - Daarna één extra ontkorrelronde (oogpixels uitgezonderd): 5 px.
4. **Ogen:**
   - **Kijkrichting gemeten** in het natieve model (pupilmidden t.o.v. het midden van wit+pupil): bovenoog −0,3/+0,4 (links-omlaag), rechteroog +1,3/−0,2 (rechts), onderoog −1,0/+0,3 (links).
   - **Hoofdversie:** Psyduck-oogwit (5×4) blijft, pupil 1 px op de kijkkant: bovenoog (18,21), rechteroog (28,22), onderoog (16,31). Oogwit nog steeds één vlak per oog (3× 15 px).
   - **Gekozen: 1 px.** Een pupil van 2 px (1×2 of 2×1) uit het midden splitst in dit 5×4-oog het wit in twee stukken (getest: wit 12 + 2 px per oog) of raakt de oogrand. Op 1× leest 1 px op de kijkkant duidelijk als kijkende ogen (`varianten.png`).
   - **Variant (Weepinbell):** boven- en onderoog kijken al links, zoals het model. Het rechteroog keek links; nu staat de pupil 1 px naar rechts (2×2 op (27–28,23–24)). Het oog staat 1 px lager (y0 20), anders werd de witte rand rechts van de pupil door de buitenrand een los eilandje. Oogwit 17/16/17 px, één vlak per oog.

## Metingen (png)
| | hoofdversie r4 | ogen groter r4 |
|---|---|---|
| alpha-diff t.o.v. r1/r2/r3 | 0 | 0 |
| zwart | 16,7 % | 17,9 % |
| zwart alleen aan de lichtkant | 0 | 0 |
| oogwit per oog | 15 / 15 / 15 (één vlak) | 17 / 16 / 17 (één vlak) |
| anders dan kaal: tros+ogen / rank / krullen / blad | 166 / 51 / 83 / 17 (317) | 167 / 51 / 83 / 17 (318) |
| anders dan r3 | 40 px | 35 px |

Controle: geen lichte kleur op de buitenrand, geen losse zwarte pixels; 10 kleuren + transparant.

## Zwakke punten (eerlijk)
- **Pupil hoofdversie is 1 px:** het model heeft ±2×2. Leest als kijkend oog, maar is kleiner dan in het model.
- **Variant-rechteroog:** de 2×2-pupil raakt met zijn rechteronderhoek diagonaal de buitenlijn ((28,24) naast (29,24)).
- **Lijn rechtsonder rij 28:** onder de linkervrucht 2 px dik bij x13–14 (rij 28 + (13–14,29)), want beide pixels hadden alleen lijnburen.
- **Kolom 21:** het model is daar eigenlijk donker (L 92–98, net onder de schaduwdrempel). Midden is een keuze op de grens, op verzoek van de keurder.
