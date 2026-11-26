# Eindkeuring r15 (keurder + Dragonfly Cave), ruimtestation fase 3

**Oordeel: PASS** voor `eindkeuring_r15/sprite.png`. Dat is r15 met 36 indexwissels, allemaal hieronder benoemd.
- Bijgewerkt: PF/PE/PB-randen; silhouet +5 px.
- Ongewijzigd: ogen en bollen.

r15 zelf was nog **niet** goed genoeg. Er zaten zes uitvoeringsfouten in die binnen de checklist vallen, en die heb ik zelf opgelost. Er is geen MOET-lijst voor de maker.

## Bestanden
- `sprite.png`: 64×64, index 0 transparant (transparency=0), 16 kleuren incl. transparant, palet ongewijzigd.
- `sprite_8x.png`
- `vel.png`, met:
  - r15 | gecorrigeerd | model, op 8×;
  - close-ups van PE/PF/voorbuis, PB+PA en PC;
  - 1×/2×/3× naast fase 2 en Magneton, op licht en donker.
- `fix.py` en `log.txt`: elke pixel met zijn reden, vanaf `sprite/r15/sprite.png`.

## Checklist (Jordi's woorden)

| Punt | r15 | Na eindkeuring |
|---|---|---|
| Ogen zoals r11, driekwart, ring+iris+pupil, geen wit binnen de ring | ok (0 px verschil met r11) | ongemoeid |
| Bollen rond (cirkelfit op de vrije rand) | voor 0,41 · links 0,40 · eindbol 0,39 · rechts 0,55 (1 px, (54,43)) | idem; rechts zit binnen meetruis |
| Rechterbol vóór PC | ok (bolrand x50–56 y32–33 over PC) | idem |
| PA rechts van PB loopt door tot de achterarm | ok. Bovenrand helling 0,29, gelijk aan links van PB en aan het model | eindpixel (42,24) navy (lichtkant) |
| PB: 4 px tussen de rasterlijnen | **fout**: lijn 2 had een ander trapje dan lijn 1, dus vakken 4/3/2 px op x34/x36 | lijn 2 = lijn 1 + 4 px; vakken 3 px |
| PF = PB-breedte, 4 px, stok gecentreerd | breedte en lijnen ok. **Boven- en onderrand niet parallel** aan de rasterlijnen: vak 1 was 2 px op x34/x36, het laatste vak 2 px op x35 | boven- en onderrand in het PB-trapje; elk vak 3 px + lijn |
| PF leest als één doorlopend paneel achter PE | **fout**: PE had boven PF géén bovenrand ((32–34,46/47) liep als vak door in PF). Daarnaast een losse navy pixel (34,46) | PE-bovenrand volgens de PE-geometrie (GEO10, PE vóór PF), recept herberekend: trapje (30–31,45) · (32–34,46) · (35–37,47) · (38–40,48) |
| Geen onnodige zwarte pixels; buitenlijn 1 px | **fout**: dubbele zwarte band onder de voorbuis (27–29,44–45; 31–32,41–43) | onderrand 1 px langs de modelrand (26,46)→(33,41); de rest is buisschaduw (4) |
| Gaatje 2×2 op (30–31,44–45) | leest als gat met een dikke zwarte rand | Nu 2×1 (30–31,44), zie hieronder |
| Geen ruis in panelen | PC (53–54,31): dubbele rasterlijn C+E. Hubkraag 8-3-1-8-3-8 plus een losse witte pixel (37,27) | PC één lijn; kraag: stok loopt door, rand 8 8 8, bovenrand navy |
| Zwart alleen aan de schaduwkant | gemeten: 1 pixel zwart aan de lichtkant (42,24) | 0 |
| Schaduw, tinten, ≤16 kleuren | licht linksboven consistent. Ramps logisch (wit 249/210/158, paneel 183/132/103/54, paars 146/109/76) | idem |
| Volgt het model, geen herontwerp | ok | idem; alleen indexwissels en randen per pixel |

## Het gaatje
Volgens de PE-geometrie liggen (30,45) en (31,45) ín PE: dat is de bovenrand van PE. In r15 waren ze transparant, en (32–33,46) hoorden bij PF terwijl PE ervoor ligt.

Na de correctie blijft alleen (30–31,44) over: echte achtergrond tussen buisrand, PF en PE. In het model is daar een witte driehoek. De sprite houdt die ruimte dus trouw, alleen kleiner, omdat PE in de spritefase breder is gemaakt (×1,5).

Gen 3 heeft zulke ingesloten gaatjes vaak. Gemeten: 53 gaatjes van 2 px, bijvoorbeeld bij Aerodactyl, Golem, Hariyama en Jolteon. Op 1× leest het als een spleet tussen de onderdelen, niet als een fout. Ter info: moet hij dicht, dan is dat een ontwerpkeuze van Jordi (dichtmaken = PE of buis hoger, en dus van het model af).

## Ter info voor Jordi (geen fout, wel zichtbaar)
- **De stok in de hubkraag staat links van het midden** (kraag x33–39, stok x34–35). Dat komt waarschijnlijk door de PB-verschuiving van −2. Niet aangeraakt; dit is een vormkeuze.
- **Twee enkele lijnpixels in PA** ((29,24), (31,25), lichter in het donkere vak). Volgens het recept zijn het lijnpixels; ze laten de vakgrens zien en lezen niet als ruis.
- **De rechterbol wijkt op één randpixel 0,55 px af.** Andere selectie = 0,5; niet zichtbaar.
