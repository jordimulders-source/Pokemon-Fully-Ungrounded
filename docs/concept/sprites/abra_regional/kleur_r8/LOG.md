# Regionale Abra, kleur_r8 (maker, 15 nov)

Jordi over r7 (letterlijk): "de zwarte belijning aan de buitenkant is meer dan bij andere gen 3 sprites of niet? Daarnaast zijn er nog steeds best veel rechte lijnen, rechterkant van de staart, rechterkant van het lichaam, beide armen, linkerkant hoofd. Controleer deze even allemaal."
Basis: `../kleur_r7/abra_r7_A.png` (Jordi koos A). Bevroren: ogen (8 px, assert), pose, kleuren A, vlekjes.

Reproduceren (vanuit `kleur_r8/`): `python3 maak_r8.py` (edits als data met oude waarde = assert en reden) → `abra_r8.png`, `abra_r8_curve.png`; `TMPDIR=<scratch> python3 maak_vel.py` → `abra_r8_8x.png`, `abra_r8_curve_8x.png`, `vel.png`, `closeup.png`; `python3 randmeting.py <png>...` = rand-zwartmeting.

## Opleveringen
- **`abra_r8.png`**: buitenrand naar het Abra/Kadabra-recept + de curven die het model op natieve resolutie zelf heeft (staart rechts, linkerarm buitenkant). 50 px gewijzigd, silhouet 3 px.
- **`abra_r8_curve.png`** (variant, Jordi beslist): r8 + lichte curven op de plekken waar het model recht is (kop links, lijf rechts, linkerarm binnenkant, rechterarm). 65 px t.o.v. r7, silhouet 9 px.
- `vel.png`: r8 8× | r8_curve 8× | r7 A 8× | model zelfde schaal | echte Abra 8× | 1×/2× licht/donker/groen.
- `closeup.png`: per onderdeel r7 A | r8 | r8_curve | model (Gemini verkleind tot 12× per spritepixel, rode lijn = r8_curve-silhouet).

## 1. Buitenrand
**Meting** (`randmeting.py`: figuurpixels die met 4-buren aan transparant/beeldrand grenzen; aandeel donkerste paletkleur; echte sprites eerste frame van `anim_front.png`):

| sprite | rand px | zwart |
|---|---|---|
| Abra | 191 | 40,3 % |
| Kadabra | 262 | 40,8 % |
| Sneasel | 275 | 41,5 % |
| Zigzagoon | 165 | 50,3 % |
| **r7 A (vóór)** | 248 | **60,9 %** |
| **r8 (na)** | 248 | **42,7 %** |
| r8_curve | 247 | 42,5 % |

**Studie echte Abra/Kadabra** (per index, op richting van de rand: licht = open naar boven/links, schaduw = open naar onder/rechts):
- Abra: lichtkant 72 px: 14 zwart (F), 50 donkere lichaamstint (E = (90,57,8)), 8 licht; schaduwkant 70 px: 45 zwart, 23 E; beide (dunne delen) 49: 18 zwart, 29 E.
- Recept: E (donkere geel) op kop links/boven, oor rechts, handen en voeten bijna helemaal (F alleen aan de rechter-/onderpunt); F op kop rechts, onderkanten en tussen de bruine platen. Kadabra: rechterkant van het gele lijf en de staart óók E, F pas aan de onderkant.
- r7 A had de lichtkant al goed (12 zwart / 101), maar de schaduwkant 100 % zwart (100/102) en dunne delen 39/45.
- r8: lichtkant 12/101 zwart (ongewijzigd), schaduwkant 74/102 (Abra 45/70), dunne delen 20/45.

**Regel in r8** (één kleurverdeling per rand, geen losse K tussen L of andersom: gecontroleerd met script, 0 gevallen; geen 2×2-zwartblokken; geen vulkleur op de rand):
- **L** (lijnkleur huid (60,54,80)) = de donkere huidtint van het recept: kop rechts onder de oorkerf, staart boven-rechts en rechterkant, binnenrand staartlus, onderlijf rechts, linkervoet (links + rechterkant scheen), linkerhand (vingers rondom behalve de onderkant), staartpunt.
- **K blijft**: onderkanten (staartbodem, bodem dij/rechterhand boven de staart, voetzool (16–18,56–57), vingerbodem (22–25,54)), tegen de donkere platen en de kaak (L is lichter dan plaat 1, dus daar zou L als lichte rand lezen), het gat arm/lijf, oorpunt + kerf (de snede), staartaanzet onder het lijf (45–49,46–47; slagschaduw, KEURING r7) en de vingertoppen van de rechterhand.
- Zwart totaal 17,5 % (was 21,6 %).

| pixel | oud → nieuw | reden |
|---|---|---|
| (50,47) (51,48) (52,49) (53,50) (54,51) | K → L | A: staart boven-rechts, loopt van het lijf weg (Abra/Kadabra staart boven E) |
| (55,53) (55,54) (55,55) (54,57) | K → L | G: staart rechterkant (Kadabra rechterkant huid E); K vanaf (53,58) waar hij naar de bodem draait |
| (34,19) (35,20) (35,21) (35,22) (35,23) (36,24) | K → L | F: kop rechterkant onder de kerf tot de plaat; oorpunt (34,15) en kerf (35,16)(35,17)(34,18) blijven K |
| (43,43) (43,44) | K → L | H: rechterkant onderlijf (huid s, tussen plaat en staartaanzet) |
| (50,52) (51,53) | K → L | L: binnenrand staartlus, naar linksboven gekeerd; sluit aan op L/T eronder |
| (8,50) (9,51) (10,51) (11,51) (12,51) (13,52) (14,53) (15,56) | K → L | B: linkervoet hele linker-/linksonderkant (Abra: voeten E links, linker teenpunt E); sluit aan op L (15,54–55) |
| (19,52) (18,53) (18,54) (18,55) | K → L | B: rechterkant scheen; (19,52) anders losse K tussen L |
| (21,53) | K → L | C: linkerhand vinger links, sluit aan op L (21,52) |
| (24,51) (25,52) (25,53) | K → L | C: vinger rechterkant (Abra: handen bijna helemaal E); onderkant (22–25,54) blijft K |
| (25,50) (26,50) (28,50) (27,51) | K → L | C: palm-onderkant boven het gaatje (b erboven), vingerrand (28,50) en vingertop (27,51) (anders losse K) |
| (22,61) (23,61) (24,61) (25,61) | K → L | E: onderkant dunne staartpunt (links = lichtkant); de inham (26–29,60) blijft K |

## 2. Rechte lijnen (per onderdeel tegen het natieve model, 2× de spriteresolutie)
Modelrand gemeten per natieve rij (eerste/laatste figuurpixel, in sprite-eenheden; x,0 = linkerhelft van pixel x, x,5 = hele pixel). Vergroting: `closeup.png`.

| onderdeel | model (natief) | r7 (runs) | oordeel | r8 | r8_curve |
|---|---|---|---|---|---|
| **staart rechts** | 1,1,1 diagonaal → 55,0 (1,5 rij) → 55,5 (4 rijen) → 55,0 (1,5 rij) → 1,1 diagonaal | 1,1,1,1,**5**,1,1,1,1 | model heeft een bocht: de 5 rechte rijen + abrupte overgang zitten niet in het model | **1,1,1,2,3,2,1,1,1** | idem |
| **linkerarm buiten** | 24,0 / 23,5 / 22,5 / 22,0 / 21,3 / 19,8 / 18,5: versnelt naar de hand (bol) | 2,1,2,1,1 (heen en weer) | model is een vloeiende bocht | **2,2,1,1,1** | idem |
| **linkerarm binnen** (rand van het gat) | 27,0 / 26,5 / 26,5 / 26,0 ×7 | x26 rij 39–43 (5) | model op natieve resolutie recht (alleen bovenaan een halve pixel scheef) | ongewijzigd | x27 rij 39, x26 rij 40–43 (schouder iets breder) |
| **rechterarm** (binnenlijnen x38 en x41) | lichte buis met donkere lijnen, beide lijnen recht rij 36–40, knik pas bij de elleboog | linkerlijn 5,1,2,1,1 | model recht | ongewijzigd | linkerlijn **3,3,2,1,1** (knikt een rij eerder naar de elleboog; arm wordt naar onder 1 px breder) |
| **lijf rechts** | 44,5 rij 36–39 (8 natieve rijen), 43,5 rij 40–45 (12 natieve rijen), 44,0 halve inham rij 35 | 45:2, 46:1, 45:2, 44:**6**, 43:**5** | model echt recht (twee verticale stukken) | ongewijzigd | 46:1, 45:**3**, 44:**4**, 43:**6** (geleidelijk oplopend = bolle rug die verticaal wordt) |
| **kop links** | 18,0 (oor) → 18,5 → 19,5 → 19,9 → 20,0–20,5 jitter rij 25–34 | 4 (oor), 2, **9**, 1, 1 | model op natieve resolutie recht (± halve pixel jitter) | ongewijzigd | 4 (oor), **3, 6, 3**, 1: holte onder het oor, bolle wang, kaak 1 px naar binnen |

### Silhouetpixels
| pixel | r8 | r8_curve | reden / afwijking van het model |
|---|---|---|---|
| (55,52) | weg | weg | model rij 52: 55,0/55,5 → halve pixel; curve 2,3,2 |
| (55,56) | weg | weg | model rij 56: 55,5/55,0; curve 2,3,2 |
| (22,41) | weg | weg | model rij 41: 22,5 (halve pixel); runs 2,2,1,1,1 |
| (19,25) | – | erbij | model 19,94 → ~1 px buiten het model |
| (20,32) (20,33) | – | weg | model 19,94 → ~1 px binnen het model; kaak blijft K-omrand, plaatvulling 1 → 1 px smaller |
| (45,34) | – | erbij | model 44,5/44,0 → ~1 px buiten |
| (44,39) | – | weg | model 44,5/44,0 → ~1 px binnen |
| (27,39) | – | erbij | model 27,0 (bovenste natieve rij) → halve pixel buiten; gat 1 px kleiner |

### Overige pixels door de curven
| pixel | oud → nieuw | waar | reden |
|---|---|---|---|
| (54,52) (54,56) | s → L | r8 | nieuwe buitenrand staart (rechterkant = L) |
| (53,56) | b → s | r8 | schaduwband langs de rechterrand loopt door (rij 55 s s, rij 57 s) |
| (23,41) | s → L | r8 | nieuwe buitenrand linkerarm (lichtkant L) |
| (20,25) | L → b | curve | was rand, nu huid zoals (21,25) |
| (21,32) (21,33) | 1 → K | curve | nieuwe kaakrand |
| (44,34) | K → 1 | curve | plaat loopt door tot de nieuwe rand |
| (26,39) | K → s | curve | was rand, nu huid van de arm |
| (37,39) (37,40) | 1 → K | curve | linkerlijn rechterarm naar x37 |
| (38,39) (38,40) | K → b | curve | arm 1 px breder naar de elleboog (lichte kant) |

## Controle
- Ogen (22,28)(23,29)(24,30)(24,31), (30,27)(29,28)(28,29)(28,30): ongewijzigd (assert, beide versies).
- 9 kleuren + transparant (palet en indexen gelijk aan r7 A); geen nieuwe tinten.
- Op de rand: geen vulkleur (s/b/h), geen losse K tussen L of L tussen K (script), geen 2×2-zwartblokken.
- Vlekjes (3/2/1 op de huid) niet aangeraakt.

## Zelf bekeken (8× naast model en echte Abra)
- r8 leest zachter en meer Gen 3: zwart alleen nog onder (staart, voeten, dij) en tegen de platen; de handen en de linkervoet hebben nu zoals bij Abra een donkere huidtint als rand.
- Staart rechts is nu een ronde bocht; linkerarm loopt vloeiend uit naar de hand.
- Nog recht in r8 (want recht in het model): kop links (9 rijen x20), lijf rechts (6 + 5), rechterarm (twee parallelle lijnen van 5), linkerarm binnenkant (5). Die zitten in `abra_r8_curve.png`; de kaak wordt daar 1 px smaller.
- Twee eerdere probeersels teruggedraaid omdat ze een losse kleur op de rand gaven: (33,56) K→L (losse L) en de vingertop (27,51) als K tussen L (nu ook L).

## Open voor Jordi
1. **r8 of r8_curve** (of per onderdeel: kop links / lijf rechts / linkerarm binnen / rechterarm).
2. Rand-zwart 42,7 % (Abra 40,3, Kadabra 40,8). Lager kan nog met de staartbodem of de onderkant van de dij, maar die zijn bij Abra/Kadabra ook zwart.
