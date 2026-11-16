# Studie Gastly Gen 3 (anim_front.png bovenste 64x64, normal.pal) — voor Dustly r6
Gemeten met script; vergroting: `studie.png` (12x + palet met L/hue/verzadiging/aantal px).

## (a) Belijning
- Zwart (F, 16,16,16; 59 px) alleen rond de **dichte bal** en in het gezicht (ogen, mond), en dan vooral aan de **schaduwkant** (rechts/onder de bal: "FCC"-rand rij 22–45). Linksboven gaat de donkere bal (9) zonder lijn direct over in het gas.
- Lijndikte 1 px; binnen het gezicht rode lijnen (3/4) naast zwart.
- **Het gas heeft nergens een buitenlijn**: de rand van de wolk is de lichtste gastint (A) direct tegen de achtergrond.

## (b) Schaduw
- Bal: 3 tinten (9 L48 = 193 px, 8 L90, 7 L114) met een groot **glansvlak/sikkel linksboven** (7/8, ±50 px); de rest van de bal vlak donker.
- Gas: 3 tinten in **concentrische banden**: donkerst (C, L114) vlak om de bal, dan B (L164), buiten A (L188). Licht wordt dus naar buiten toe lichter (doorschijnend), niet per bult belicht.
- Clusters groot (gasbanden 186–309 px per tint); enkel aan de uiterste rechterrand een kort dambord-dither A/B (rij 27–31, x49–55).

## (c) Kleur
- Gas: hue constant 312°, verzadiging stijgt naar donker (A .19 → B .22 → C .29 → 8 .36); helderheid A/B/C = 188/164/114 (stappen 24 en 50).
- Donkerste baltint 9: hue 300° (−12° hue shift naar blauwpaars), s .28, L48. Lijn: neutraal bijna-zwart L16.
- Contrast bal ↔ gas: L48 tegen L114 (±66); gas onderling ±24–50. Gezicht: wit 255 en rood (9°, s .74–.91) als enige felle kleur.

## Toegepast op Dustly r6 (palet A-familie, hue 336°)
- Palet: 6/5/4 = v .84/.74/.55 met s .19/.22/.29 (L188/161/114, = Gastly A/B/C); kern 3 hue 324° (−12°) L72 (iets lichter dan Gastly's 48, Jordi: "minder zwart"); lijn 2 L49, buitenlijn 1 L26 (pruim i.p.v. zwart). Rand (7/8), wit en tandgrijs ongewijzigd.
- Belijning: buitenlijn alleen nog rond de dichte donkere kern; randpixels waar het gas (4/5/6) aan de binnenkant ligt krijgen de gastint van hun binnenburen (geen lijn, zoals Gastly). Bultlijnen in het gas tonaal (één tint donkerder, geen lijnkleur).
- Schaduwverdeling: niet verschoven (vormen en licht/donker komen uit het model; verplaatsen zou tekenen zijn).
