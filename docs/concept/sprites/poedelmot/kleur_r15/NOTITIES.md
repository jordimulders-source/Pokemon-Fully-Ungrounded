# Poedelmot: kleur r15

Vanaf r14, met alleen de 3 gevraagde punten aangepast: 30 px verschil, allemaal in de genoemde zones (de lijst staat in het rapport). Rijen in `stappen/r15.py`.

## Gedaan
1. **Schubjes:** de linker schub (47–49,31–32) is weg. Het model heeft daar alleen de golflijn van de C-krul. De rechter schub zakt een rij (51–53, 32–33) en verspringt nu ten opzichte van de schub op (51–53,23–24) en de krullen ertussen.
2. **Naden taps:**
   - A/B begint licht bovenaan (21,51 crème; 21,52 tan) en is alleen in het dal (y53–54) donker 3. A krijgt een tan schaduw langs de naad (20,52–53).
   - B/B2 loopt rechts uit in 6 (28,56).
   - De C/D-naad begint bovenaan in 6 (41,54), de C-linkerrand in 5 (35,54) en de D/E-naad in 7 (46,53).
   - Plaatlijn x31 begint in de plaattint (31,49).
3. **Koepels:**
   - D heeft een ronde top: (43–45,51) boog en (42,52)/(46,52) schouders, in plaats van de punt op (44,51).
   - E heeft een ronde linkerbovenhoek (45,47); de rest van de top van E zijn de schulpbogen van de achtervleugel uit r14.

## Controle
- Alpha-diff 0, open randen 0, losse pixels 0, clusters < 3 px 0.
- Bekeken op 12× naast het model en op 1×/2×.

## Grenzen die vastliggen (geen open zwak punt binnen deze opdracht)
- **Plaatlijn x34:** begint niet taps. Een losse pixel 8 bovenaan zou een cluster < 3 geven, en de plaat is daar maar 2 px breed.
- **Lijnen op de buitenrand:** blijven lijntint (eis: geen open randen).
