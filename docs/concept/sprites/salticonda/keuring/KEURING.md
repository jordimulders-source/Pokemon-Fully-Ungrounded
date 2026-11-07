# Salticonda kleur3f – onafhankelijke keuring (5 nov)

Gekeurd: `../kleur3f/salticonda.png` (frontsprite, frame 1). Vel: `vel_keuring.png` (1. lijnvergelijking 4× en 1× op licht en donker; 2. Salticonda naast 18 echte sprites op 1× en 2×; 3. FAIL-uitsneden op 8×).
Coördinaten: (x, y) in de 64×64-sprite, 0 = linksboven. Indexnamen: 1 = donkerste omlijning (54,44,42), 2 = (100,86,76), 3 = (124,108,90), 11–14 = turquoise licht → donker.

**Eindoordeel sprite: nog niet goedkeuren.** 13 PASS, 4 FAIL op norm + §0, en 1 technische FAIL. Alle FAILs zijn klein en te repareren zonder de kop, de kuif, de neus of het silhouet van het lijf aan te raken (alleen R4 raakt de staart).
**Eindoordeel regional form: geslaagd.** De omzetting zandzak → pekelband → accuringen is logisch, en de regio verklaart hem.

## 1. Eerste indruk (vóór de normen en de notities)
- Op 1× leest hij meteen als een zware slang die opgerold op een kegel zit. Kop en kuif staan bovenop, het halve oog en de turquoise ringen vallen op en de staart komt rechtsonder uit. De kop is herkenbaar die van de Uyuni-Silicobra.
- Naast de Gen 3-sprites is hij **het bleekst van het hele vel**:
  - De omlijning is licht en er is nauwelijks donker. Op een lichte achtergrond lost de onderkant op.
  - Hippowdon, Torkoal en Sandaconda hebben allemaal een duidelijk donkere onder- en schaduwrand.
- De ringen zijn strak horizontaal. Hun onderste drie rijen zijn lange, evenwijdige rechte strepen. Daardoor leest het lijf ook een beetje als gestapelde banden of een bijenkorf, en minder als één slang die over zichzelf rolt.
- De staart is een dun haakje van 3 px met een turquoise stipje. Op 1× is dat nauwelijks een staart.
- Electric zie ik niet. Ground en wall zie ik wel.
- De sprite raakt de bovenrand, terwijl onderaan 3 rijen vrij zijn.

## 2. Technische check (script)
| Punt | Uitslag | |
|---|---|---|
| 64×64 | PASS | |
| Palet-PNG (mode P), ≤ 16 kleuren | PASS | 15 in gebruik (index 0–14), index 15 vrij; palet 1:1 gelijk aan de Uyuni-Silicobra |
| Index 0 transparant, `transparency=0` | PASS | index 0 = (152,208,160) |
| Open randen (schaduw- of vulkleur naast transparant) | PASS | Aan de rand liggen alleen de indexen 1, 2, 3, 13 en 14. Index 13 (middenturquoise) ligt aan de rand op (10,31–33) en (4–5,45–47). Dat is de lichtkant, dus acceptabel. |
| Losse pixels / gaten | PASS | 0 / 0 |
| Geen puur zwart | PASS | donkerste is (54,44,42) |
| Lucht rondom | **FAIL** | De rand raakt **y = 0 op x 19–24 en 27–31** (11 px, kuif). Onderaan zijn de rijen 61–63 vrij. Jordi vroeg in 3b/3d zelf om "1 px lucht boven". |
| Maten | info | 2495 px, box 62×61. Symmetrie 0,808, soliditeit 0,871, donker aandeel 0,036. Zie de tabel hieronder. |

**Maten naast de referenties** (`vormstudie/tools`):

| | Pixels | Donker aandeel |
|---|---|---|
| Silicobra | 889 | 0,23 |
| Uyuni-Silicobra | 990 | 0,09 |
| Sandaconda | 1609 | 0,32 |
| Hippowdon | 2145 | 0,20 |
| Torkoal | 2307 | 0,10 |
| Steelix | 2313 | 0,14 |
| **Salticonda** | **2495** | **0,036** |

## 3. SPRITE_NORM 1–10
| # | Punt | Uitslag | Zones / reden |
|---|---|---|---|
| 1 | Leest op 1× als Pokémon (naast 10+ echte) | PASS | Naast Hippowdon, Torkoal, Camerupt, Steelix, Sandaconda, Ekans, Arbok en Seviper leest hij als slang op een zoutkegel. Aantekening: het is de bleekste en zachtste van het vel (zie 9). |
| 2 | 3/4 links-voor, kop meer naar kijker | PASS | Kop in de 3/4-hoek van de Uyuni-kop: één oog (x 20–32, y 10–14) en de snuit naar links. Het lijf is aan de rechterkant beschaduwd, de ringen lopen 2–3 px op naar rechts en de staart zit rechts. |
| 3 | Ledematen geteld en verbonden | PASS | Geen poten. De staart zit vast aan de onderste winding (x 55–58, y 50–55). |
| 4 | Geen Escher | PASS | De kop ligt over de halsband, de windingen liggen op elkaar en de staart komt onder de onderste winding uit. |
| 5 | Geleidelijke curven, geen rechte lijnen ≥ 4 px waar rond | **FAIL** | De ringen zijn drie evenwijdige rechte runs boven elkaar (rechte lijn én banding): <br>• ring 3: **y 47, 48 en 49, elk x 14–34 (21 px)**, kleur 12/13/14; <br>• ring 2: **y 33–35, x 20–30 (11 px)**; <br>• halsband: **y 24, x 14–30 (17 px)**. <br>Op een rond lijf moet de onderrand van een ring als een ellips doorzakken, met runs van hooguit ±8 px. Volgens kleur1 "buigen ze in het midden naar beneden", maar dat gebeurt alleen aan de uiteinden. |
| 6 | Kop: verhouding | PASS | 21 van 61 rijen = 34 %. Dat past bij een eindvorm (D2: 30–35 %). |
| 7 | Ogen geïntegreerd | PASS | Donkere lidlijn (y 10–11), turquoise ring, pupil (26–27, 12–13) en glans (23,12). Gelijk aan de goedgekeurde pre-evolutie. |
| 8 | Kenmerken op 1× leesbaar | **FAIL** | **Staart x 55–62, y 46–56:** <br>• 3 px dik, met een punt van 3 px (C/E op (59–61, 47–49)); <br>• op 1× leest hij als een stip of haakje, niet als staart. <br>Jordi vroeg ook letterlijk (5 nov): "dat de staart duidelijk én een staart is maar ook een zoutkegel". Dat stond in ronde 2, die is afgekeurd, en daarna is het nooit uitgevoerd. Het staat dus nog open. |
| 9 | Omlijning: zwart/donkerst aan de schaduwkant, licht van linksboven | **FAIL** | De **onderrand (grond- en schaduwkant) is index 2 in plaats van 1, op y 53–60, x 1–32**: <br>• (1,53)–(11,58) en (12–20,59), (21–32,60); <br>• alleen x 33–45 heeft index 1. <br>Het donkere aandeel is 0,036, tegen ±0,10–0,25 bij echte sprites (E3) en 0,09 bij de eigen pre-evolutie. Daardoor lost de onderkant op 1× op een lichte achtergrond op en heeft de massa geen gewicht op de grond. |
| 10 | Geen Chernobyl | PASS | Gezicht in orde, geen losse delen. Het crème hooglicht in de halsband (16–21, 21–23) zit ook in de Uyuni-Silicobra. |

## 4. SPRITING §0
| # | Punt | Uitslag | Zones / reden |
|---|---|---|---|
| 1 | Lijf én blik diagonaal | PASS | Zie norm 2. |
| 2 | Alles geteld en verbonden | PASS | |
| 3 | Geen rechte lijnen | **FAIL** | Zelfde als norm 5 (ringen y 47–49, 33–35, 24). |
| 4 | Ogen | PASS | |
| 5 | Silhouet leest als de soort | PASS | Opgerolde slang. Aantekening onder "Voor Jordi". |
| 6 | Formaat | PASS | 2495 px valt in de band van fase 3 (1700–2600), maar het is de zwaarste sprite van het vel en ligt boven Jordi's eigen doel van 2100–2400 (zie "Voor Jordi"). |
| 7 | Pose niet stijf | PASS | De spiraal loopt 2–3 px op naar rechts en de staart krult. |

Uit FAKEMON_CHECKLIST, ter info:
- **A4** soliditeit 0,871 en **A5** symmetrie 0,808: binnen de tolerantie voor bol/kegel.
- **E3** donker aandeel 0,036: ver onder de band (ondersteunt FAIL 9).
- **D5** groei 2,52× de pre-evolutie: daarboven, zie §6b.

## 5. Concrete reparaties
Pixelbudget totaal ±120. Kop, kuif, neus, oog en het silhouet van het lijf bevroren (alpha-diff 0 behalve bij R1 en R4).

| # | Zone | Wat | Budget |
|---|---|---|---|
| R1 | Hele sprite | 1 px (liefst 2) omlaag schuiven, zodat y 0 leeg is. Onderkant komt dan op y 61/62. Geen vormwijziging. | verschuiving |
| R2 | Ring 3 (x 4–50, y 43–49), ring 2 (x 10–50, y 28–35), halsband y 24 | Banding breken: <br>• de onderrand van elke ring zakt in het midden 1 px door (ellips), runs ≤ ±8 px; <br>• de lichte rij (12) alleen aan de linkerhelft; <br>• de donkere rij (14) wordt naar rechts dikker. <br>Alleen tinten binnen de ringen; de ringdikte gemiddeld gelijk. | ±60 |
| R3 | Onderrand x 1–32, y 53–60 | Onderste rij omlijning van index 2 naar index 1 (grond- en schaduwkant). Index 2 alleen als overgang linksboven (y 50–54). Doel: donker aandeel ≥ ±0,06. | ±35 |
| R4 | Staart x 54–63, y 44–57 | Jordi's open wens uitvoeren: <br>• de staart aan de basis 4–5 px dik, taps; <br>• eindigt in een klein zoutkegeltje (crème met eigen omlijning, ±4×4); <br>• eventueel een turquoise naad, zodat hij op 1× als staart én als kegeltje leest. <br>Kleine silhouetwijziging, alleen in deze zone. | ±25 |

## 6. Evolutie en regional form (Jordi's extra vraag)
Vel deel 1: Silicobra → Sandaconda links, Uyuni-Silicobra → Salticonda rechts.

**a. Herkenbaar de evolutie van de Uyuni-Silicobra, en toch volgroeid?** Ja, met de kop als zwakste schakel.
- Herkenning is sterk:
  - het palet is 1:1 gelijk;
  - zelfde half dichtgevallen oog met turquoise oogring;
  - zelfde kuifmotief, groter en met zoutplaten;
  - de halsband zit op dezelfde plek onder de kaak.
- Het lijf is overduidelijk volgroeid. De kop groeit maar weinig: van 19×33 naar 21×38 px (±1,15×), met een 4 px langere snuit en een hogere kuif. De expressie is dezelfde.

**b. Verhouding tot Silicobra → Sandaconda?** Deels.

| | Massa | Box | Waar groeit hij | Kop |
|---|---|---|---|---|
| Origineel | 889 → 1609 px (1,81×) | 39×36 → 64×40 | in de lengte | verandert sterk: wijde zandmuil, neusbult; de zandzak wordt een enorme buidel over het hele lijf |
| Regionaal | 990 → 2495 px (2,52×) | 39×39 → 62×61 | in de hoogte | blijft bijna gelijk |

- De **massastap is groter** dan bij het origineel en de **kopstap is kleiner**.
- De extra massa past bij "bulky wall": hij hoort bij Hippowdon, Torkoal en Steelix, en de pose als zoutkegel is een bewuste keuze, geen ongelukje.
- De kopstap blijft achter bij het origineel (dat was ook Jordi's eigen les: "een evolutie moet ook in de kop evolueren").

**c. Geslaagde regional form volgens de studie?** Ja.
1. **Idee herkenbaar:** een opgerolde slang die een materiaal in zijn lijf opslaat en uitspuwt. Dat is Sandaconda's idee in een eigen vorm, zoals Runerigus naast Cofagrigus.
2. **Kenmerk met ander materiaal en andere functie:** zand → zoutkorst, zandzak → pekelband (lithium) → batterijcellen. Dat is het sterkste punt, net zo duidelijk als Yamask-masker → kleitablet.
3. **Verklaard door de regio:** de zoutvlakte van Uyuni, de lithiumpekel eronder en de zoutkegels van Colchani. Concreet, echt en uniek voor Zuid-Amerika.
4. **De regionale evolutie vergroot het nieuwe kenmerk:** één halsband wordt drie ringen over het hele lijf. Precies wat Perrserker (munt → pantser) en Obstagoon doen.

**d. Ground/Electric en wall, niet Ice of Nacli?**
- **Ground:** ja (aardtinten, heuvelvorm, zwaar).
- **Wall:** ja. Brede basis, geen ledematen, loom half oog. Op het vel staat hij in de familie van Torkoal en Hippowdon.
- **Electric:** zwak. De turquoise banden lezen als pekel of strepen, niet als stroom. Je weet het pas via de naam of de dex. Teal is wel een Electric-kleur (Eelektross, Tynamo), maar er is geen enkele vonk, pool of glans die "stroom" zegt.
- **Ice:** laag risico. Het warme beige houdt hem ver van het ijsblauw van Alola-Sandshrew en -Sandslash. Het meest ijzige deel is de witte glans in de glanzende halsband op een donkere achtergrond.
- **Nacli-lijn:** laag risico. Ronde windingen in plaats van blokken, geen oranje, geen kubussen. Garganacl en Naclstack staan op het vel ter controle.

**Eindoordeel regional form: geslaagd.**
- Het concept voldoet aan alle vier de punten van de studie, en de regionale verklaring is beter dan die van de meeste officiële forms.
- Wat het nog niet helemaal waarmaakt:
  - de kop evolueert minder dan in het origineel;
  - Electric is in de sprite nauwelijks te zien.
- Dat zijn smaakvragen voor Jordi (hieronder), geen fouten in de opzet.

## 7. Voor Jordi (smaak) – vragen, geen fails
Deze punten raken onderdelen die Jordi goedkeurde. Ze tellen niet mee in de uitslag.
1. **Kop-evolutie:** de kop is ±1,15× de Uyuni-kop, met dezelfde expressie. Sandaconda verandert zijn kop veel sterker. Is de 3e-kop "volgroeid" genoeg, of mag het oog bijvoorbeeld iets zwaarder, met een dikkere wenkbrauwschub zoals op de anacondafoto?
2. **Electric-hint:** palet-index 15 is vrij. Bijvoorbeeld een bleekgele glans van 2–3 px op de lichte kant van elke ring, of een "pool" op de staartpunt, zou Electric op 1× laten lezen. Dit verandert het palet van de lijn (shiny!).
3. **Eén slang of gestapelde banden:** de windingen lopen horizontaal en kruisen nergens. Op 1× kan het lijf ook als bijenkorf of autobanden lezen. Eén zichtbare overlap, waar een winding vóór de volgende langs schuin omlaag loopt (Ekans, Sandaconda), maakt "één slang" duidelijker. Het lijf van kleur1-E is bevroren, dus dit is alleen een vraag.
4. **Formaat:** 2495 px. Dat ligt boven je eigen doel van 2100–2400, en hij is zwaarder dan Steelix en Torkoal. Goed zo voor een wall, of iets kleiner?
5. **Spiraalstaart:** de staartkrul met spiraal van de Silicobra-lijn (ook bij de Uyuni-vorm) is weg. Die zou als het "zoutkegeltje" van R4 terug kunnen komen.
6. **Glans in de halsband en ringen:** de glans is crème (index 8). Een glans in mintkleur (index 11) leest minder als glas of ijs. De pre-evolutie heeft dezelfde crème glans, dus het is een keuze voor de hele lijn.

## 8. Na het lezen van de notities
- De notities van kleur1 zeggen dat de ringen "in het midden naar beneden buigen". Gemeten: alleen aan de uiteinden. Het midden bestaat uit runs van 21 px, dus FAIL 5 blijft.
- Uit SPEC.md blijkt dat de staartwens van Jordi nog openstaat (R4). Die had ik al als zwak gezien.
- Jordi vroeg zelf in 3b/3d om "1 px lucht boven" (R1).
- 3f zelf (de shading van de kop en de slagschaduw op y 26) is geslaagd. Kop en lijf vallen nu in hetzelfde licht. Mijn oordeel verandert er niet door.
