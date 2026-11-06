# Poedelmot: kleur r16

Vanaf r15. Rijen in `stappen/r16.py`; de voorvleugel is per pixel omgezet op `stappen/basis.txt` (= r15).

## Gedaan
1. **Bontkraag:**
   - Haarplukjes (crème 7, met een haakje naar rechts) hangen op onregelmatige afstanden aan de kinschaduw (y43): op x21 (3 px), x26 (2 px), x30 (3 px) en x33 (3 px). Daaronder een tweede rij korte streken op (19–20,46–47) en (28–29,46–47).
   - Losse 7-stippen in de kraag zijn weggehaald ((32,47) e.a.).
2. **Voorvleugel:**
   - Gemeten op het model: tan ≈ (216,192,170), crème ≈ (228,210,185). Onze crème 7 (232,212,184) klopt. De tan 6 (200,168,136) was te oranje en te donker.
   - De vlakken van de voorvleugel (voet, schub-vullingen) staan nu in een nieuwe tint D = (214,190,168).
   - De krul-, schulp- en boogkrullijnen staan in 5 (176,144,120), zodat ze op 1× leesbaar blijven en de vlakken toch lichter worden. Ze zijn 1 px gebleven, niet grover.
   - De achtervleugel staat ook in D (vlakken) en 5 (krul, golf- en schulplijn), zodat beide vleugels dezelfde tint hebben, zoals in het model. De randtaps (55,43)/(54,44) blijven 6.
3. **Klauwtjes:** elke groep heeft nu 2 teentjes, gescheiden door een lichter pixel 4:
   - A: (18,55)+(19,56) en (20,55–57)
   - B: (22,55)+(23,56) en (24,55–56)
   - B2: (24–25,58–59) en (27–29,58)
   - middenpootje: (32,57) en (33–34,58); nieuw teentje 4 op (33,57)
   - C: (35–37,60–61) en (38–39,60–61)
   - D: (43,58–59) en (45–46,58)
   Waar het silhouet geen tweede klauw toeliet: nergens.
4. **Middenstuk:** warmer en zachter: 8 = (194,170,154), 9 = (166,142,128). Het ligt nu in de tint van het omringende tan.

## Controle
- Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0.
- Controle telt D als vlaktint.
- Drie diagonale krulpixels in 5 staan in `krul_lijnen.txt`.
- Palet: 13 kleuren + transparant.

## Zwakke punten
Beide zelfgenoemde punten uit de eerste versie zijn gerepareerd: de kraagplukjes stonden op een kam van 4 px, de achtervleugel was nog in de oude tan.
Op 8× naast het model vond ik geen nieuwe afwijkingen binnen deze vier punten.
