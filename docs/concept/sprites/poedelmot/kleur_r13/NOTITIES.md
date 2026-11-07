# Poedelmot: kleur r13

Vanaf r12; alleen het middenstuk aangepast (rest bevroren: 13 px verschil, allemaal op x30–31, y49–55, plus de paletwaarden 8/9). Rijen: `stappen/mid13.py`.

## Gedaan
- **Smaller:** pluim B loopt nu door tot x30 (crème schaduw 7). De plaatlijn staat op x31. Het zichtbare middenstuk is daardoor een smalle plaat van 2 px (x32–33, y49–55), plus de kleine tan plaat 35–39 × 49–52.
- **Warmer en zachter:**
  - 8 = (196,176,164), zacht grijsroze: de plaat.
  - 9 = (164,142,130), warm donker grijsroze: de schaduw onderaan.
  - Eerst geprobeerd met (176,160,152)/(144,124,116); dat las op 8× nog als een grijze balk, dus nog een stap lichter.
- **Segmentlijnen:** 1 px (x31, x34, x40 en de kraagrand op y48).

## Controle
Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0.

## Zwakke punten
- Op 8× is de plaat nog als een smal verticaal strookje tussen B en C te zien. Hij valt minder op dan in r12, maar nog meer dan de zachte buik in het model.
- Kleiner kan alleen door B of C verder over het middenstuk te laten lopen. Dat verandert de poten, en dat valt buiten deze opdracht.
- De sprieten en klauwtjes zijn ongewijzigd ten opzichte van r12 (zie de zwakke punten daar).
