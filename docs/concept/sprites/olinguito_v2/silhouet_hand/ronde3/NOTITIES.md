# Olinguito v2: silhouet met de hand, ronde 3 (gerichte reparaties)

Basis: `../ronde2/silhouet.txt`. Bevroren: de voorpoten, de romp, de nabije achterpoot en het oor. **Pixeldiff buiten de drie zones = 0** (nagemeten met een script). Binnen de zones zijn 97 pixels gewijzigd.

Zones:
1. **Kop:** x 0–27, y 13–37. Het oor (y 13–17) en de rechterrand van de kop (nekwig) zijn ongewijzigd.
2. **Staart:** x ≥ 38, y 5–25. Vanaf rij 26 (de bovenkant van het achterlijf) is niets veranderd.
3. **Verre achterpoot:** x ≥ 46, y 38–52.

**Bestanden:** `silhouet.txt`, `silhouet_1x.png`, `vel.png`. Op het vel staan:
- de onderlaag;
- ronde 3 op 4×;
- ronde 3 half doorzichtig over de onderlaag (+2, +2 px);
- ronde 3 met de verre poten lichter;
- ronde 2 op 4× ernaast;
- alles op 1× op grijs en wit, naast Linoone, Zigzagoon, Poochyena, Growlithe en Sentret.

## Maten
| | ronde 3 | ronde 2 |
|---|---|---|
| pixels | 1137 | 1110 |
| box | 52 × 50 (x 2–53, y 8–57) | 52 × 48 |
| spleten van 1 px tussen poten | 0 | 0 |
| losse pixels | geen; alleen klauwpunten en tenen hebben 1 buur | |

Er kwamen 27 px bij door de vollere, stompe snuit en de hogere staartboog.

## Per reparatie
1. **Kop als ronde druppel.**
   - De linkerrand loopt nu in één vloeiende curve van de kruin naar de neus (x per rij: 12, 10, 9, 8, 7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 2) en buigt dan rond terug naar de kin (3, 5, 8, 12).
   - Geen knik tussen voorhoofd en snuit en geen spits meer.
   - De snuit is stomp en dik: bij x 5 is hij ±10 px hoog. De neus is een ronde punt van 4 rijen (x 2–3, y 31–34) naar linksonder.
   - In de overlay valt de omtrek bijna precies samen met de kop van de onderlaag.
   - Het oor is ongewijzigd: één ronde bult.
2. **Rechtsonder ontward.**
   - **Verre achterpoot:** één eenvoudige gebogen poot onder het achterlijf, achter de nabije achterpoot.
     - Hij komt onder de bil uit (y 38) en loopt schuin naar achteren naar een knik (hak, x 53, y 42–43).
     - Daarna gaat hij omlaag naar een platte voet op de grond (x 47–52, y 48–49), hoger dan de voet van de nabije achterpoot (y 52).
     - Hij is 5 px dik, met overal 2 px lucht tot de nabije dij of hak. De oude haak naar achteren en de zwevende voet zijn weg.
   - **Staart:** volgt nu de boog van de onderlaag. Hij gaat vanaf de bovenkant van het achterlijf hoog omhoog (base x 44–48, y 25), buigt licht naar rechts (x 49–51, y 12–17) en krult bovenaan naar links (top y 8), met de punt omlaag (x 40–42, y 10–13). Hij is vrij van de poten, met ±12 rijen lucht tussen staart en verre achterpoot.
   - Onderaan het achterlijf hangen geen andere krullen of haakjes.
3. **Formaat:** 1137 px. De dikte van de poten is gelijk gebleven (bevroren).

## Toets op 1×
- **Kop:** ik lees een ronde kop die afloopt naar een stompe, dikke snuit; geen naald.
- **Rechtsonder:** ik lees één poot onder het achterlijf (met de verre poten lichter is het eenduidig) en daarboven, los ervan, de staart in een boog met de krul bovenaan.

## Eerlijk: aandachtspunten
- **Box:** 52 × 50, groter dan de fase-1-richtlijn. Dat komt door de uitgestrekte pose en de hogere staartboog.
- **Verre achterpoot:** in één kleur hangt de leesbaarheid op 1× nog deels af van de schaduwtint in de kleurfase. De vorm zelf is nu wel een eenvoudige poot.

## Lessen
- **Bij gerichte reparaties eerst de zones vastleggen**, dan per zone tekenen en daarna de pixeldiff buiten de zones meten (moet 0 zijn). Rijen op de rand van een zone (de aanhechting van een poot op rij 38) horen bij de zone; vooraf benoemen.
- **Een kopomtrek als lijst linkerranden per rij** maakt een vloeiende druppel controleerbaar: elke stap 0–2 px, geen terugsprong behalve bij de neus.
