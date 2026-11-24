# Proef tintzones: Gnomad (24 nov)
Bron: `../../../gnomad/af/gnomad.png` (niet aangeraakt). Resultaat: `na.png`; vel `voor_na.png` (voor | na | Makuhita | Jigglypuff | Banette, 6× en 1×); `diffmasker.png` (grijs = sprite, groen = bevroren gezichtszone, rood = gewijzigd). Scripts: `maak.py` (alleen gerichte pixellijsten + 3 paletkleuren), `bewijs.py`, `vel.py`.

## Wat per zone veranderde (62 px, alle per pixel benoemd in `maak.py`)
| Zone | px | Wat |
|---|---|---|
| Muts buitenlijn | 4 | lijn linksboven overal in eigen donker lila (2 i.p.v. losse 3-pixels); 2 airbrushpixels langs de rand (3/4 tussen lijn en licht) → licht |
| Muts randplooi | 8 | de plooi boven de omgeslagen rand was een streepjeslijn (22·4444·22); nu één doorlopende 1-px-lijn die de rand volgt en in de schaduwzone rechts verdwijnt |
| Muts rand | 4 | rand links één lichte band (losse 4-pixels in de 5-band weg), onderkant één 3-zone (losse 4-pixels weg) |
| Muts flap | 16 | tweede, parallelle vouwlijn (kolom 41) weg, zodat er één vouwlijn is; de lichte 4-rand langs de schaduwkant van de flap (ring) → flap is één schaduwvlak onder een belichte bovenkant |
| Muts punt | 2 | los lichtpixel in de punt → belichte bovenkant van het omkrullende puntje (3 px) |
| Lijf romp | 7 | losse 7-vlekjes onder de snor weg; romp één grondtint |
| Lijf sikkel | 7 | 6-vlekjes in de schaduw rechts weg; schaduw is één 7-sikkel aan de rechterkant met harde grens |
| Hand links | 9 | lijn aan de lichtkant in 6 (was 7); armpje boven licht / onder schaduw; hand licht linksboven, sikkel rechtsonder; knokkelvlekjes weg, pols- en okselijn (1 px, 6) blijven |
| Hand rechts | 5 | sikkel rechtsonder toegevoegd (had bijna geen schaduw); buitenlijn schaduwkant zwart |

Palet: lila 3/4/5 iets verzadigder (137,119,170 → 130,104,178; 184,163,211 → 178,150,224; 205,183,230 → 212,190,246). Lila 2, roze, crème, bruin, blauw ongewijzigd (zit in de gezichtszone). 15 kleuren + transparant, mode P 64×64.

## Bewijs (`python3 bewijs.py`)
- silhouet-diff (alfa): **0**
- gezichtszone (neus, snor, wang, roze tussen de snor, en de zwarte/2-lijn eromheen): 397 px, diff index + RGB: **0**
- gewijzigde pixels: 62

## Zelf nog zwak
- De muts blijft een groot vlak 4 met de lichtvlek linksboven; naast Banette is de stof nog vrij glad (geen plooistreepjes). Ik heb geen plooien toegevoegd die niet in het model staan.
- Onderrand van de muts rechts (rij 25–28) houdt een band 4 tussen twee 3-zones; leest als rand, maar is het minst duidelijke stuk.
- Roze is niet verzadigder gemaakt (zelfde paletindexen als de neus, die bevroren is); de "pastel"-indruk van het lijf blijft daardoor deels.
- Broek/laarzen (losse lichtblauwe vlekjes in de laarzen) en de zwarte riemlijnen niet aangeraakt: buiten de opdracht.
- Buitenlijn: was al grotendeels selout (muts 2, handen 6, broek 9); de echte winst zit in de zones, niet in de lijn.

# Ronde 2 (opdracht coördinator: meer contrast, romp met snorschaduw, broek en laarzen)
Resultaat: `na_r2.png`, vel `voor_na_r2.png` (voor | r1 | r2 | Makuhita | Jigglypuff, 6× en 1×), `diffmasker_r2.png`. Script `maak_r2.py` (bouwt op `na.png`, alleen pixellijsten), `vel_r2.py`. Bewijs: `NA=na_r2.png python3 bewijs.py`.

## Per zone (r1 → r2, 169 px; t.o.v. het origineel 191 px)
| Zone | px | Wat |
|---|---|---|
| Muts onderrand | 27 | 4-band rechts onder de muts (rij 24–27) is in de 3-schaduwzone opgenomen |
| Romp, snorschaduw | 33 | slagschaduw van de snor als één 7-zone van ±2 px direct onder de snor (links, midden en onder de rechtersnorhelft) |
| Romp, rechts | 17 | schaduw rechts in twee harde zones: 7 en aan de buitenkant een diepe 6-zone; de verticale 8-strook (rij 36–41) is het licht op de bolling |
| Handen | 7 | diepste schaduw (6) in de hoek rechtsonder van de sikkel |
| Broek | 24 | lichtzone (lichtblauw) linksboven op de bolling, schaduwzone rechts als één vlak; losse vlekjes weg |
| Been links (dichtbij) | 22 | licht aan de voorkant (scheen, bovenkant voet), schaduw achter en onderzool als zone |
| Been rechts (veraf) | 19 | donkerder: grondtint donkerblauw met middenblauw alleen aan de voorkant; geen lichtblauw meer |

Palet: lila 3 (122,92,182), 4 (180,148,230), 5 (218,198,255): grotere stappen, diepere schaduw. Blauw 9 (44,92,140) donkerder, b (140,204,244) helderder; a ongewijzigd.
Roze: geen eigen paletslots voor de romp gemaakt. Er zijn geen bijna-dubbele tinten buiten het gezicht om samen te voegen: alle 15 slots zijn in gebruik (lila 4, roze 3, crème/bruin 3, blauw 3, riem 1, zwart 1), en roze 6/7/8 zitten in de neus. Het contrast op de romp komt daarom uit grotere en dieper liggende zones (6 als echte zone), niet uit nieuwe tinten.

## Bewijs r2
- silhouet-diff (alfa): **0**
- gezichtszone 397 px: diff index + RGB **0**
- 15 kleuren + transparant, mode P 64×64

## Zelf nog zwak (r2)
- Het roze blijft het originele (vrij pastel) roze omdat de slots gedeeld zijn met de neus. Echt warmer/verzadigder kan alleen als de neus mee mag of als er een slot vrijkomt (bijv. lila 5 schrappen of de riem op een andere tint).
- Lila 2 (lijnkleur, zit in het gezicht) is grijzer dan de nieuwe, verzadigde 3; in de schaduwzones leest de vouwlijn daardoor als een grijze lijn i.p.v. een donkerdere tint.
- Snorschaduw: 2 px band; Jordi vond een roze rand om de snor eerder raar (r8). Het is nu een schaduwzone en geen rand, maar daar moet Jordi naar kijken.
