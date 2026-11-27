# r14 – rechte-lijnenreparatie (regionale Hitmonlee, glas)

Opdracht: Jordi (27 nov): "ok nog even een rechte lijnen check doen, de benen hebben slordige rechte lijnen ipv de vorm die hitmonlee hoort te hebben, is opnieuw getekend? arm ook, kijk naar de oorspronkelijke hitmonlee hiervoor. Bovenop hoofd ook een lange rechte lijn" + "het ziet er iig niet uit, dat moet nog gefixed worden, verder is de sprite goed".
Daarom: basis = `eindkeuring/ek2.png`, alleen lokale reparaties; al het andere pixel-gelijk aan ek2.

Bestanden: `r14.png` (64×64 geïndexeerd, palet van ek2 ongewijzigd: 15 kleuren + index 0), `r14_8x.png`, `rechte_lijnen_overlay.png` (ek2, rood = gerepareerd, geel = ook recht in het model), `diff_ek2_r14.png`, `vel.png` (ek2 | r14 | model op dezelfde schaal | Gen 3-Hitmonlee, plus diff en 1×/2× licht/donker), `log.txt` (elke gewijzigde pixel met reden), `bouw.py`, `vel.py`.
Meetgereedschap: `recht.py` (runs in omtrek en binnenlijnen), `uni.py` (gelijkmatige oppervlakgewogen bemonstering van het natieve model met schaal/offset), `masker.py`/`warp.py` (globale vergelijking), `ringmeet.py` (lijnfractie + ringtint per spritepixel uit het model).

## Rechte-lijnencheck (ek2)
Detector: horizontale/verticale randruns ≥ 5, binnenlijn-runs ≥ 4. Per run gemeten tegen het model: het natieve masker (136×148) lokaal gefit op ek2 (schaal + subpixelverschuiving per zone, oppervlakgewogen, drempel 0,5) en de subpixelrand per rij/kolom.
| run in ek2 | model | r14 |
|---|---|---|
| bovenop de romp rij 21, 10 px (kol 17–26), daarna rechts 2-3, links meteen een 45°-trap | model is rond: rand op kol 17 = 21,50, kol 26 = 21,33, kol 31 rij 23 = dekking 0,25 | gerepareerd: top 8, rechts 8-3-2-1-1, links 8-2-2-1-1-1 (≤ 0,5 px van de modelrand) |
| trapbeen: ladder van 6 volle rechte ringlijnen (rij 11–22) + rechterrand kol 48 10 rijen recht | model: ringlijnen zijn bogen (uiteinden ±1 rij hoger dan het midden, gemeten in de lijnfractie), dekking kol 48 laagst op rij 13/15/18 | gerepareerd (zie onder) |
| standbeen: ladder van 5 volle ringen, linkerrand kol 52 6 rijen recht | model: kol 51 heeft dekking ≥ 0,5 (ek2 miste die), ringen puilen per ring uit (geribbelde rand) | gerepareerd (zie onder) |
| nabije arm: rechterrand 16,15,15,15,15,14,14,14 (onderarm even breed) | model: 16,15,15,14,14,14,13,13 (taps) | gerepareerd |
| linkerwand romp: kol 10 rij 29–33 (5) en kol 12 rij 37–43 (7) | ook recht in het model: natieve linkerrand x=21 over 11 natieve rijen en x=24 over 15 rijen; ek2 volgt het model hier exact (3-5-3-boog van de koepel, dan de schouderbol) | niet veranderd (zou hertekenen zijn) |
| zool trapvoet rij 0 (9), verre arm kol 37 (6), onderkant romp rij 42/46, standvoet kol 56 | ook recht in het model (zool = plat) | niet veranderd |

## Hoe de ringen naar de Gen 3-Hitmonlee zijn gepixeld
Gen 3-Hitmonlee (`graphics/pokemon/hitmonlee/anim_front_gba.png`, frame 1, 8×): de spiraal is per ring licht aan de lichtkant (wit/lichtgrijs) en donker naar de schaduwkant, ringlijnen 1 px in een donkere eigen tint, en de buitenrand is geribbeld (elke ring een eigen 1-px-stap), nergens een rechte ladder. Overgenomen op ons model (vorm, aantal ringen, kleur en pose van ons model):
- **Trapbeen** (rij 12–21): ringlijnen als bogen (buitenste binnenkolommen 1 rij hoger dan de middelste 3, zoals het model), lichtkant-uiteinde van elke boog in donkerrood 3 i.p.v. 2 (taps); volle lijnen rij 11 (onder de voet) en 22 (overgang naar het doorschijnende deel) blijven. Zes lijnen zoals ek2. Rechterrand ingekeept op de lijnrijen 13, 15, 18 (ribbels, modeldekking daar 0,67/0,78/0,44); linkerribbels van ek2 (13, 15, 18) blijven.
- **Standbeen** (rij 44–53): te smal (3–4 px) voor bogen (gaf een zigzag); lijnen blijven op ek2-rijen 44, 46, 48, 51, 53, maar de rand is nu geribbeld aan beide kanten: banden tot kol 51 (model), lijnrijen ingekeept op kol 52.
- **Bandtinten** per ring (beide benen): licht → donker van links naar rechts zoals Gen 3 en zoals het model per band meet (bleek links, oranjerood rechts): trapbeen eerste bandrij 15-7-6-5-5, tweede 7-6-5-5-4; standbeen 7-6-5-4 / 6-5-5-4. Alleen bestaande paletkleuren.
- **Arm**: 4 pixels van de rechterrand weg (dekking < 0,5) en de nieuwe rand zwart, zodat de onderarm taps naar de polsring loopt zoals in het model. Dunne vingers, polsring, ovaal oog, stompe teentjes ongemoeid.

## Pixels die niet 1-op-1 uit ek2 komen: 86 (silhouet 13)
koepel 5, arm 8, trapbeen 50, standbeen 23 — alles in `log.txt`. Buiten deze zones diff 0 (`diff_ek2_r14.png`).
Niet direct uit het model: de bandtint-templates (tinten gekozen naar Gen 3 + modelmeting, geen modelpixels), de lichtkant-uiteinden in 3, en de inkepingen op rij 46/51 van het standbeen (modeldekking ±0,5).

## Twijfelpunten
1. Linkerwand bewust niet veranderd: het model is daar zelf recht (gemeten). Als Jordi daar toch een rondere schouderbol wil, is dat een vormkeuze buiten het model: eerst vragen.
2. Trapbeen: periode ±2 px (6 lijnen in 12 rijen, zoals ek2 en het model) maakt de bogen op 8× wat druk; op 1×/2× lezen ze als ringen. Minder ringen (periode 3, Gen 3-banden van 2 px) zou rustiger zijn maar het aantal van het model veranderen: niet gedaan.
3. De bleke linkerkolom van het trapbeen vormt een doorlopend glanslicht langs de cilinder (zoals de witte kolommen in de Gen 3-spiraal); gewenst, maar Jordi laten kijken.
4. Geen verse keurder gedaan (opdracht = makerronde); r14 heeft nog een eindkeuring nodig vóór Jordi.
