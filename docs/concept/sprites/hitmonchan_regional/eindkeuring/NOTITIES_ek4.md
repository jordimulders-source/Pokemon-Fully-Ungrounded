# ek4: duidelijker onderscheid tussen schouder en wachtarm (krabbel_ek3)

Jordi (letterlijk): "hierzo nog iets duidelijker onderscheid tussen schouder en arm".
Krabbel: `jordi/krabbel_ek3.png`, groene ^ boven op de wachtkubus, rechts in beeld.

**Resultaat:** `ek4.png` (64×64, geïndexeerd, dezelfde 7 kleuren + transparant), `ek4_8x.png`, `vel4.png` (ek3 8× | ek4 8× | model; close-up schouder 16× naast het natieve model, gezette pixels en hun modelcellen rood omkaderd; 1×/2× op licht en donker), script `ek4.py` (asserts: oude waarde, modelwaarde, silhouet gelijk, beide ogen/gezicht rij 18–26 × x28–43 gelijk, geen nieuwe kleur, precies 4 pixels anders), log in `ek4_log.txt`.
**4 pixels gewijzigd, alleen de tint. Silhouetdiff 0, gezicht niet aangeraakt.**

## Meting
- De krabbel is ek3 op 6,2× (offset x −15, y +1; gefit op de spritekleuren). In spritecoördinaten loopt de ^ zo: (42,30) → (43,29) → (44,28) → top op rij 27, x45–47 → (48,28) → (49,29) → (50,30).
- Boven de ^ ligt de schouder: de bovenrand 444 op rij 25, het lichte 777 op rij 26 en 666 op rij 27, plus links de 5-vlakken (x41–44, rij 28–30). Onder de ^ ligt het lichte bovenvlak van de kubus (7/6, vanaf rij 28).
- **Model (natief_q, rij/kol):** daar staat de ^ als donkere binnenlijn om het bovenvlak van de kubus. Het linkerbeen is 3 op (40,35), (39,36) en (38,37), en daarna 2 op (37,38). De top is een band 4 4 4 op rij 34, kol 42–44, met (41,35) = 4. Het rechterbeen is 3 op (45,35) en (46,36), en 4 op (47,37).
- **ek3:** het rechterbeen (48,28)=3 en (49,29)=3 stond er al, net als (45,28)=4 en (46,27)=4. Twee stukken vielen weg in de verkleining. Het linkerbeen werd 5, gelijk aan de schouder, waardoor 5 direct tegen het witte vlak lag. De rechterhelft van de top werd 6, omdat sprite-rij 27 vooral model-rij 33 (licht) pakt. Daardoor liep de lichte schouder (777/666) zonder lijn over in het lichte kubusvlak.

## Gezet (x,y oud→nieuw, modelcel)
- (47,27) 6→4: de top van de ^, de band onder de schouder (model r34 k43 = 4).
- (44,28) 5→3: het linkerbeen (model r35 k40 = 3).
- (43,29) 5→3: het linkerbeen (model r36 k39 = 3).
- (42,30) 5→3: het linkerbeen (model r37 k38 = 3). Sluit aan op de bestaande 2-lijn (42,31)/(41,31).

Alle vier de tinten komen uit het model. Er is dus geen eigen ingreep nodig geweest.

Volgorde nu: schouder (4/7/6 en links 5) → binnenlijn 3-4-4-4-3 (^) → kubusvlak (7/6). Het tintcontrast komt van de lijn: schouder en kubusvlak zijn in het model allebei licht (7/6). Op 1× en 2× leest de ^ als een rand.

## Niet gedaan (open)
- (45,27) blijft 6. Het model heeft daar 5 (k40–41 r34). ek2 zette die 5→6. De lijn loopt nu via (45,28)=4, zoals in het model (41,35)=4.
- (48,27) blijft 6 (de schouder boven het rechterbeen).
- De opties uit ek2 blijven open: de bovenrand van de kubus, r25 x44–46, 4→3, en (41,26) 4→3.
