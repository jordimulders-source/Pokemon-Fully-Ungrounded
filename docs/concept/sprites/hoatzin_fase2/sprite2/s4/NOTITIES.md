# Hoatzin fase 2, ontwerp 2, s4 (20 nov): keurderpunten s3 + scherpte

Jordi: "hij wordt beter, maar nog steeds erg blurry, ga zo verder" · "leer de lessen van andere ontwerpen die blurry begonnen maar uiteindelijk sterk werden".
`sh alles.sh` (bouw4.py, keuze.json, afwerking.json). Niets getekend.

## Keurderpunten s3
1. Verre vleugel niet meer een tint donkerder; in beide vleugels boven het lijf is de donkerste modeltint de vlaktint 3 (palet: 2 (100,100,140), 3 (62,62,96), 4 (36,34,58); stappen ±38).
2. Penranden: per pad 1 lichte rand (verre vleugel en steile paden 1 px, aan de linkerkant bij steile paden; nabije vleugel 2 px boven). Voorrand nabije vleugel nu doorlopend (paden 19 en 42 erbij, naast 61).
3–5 en klein: `afwerking.json` (onderkaak grijs licht/midden, spleet en ondercontour zwart, (4,36) eruit, (8,36) crème, achterteen rij 56 grijs, nek rij 32 doorlopende crème-selout, (19,31) eruit, pootgrijs in staartpunt → crème schaduw). 31 px, allemaal kleur binnen de vorm of eruit waar het model lucht heeft.
6. Lichte vlekken op het lijf vanaf y31 → vlaktint, behalve het lichte vlak y31–32 x33–39.

## Lessen uit GEMINI.md toegepast
- 77/115 (Krassault, Dustly): vulclusters < 6 px samengevoegd met de buurtint binnen dezelfde zone (lijnen, oog, penranden en klauwen niet). Werkte: minder vlekken.
- 152 (pitahaya fase 3): binnenlijnen in de donkerste vlaktint geprobeerd (penlijn = 4): **slechter**, de pennen verdwenen en de vleugel werd vaal. Terug naar zwart.
- 153 (contrast): palet gespreid (stappen ±38). Werkte.
- 129 (gladde toonkaart) → s5.

Controle: dambord 0 · om-en-om 0 · klonten 0 · barcode 0; losse tintpixels 9 (klauw-, poot- en snaveldetail en 2 in de staartpunt).
