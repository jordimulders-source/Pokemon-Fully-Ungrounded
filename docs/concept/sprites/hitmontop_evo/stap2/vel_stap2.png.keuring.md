# Keuring: vel_stap2.png (stap 2, stick man in Hitmonlee-verhoudingen + geplakte handen/voeten)

Bron: `stap2/vel_stap2.png`, `stap2/optie_D.png`, `optie_E.png`, `optie_F.png`, `stap2/stap2.py` (gewrichten nagerekend met `maak`/`plaats`), `referenties/pose_eenhandsstand.webp` (gespiegeld), `skelet/vel_skelet.png.keuring.md`, `graphics/pokemon/hitmonlee/anim_front.png` en `graphics/pokemon/hitmontop/anim_front.png` (bovenste 64×64, op 6× bekeken en bounding box gemeten).

Bekeken: 8× (vel), 1× en 2× (onderaan het vel, naast Hitmontop en Hitmonlee). Niet gekeurd op netheid (bewust knip- en plakwerk).

## Metingen (op 64)
- **Hitmonlee:** bbox x 7–59, y 6–58 (marge 4–7 px). Kop-lijf ±30 hoog; zichtbaar been van lijfonderkant tot teenpunt ±22–25 px, incl. voet.
- **Hitmontop:** bbox x 3–55, y 7–56. Voet ±16×11, hand ±8×9.
- **D:** bbox x 10–60, y 4–62. Heup→voet2-punt 22,8; met de geplakte voet tot de klauwpunten ±27. Kop Ø18, romp (schouder→heup) 20, steunarm 18.
- **E:** bbox x 9–61, y 3–62. Benen 22, romp 22, kop Ø20.
- **F:** bbox x 7–61, **y 0**–62. Benen 26 + voet: zichtbaar ±31.

## Per onderdeel: lijkt op / wijkt af in
| Onderdeel | Lijkt op | Wijkt af in |
|---|---|---|
| Pose als geheel (1×) | Alle drie lezen als eenarmige handstand: één rechte steunarm, kop laag links, twee blauwe voeten als hoogste punten in een V. Hoeken van de foto zijn behouden. | De V is breed en vlak (dijen bijna horizontaal), maar dat is zo op de foto. Op 1× is de kopcirkel het dominante volume; de romp is een 1-px lijn en verdwijnt (normaal bij een stick man, wel iets om op te letten, zie hieronder). |
| Steunarm + hand | Hand (Hitmontop 1:1) precies op het eindpunt, handcentrum y 59, onderkant op de grond (62/63). Arm recht en verticaal zoals op de foto. | Niets. |
| Vrije arm + hand | Hand op het eindpunt van de lichtbruine arm, arm vóór het lijf. | De hand zit op 3,4 px van de schouder en 10 px van de heup: op de borst, terwijl hij op de foto bij de riem/heup ligt. In D en F raakt de hand bijna het rode koord. |
| Kop | Laag naast de steunarm, nek aan de cirkelrand, zoals op de foto. | Ø18 (D, F) en Ø20 (E) is even groot als de romp (20–22). Stap 1 rekende op ±14–16 **inclusief afrohaar**; met haar erbij wordt dit een Hitmontop-achtige grote kop op een smal lijf, precies het "wimpy" waar Jordi vanaf wil. |
| Romp | Lengte 20–22 is Hitmonlee-achtig ten opzichte van de benen (kop+romp ±38 vs. benen 22–26). | Als lijn nog niet te beoordelen op stevigheid; bij de volgende stap moet de romp het grootste volume worden (breder dan de kop). |
| Benen | Twee blauwe lijnen in de foto-hoeken; D ≈ Hitmonlee (iets langer door de geplakte voet), E korter dan Hitmonlee, F duidelijk langer. | F breekt de eis "niet langer dan Hitmonlee": zichtbaar ±31 tegen ±25. |
| Voet 2 (rechts) | Hitmontops voet 1:1; het bruine enkelstompje (±(49–51, 10–13)) ligt op enkel2 (52,11) en het been komt er schuin van linksonder in. Logisch. | Stompje staat verticaal, het been komt onder ±45°: kleine knik, acceptabel. |
| Voet 1 (links) | Gespiegelde voet, klauwen naar buiten. | **Fout:** de voet is gecentreerd op `voet1` (18,3; 16,2), dat **onder** enkel1 (20,2; 13,8) ligt (de "geflexte voet"-correctie uit stap 1). Daardoor hangt de blauwe bol op enkelhoogte, het stompje steekt op y 18–21 recht **omlaag, van het been af**, en het scheenbeen loopt van opzij de bol in. De enkel wijst niet naar het been. |
| Koord | Rood, vanaf de riem omlaag, zoals op de foto. | Kort; prima voor nu. |
| Marge 64×64 | D: 4 px boven, 3 rechts, 10 links, 1 onder (hand op de grond, goed). E: 3 boven, 3 rechts. | **F raakt de bovenrand (y 0): geen marge.** D en E zitten rechts/boven krapper dan Hitmonlee (4–7). |

## Toets
1. **1× leesbaar als eenarmige handstand met V:** ja, alle drie.
2. **Benen ≤ Hitmonlee, verhoudingen eerder Hitmonlee dan mens:** D ja (op de grens), E ja, F nee. Romp/kop-verhouding: kop te groot ten opzichte van de romp om "stevig" te worden (zie Kop).
3. **Handen/voeten op de eindpunten, enkel naar het been:** handen ja; voet 2 ja; **voet 1 nee**.
4. **Past in 64×64 met marge:** D ja (krap), E ja (krap), F nee.
5. **Raar voor de volgende stap:** voet 1 zoals hierboven; de kopcirkel (zonder afro) is al zo groot dat er met haar weinig ruimte overblijft en het geheel kopzwaar wordt; vrije hand op de borst in plaats van bij de riem.

## NODIG
1. **Voet 1 verankeren aan de enkel, niet centreren op `voet1`:** plak de voet zo dat het bruine stompje óp enkel1 ligt en in het verlengde van het scheenbeen wijst (van de enkel naar de bol, dus naar linksboven). Het eenvoudigst: gebruik voor voet 1 Hitmontops **linker** bovenvoet (±crop (3,6,22,27) in de sprite), waarvan het stompje al schuin naar rechtsonder naar het lijf wijst, precies de richting van dit been. Dezelfde regel (stompje op de enkel, bol in het verlengde van het been) voor voet 2 aanhouden; ook mag 90°/spiegelen. De "geflexte voet" uit stap 1 hier loslaten: een ronde klauwvoet heeft geen hiel/teen-richting.
2. **Kop kleiner:** Ø ±14 als het afrohaar er later nog omheen komt (of zeg expliciet dat de cirkel al incl. haar is, dan mag Ø16). De romp moet het grootste volume worden; anders blijft het Hitmontop-wimpy.

## POLIJSTEN
- Vrije hand 3–4 px verder langs de arm richting de riem/heup (zoals op de foto), los van het koord.
- Na de voetfix de marge boven en rechts op ≥4 px brengen (1 px kleiner schalen of 1 px naar links/omlaag), zoals Hitmonlee.
- Vel: geen opmerkingen; 1× naast Hitmontop/Hitmonlee werkt goed.

## Advies
**Optie D** (benen 24, op Hitmonlee-lengte), met de kleinere kop. E is een goede tweede als Jordi het nog compacter wil (benen duidelijk korter dan Hitmonlee, maar de grotere kop Ø20 maakt hem juist kopzwaarder; dan ook de kop verkleinen). F valt af: langer dan Hitmonlee en tegen de bovenrand.

Oordeel: FAIL
