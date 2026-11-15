# Keuring welp r10 (onafhankelijke keurder, 15 nov)

**Oordeel: FAIL** (dichtbij; oog en ver oog zijn nu goed, lijf staat, maar de snuitpunt leest als uitstekend donker balkje en de tong is nog steeds een rechte staaf met een open rand; precies de gezichtsonderdelen waar Jordi op let).

Werkwijze: eerst blind; daarna `r8/keuring.md` gelezen en r9→r10 gedifft (93 px, allemaal in de kop). Vergelijkingen: sprite 8× naast het model (bbox model x 97–942 / y 194–942 → sprite x 7–57 / y 18–63); kop op 12–24× naast uitsnedes van het model (oog, ver oog, snuit); 1× en 3× naast Growlithe, Vulpix, Skitty (`anim_front_gba` + `normal_gba.pal`) en `af/steenjaguar.png`.

Paletindex (r10): 1 zwart (22,11,17), 2 (59,34,36), 3 (98,64,60), 4 (136,96,88), 5 (170,128,114), e (204,166,148), 6 lila-donker, 8 lila, 9 oog-licht (188,178,164), a wit, b beige, c tong (230,140,134), d tong-licht, f tong-donker.

## Hoofdvraag
Op 1× een leesbare, zittende welp die zijn poot likt; past in formaat en kleur naast Growlithe/Vulpix en de volwassen vorm; het facettenidee (licht boven, schaduwkant borst/onderlijf) staat, geen kussen. Het gezicht is ten opzichte van r9 duidelijk beter: het oog volgt het model (glans linksboven de pupil, oogwit achteraan), de voorhoofdsband heeft nu een binnengroef, de glimlachcurve loopt omhoog naar de wang zoals in het model. Maar op 8× naast het model zijn er nog twee dingen die direct opvallen: de neus is geen driehoek maar een donkere plank die links uitsteekt, en de tong hangt als recht roze staafje in plaats van breder naar links over de poot te krullen. Zo zou ik hem nog niet trots laten zien; na de drie MOET-punten (±10 px) wel.

## Ver oog (Jordi's vraag)
**Leest nu goed.** Model: op de kopcontour een smal oog van ±2×3 sprite-px: zwart lid boven, witte kolom, donkere kolom rechts. Sprite: (11,26)+(12,26) zwart lid, (11,27) wit, (11,28) licht, (12,27–28) zwart, contour (10,26–30). Dat is exact dezelfde opbouw als het verre oog van Growlithe (wit kolommetje + zwart kolommetje, 3 hoog). Geen losse pixels meer: het is een omsloten oogje. Laten zo.

## Eis 1: trouw aan het model
| Onderdeel | Oordeel |
|---|---|
| Oren | OK (ver oor wat klein, zie MAG) |
| Voorhoofdsband | OK: gave lila band met binnengroef 3 van (14,24) naar (20,20). Groef komt rechts op de buitenlijn uit (20,20), zie MAG |
| Oog | OK, trouw aan het model; iris boven iets te licht (MAG) |
| Ver oog | OK (zie boven) |
| Snuit / neus | **AFWIJKING** (MOET 1): model = omgekeerde driehoek met punt onder; sprite = donkere rij (9–13,31) + uitstekende pixel (8,32) + vulling 3 die bijna even donker is, dus een balkje |
| Mond / glimlach | OK: lip (12–14,35), hoek omhoog (17–18,34), kaaklijn (18,35–36) volgt het model |
| Tanden | OK: boven (11,35–36) en (15,35), onder (16,37–38) |
| Tong | **AFWIJKING** (MOET 2): rechte staaf x12–14 y37–40, tip 2 px; model = tong die breder wordt en naar links over de poot krult (r8 MOET 2 niet uitgevoerd) |
| Poot, borst, romp, dij, voeten, staart | OK |
| Spiralen | buiten beoordeling (volgende ronde) |

## Eis 2: Gen 3-techniek
- Bruin 4 tinten + e als 4e licht (toegestaan); stappen ±30–40; belijning 1 px, gekleurd aan de lichtkant, zwart onder: OK.
- **Open buitenrand bij mond/tong** (MOET 3): (12,37) licht roze en (11,36) tand liggen direct tegen de achtergrond, (12,36) is transparant (gat tussen tand en tong).

## MOET-reparaties
1. **Neus als driehoek (x8–13, y31–33).** (13,31) 2 → 4 (bovenrand 4 breed: x9–12); (12,33) 3 → 4; (10,33) 3 → 2. Dan: bovenrand 2 op y31, vulling 3 op (9–11,32), rechter schuine rand (12,32)→(11,33) met de zwarte punt (11,33) die in het philtrum (11,34) overgaat. (8,32) blijft als neuspunt vooraan (staat ook zo in het model), maar controleer op 1× of hij niet meer als stokje leest; zo ja (8,32) → transparant en (9,32) → 2.
2. **Tong breder en naar links (x11–13, y38–40).** (11,39) 2 → c, (11,40) 2 → d; buitenlijn blijft (10,39–40) 2. Tip wordt 3 px breed en leunt naar links over de poot; groef f op x13–14 blijft.
3. **Rand dicht bij tand en tong.** (11,37) transparant → 2; (12,36) transparant → 1 (mondholte tussen tand en tong); (10,36) transparant → 2 (tand krijgt buitenlijn).

Na de reparaties de kop opnieuw op 12× naast het model leggen (geen nieuwe keurder nodig als alleen deze ±10 px wijzigen en Claude het zelf ziet; anders wel).

## MAG-punten
- Iris: (20,27) 9 → 4 of 6, zodat de iris boven donkerder is dan onder zoals in het model (nu iris en oogwit bijna gelijk licht; risico op "lege blik").
- Bandgroef: (20,20) 3 → 8 zodat de groef binnen de band eindigt en het rechtereinde gesloten is (model).
- Ver oor (11–15, y18–19) is 2 px hoog; in het model ±3–4 px. Bij een volgende ronde 1 rij erbij op (12–13,17) als dat de kopvorm niet verandert.
- Spiralen: in de spiraalronde meenemen (buiten deze keuring).
