# Gnomad – sprite r3 (maker-agent, 22 nov)

Basis: `../sprite_r2/gnomad_A.png` (bruine riem). Script: `r3.py` (een assert bewaakt dat er buiten riem en broekrand niets verandert), vel: `vel.py`.
Jordi: "kijk eens hoe machoke de riem goed doet".

## Machoke bestudeerd (`graphics/pokemon/machoke/anim_front.png`, x22–43, y28–37)
- Direct boven de band ligt een rij zwart (1). Onder de band zit zwart, met een paar pixels van de bandkleur ertussen.
- De band zelf is 2–3 rijen vlak donkergrijs (74,74,98), bijna zonder tintverloop.
- De gesp is goud in 3 tinten (131,115,41 / 205,189,98 / 238,230,139). Hij heeft een eigen zwarte omlijning, steekt iets boven en onder de band uit en heeft een glanspixel.

## Toegepast op Gnomad (de boog volgt de bol, zelfde bovenrand als r1 en r2)
- Riem in het midden 5 rijen: zwart, 3× band, zwart. Op de flanken 4 rijen: zwart, 2× band, zwart.
- Band vlak donkerbruin (104,68,48). Links op de bovenste bandrij (x15–21, lichtkant) een klein stukje lichtbruin (174,130,90).
- De broekrij onder de riem blijft in schaduw, zoals in r2.
- **A (aanvulling, naar Jordi's foto `referenties/gesp_jordi.png`):** rechthoekige framegesp, 7×6 inclusief zwarte omlijning, op x22–28, y43–48. Hij steekt 1 px boven de band uit.
  - Open midden: de bruine band is erdoorheen zichtbaar.
  - Pin als streep van 1 px in het midden, van boven naar beneden.
  - Zilver uit bestaande tinten: lavendel licht (184,163,211) linksboven, lavendel schaduw (137,119,170) rechts en onder, glanspixel crème licht linksboven.
  - De eerdere crème gesp is vervangen.
- **B:** dezelfde band zonder gesp.
- 16 kleuren, niets opgeofferd. De gesp gebruikt de crèmetinten van de snor; een echte goudtint zou een andere kleur kosten.

## Diff t.o.v. r2-A
| | riem + broekrand | elders |
|---|---|---|
| A | 113 px | 0 |
| B | 99 px | 0 |

Controle: geen lichte kleur op de buitenrand, geen losse zwarte pixels.

## Eigen zwakke punten
- Zwart is nu 21 % van de figuur (Gen 3 ±12–19 %), door de twee zwarte riemlijnen.
- Het zilver is lavendelgetint (muts-tinten). Op 1× leest het als licht metaal, maar op 8× is het duidelijk lila.
- Een echt grijs kost 1–2 kleuren. Dat kan alleen ten koste van bestaande tinten, bijvoorbeeld de lichtbruine selout van de snor laten vallen voor donkerbruin. Dat verandert de snor; nog niet gedaan.
