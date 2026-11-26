# Impala r11: eindkeuring Dragonfly Cave (schaduw + belijning + kleurtinten)

Opdracht (Jordi, 26 nov): "nee je mag nu gaan beginnen met de eindkeuring, dus netter maken".
Basis: r9 (= r10, pixeldiff 0, zelfde palet). Script: `sprite/r11.py` (leest `r9/impala_r9.png`), vel: `r11/vel.py`.
Niets getekend; elke wijziging is gemeten op het model (`kaal_lf` = aandeel zwarte modellijn in de cel, `kaal_nla` = modelhelderheid zonder lijn) of volgt de 1-px-regel van de gids. Log per pixel: `r11/wijzigingen.txt`.

**Bevroren, met assert in r11.py:** silhouet (alpha-diff 0, geen losse pixel weggehaald), oogzone x18–25 y21–27 (diff 0), Jordi's twee zwarte strepen (staart 46,32–33; dij 44–45,37–43; diff 0 en nog zwart), het witte borst/buikvlak + 1 px grens eromheen (diff 0).

**Totaal: 10 pixels + 3 paletkleuren.** Per zone: kop/kuif/oor 3, kin/hals 1, manen/rug 1, buik 4, bil 2; poten, hoorns (vorm), staart, oog 0.

## Gemeten vóór de ronde
| meting | r9 | r11 | Gen 3 viervoeters (Stantler/Rapidash/Ponyta/Girafarig) | maatstaf (Skinguin/Dundragoon/Zapacha/Princadee) |
|---|---|---|---|---|
| zwarte buitenlijn per richting O / Z / W / NW | 95/96/5/1 % | 95/96/5/1 % | 42–76 / 27–87 / 0–26 / 0–6 % | 74–97 / 75–100 / 11–54 / 0–19 % |
| zwart en selout om en om op één rand | 0 | 0 | | |
| lichte kleur op de buitenrand | 0 | 0 | | |
| zwarte losse pixels midden in een vlak | 0 (alleen neus/strepen) | 0 | | |
| dubbele hoekpixels op gladde randen (overige 18 gemelde = kruisingen hoorn/kuif/oor, neus, plukjes, hoeven: bewust) | 3 | 0 | | |
| kleuren incl. transparant | 13 (+1 ongebruikt slot) | 13 | | |

## 1. Belijning (omlijningsronde volgens de gids)
Gids: *"we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide"*; *"The 'outline shadows' are always black"*; *"lighter pixels on the inside of the outline are a far better idea"* (en niet erbuiten); E2 checklist: overlap = lijn in de outline base, niet zwart.

**Gevonden:** de verdeling zwart/selout klopt al met de maatstaf (tabel); de outline base per onderdeel is de eigen donkerste tint (vacht D, staal A, zwart alleen rechts/onder). Wel:
- 3 dubbele hoekpixels (lijn 2 px dik in een binnenhoek): kin/hals (19,30), manen/rug (33,33), kuif (21,14).
- Bovenhoek van het rechteroor (28,18) zwart terwijl de rand daar naar boven wijst (lichtkant); de rest van die oorrand is D.
- Buik over de verre achterpoot: het model heeft daar een lijn (lijnfractie 23–49 %), de sprite niet; het vlak liep in M/N/M over in de poot (leest als ruis).

**Veranderd (7 px):** de drie hoekpixels → vulling van de buren (modelhelderheid 140/93/110 → N/S/S); (28,18) zwart → D; buiklijn (37,45)(38,45)(39,45) → D, verbindt de bestaande D-uiteinden (36,46) en (40,45), per kolom de cel met de hoogste modellijnfractie. Binnenlijn in D, niet zwart.

## 2. Schaduw
Gids: licht linksboven, sikkel die de vorm volgt; KERN: schaduw uit de modelhelderheid, niet met de hand verzinnen.

**Gevonden:** schouderschaduw, buiksikkel (N onder de buik), bilhooglicht (H), donkere rugband en verre poten in M komen uit het model en kloppen. De sprite ligt overal ±1 tintstap donkerder dan het model (bewuste Gen 3-diepte uit eerdere rondes), relatief klopt hij. Twee fouten:
- (36,45) M was donkerder dan het vlak eromheen (model 196 = licht) en brak de buiksikkel.
- (43,39)(44,39) los H-vlakje van 2 px naast de dijstreep (restant van strepen-weg); model 193/197 = gewoon flank.

**Veranderd (3 px):** (36,45) M → N (sluit de sikkel boven de nieuwe buiklijn aan); (43,39)(44,39) H → L. Geen vlakken gemiddeld of gladgestreken.

## 3. Kleurtinten
Gids rule 1/3/5: tinten behouden hun relatieve helderheid; outline is ook een kleur; *"find yourself some other sprite ... that has approximately the color you're looking for"*.

**Gevonden:** vacht 7 tinten in stappen van ±30 (67/96/126/156/186/217/247) = goed (Taillow-stappen). Maar het staal lag bovenop de vacht: CIELAB-afstand staal-3 ~ D 4,7; staal-4 ~ N 3,9; staal-5 ~ H 2,1 (bijna-dubbel: staal niet te onderscheiden van vacht). Ongebruikt paletslot #1C2436 (bijna zwart).

**Veranderd (palet, geen pixels):** staal naar Steelix (`normal_gba.pal`: blauw in de schaduw, lichter = neutraler), zelfde rol per tint:
| tint | r9 | r11 | helderheid | dichtste andere paletkleur (ΔE) |
|---|---|---|---|---|
| diepe reflectie | #424B5B | #3E4A68 | 74 | D 12,5 |
| midden | #8D96A6 | #7E8DAA | 140 | M 11,7 |
| licht | #D3D9E3 | #CCD7EA | 214 | H 7,2 |
Glans blijft W (#F5F7F9), lijn A/zwart; stappen staal 47 → 74 → 140 → 214 → 247 (diepe reflectie + harde witte glans). Drie proeven vergeleken (blauwer = te blauw tegen het zilveren model; lichter = te dicht bij H); deze gekozen. Palet compact: 12 kleuren + transparant.

## Eindoordeel: PASS (uitvoering)
Belijning, schaduw en tinten voldoen aan de gids en liggen in lijn met de maatstaf-sprites en de Gen 3-viervoeters; bevroren zones diff 0.

**Ter info voor Jordi (niet veranderd):**
- Oog nog open (A, B1–B3).
- Hoornkleur is nu iets koeler blauw (Steelix-achtig) om het staal van de vacht te scheiden; terug naar het oude palet kan met alleen een paletwissel.
- Linkerkant van de snuit is N (model daar ±10 donkerder dan het voorhoofd); bewust gelaten.
- Linkeroor: verloop L-N-M uit het model (in r3 bewust als modeldetail bewaard); bovenrand oor is een rechte lijn van 6 px (vorm, niet aangeraakt).
