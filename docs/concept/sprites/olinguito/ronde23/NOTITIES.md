# Olinguito ronde 23: verre voorpoot opnieuw (alleen die poot)

Basis: ronde 22. Bouw: `bron/bouw_ronde23.py` (tekst-raster, met de hand). Controle: `bron/check.py` → `bron/check_uitvoer.txt`. Vergelijking: `bron/vergelijk.py` → `compare.png` (ronde 22 | 23 | Galar-Linoone op 1×, 3× en de poot op 8×).

Jordi, letterlijk: "Nu voeg je weer een luie poot toe met een rechte lijn." en "ook idd niet verbonden aan het lichaam."

## Wat er veranderde (37 px per frame, alles in vak x8–24, y39–54)
- Skelet: Linoone's verre voorpoot (aanzet onder de borst, overlapt door de nabije delen, schuin naar voren, taps naar de voet).
- **Vast aan het lijf:** de bovenkant loopt zonder omlijning door in de borstvacht (schaduwtint 3) en verdwijnt achter de nabije voorpoot (x23 grenst aan diens omlijning op x24). De zwarte scheidingslijn x23 (ronde 22) is weg.
- **Dikte:** 6–8 px incl. omlijning (nabije voorpoot 8): bovenarm 7–8, elleboog 8, pols 6.
- **Gebogen omtrek:** voorrand x18,17,17,16,16,15,15,15,16,16 (bolle bovenarm, pols trekt terug, poot weer naar voren); achterrand x23,22,22,21,21,21 (elleboog, dan taps). Langste verticale run 3, geen regelmatige diagonaal > 2 stappen.
- Klauwen: de 2 kleine klauwen van ronde 22 ongewijzigd op dezelfde plek. Licht accent (4) alleen op de bovenarm (rondheid), onderarm schaduwtint.
- Frame 2: dezelfde poot 1 rij hoger (zoals in 22).

## Bewijs (check.py)
- Buiten de pootzone 0 px (beide frames); kop-masker 0; palet gelijk; transparency 0; open randen 0.
- Formaat 1045 / 1049 px (22: 1024 / 1028). Bewust boven 1024: vorm gaat vóór de grens.

## Zelfcheck
- (1) Vastgemaakt aan het lijf: ja. (2) Geen rechte lijn ≥ 4 px: ja (max. run 3). (3) Dikte ≥ 6 px: ja (min. 6 bij de pols).
- 1×/3×: leest als een echte verre poot die uit de borst komt; gezicht ongewijzigd.
- Niet perfect: de elleboog is maar 1 px bolling; de poot zit dicht tegen de nabije voorpoot (dat is de overlap, maar de lucht ertussen begint pas op y44).

## Lessen
- Een verre poot "vastmaken" = de omlijning tussen poot en lijf weghalen en de poot achter het nabije deel laten doorlopen; een zwarte lijn bovenaan maakt er een losse streep van.
- Meet rechte lijnen per rand (run-lengte en gelijke stappen) in het script, niet op het oog.
