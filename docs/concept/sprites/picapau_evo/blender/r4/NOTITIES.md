# Evo van Picapau, modelronde 4 (r4): grote vogel met Raichu-motief

## Jordi letterlijk
- Over sprite r2: **"het ding is, het is nog niet echt een vogel he. De staart mag wat dunner en wat meer vogelachtig, desnoods zwart. De oren mogen ook naar achter bewegen, zwart en meer op de raichu lijken, verder mag die wat graden naar links draaien, want nu zien we een flink stuk hoofd met het oog helemaal aan de zijkant. De vleugel mag iets vogel achtiger"**
- Aanvulling (via de coördinator): **"ja het lijkt nu iets meer een alien dan een vogel, en ik heb liever eigenlijk een grote vogel met raichu motief"**
  - Daarom is het lijf herbouwd. De basis is een grote vogel (Staraptor, Braviary, Talonflame, Pidgeot, een grote specht zoals *Dryocopus*).
  - Raichu komt alleen terug als motief: zwarte oren met krul, een dunne zwarte staart met de bliksem, de kleur en de wangvlek.

## Bestanden
- `picapau_evo_r4.py`: model, een eigen kopie van r3. Het r3-model is niet aangepast.
  - `STAP=0.5` geeft een snelle, grove proef van ±30 s. De volle render duurt ±5 min.
- `maak_r4.py`: rendert de varianten V0–V3. Uitvoer: `V*_8x.png`, `V*_1x.png` en `varianten_r4.png` (C3 naast V0–V3, op 1×, 4× en als render).
- `vel_r4.py V2` → `vel_r4.png`: de gekozen render op 8× en 1×, naast Staraptor, Braviary, Talonflame, Picapau (af) en Raichu Gen 1.
- Schaal: 0,837, zo gekozen dat het geheel in 61 px past. Dat is kleiner dan bij C3 (0,890), omdat de vogel hoger is.

## Wat er veranderd is
- **Lijf (grote vogel).**
  - De borst steekt naar voren.
  - Een duidelijke nek draagt een kleinere kop: de straal is 8,2 tegen 10,1 in r3.
  - De romp loopt schuin (35°) naar achteren-onder, naar de stuit.
  - Bevederde dijen en langere poten staan onder het zwaartepunt.
  - Het ronde ei-lijf is weg, en `voorover` staat op 0 omdat het lijf zelf al schuin loopt.
- **Oren.**
  - Ze staan verder naar achteren op de schedel en zijn zwart.
  - De vorm is een brede bladvorm die schuin naar achteren-boven wijst. De punt gaat zelf over in een krul van ±260°, dus geen ring op een steeltje meer.
  - De binnenkant is een klein vlak in de lijfkleur, net als Gen 3 (binnenkant = lijfkleur). Hij is dus niet wit.
  - De rafelige achterkuif van r3 is vervallen, omdat daar nu de oren staan.
- **Staart.**
  - Drie stijve, spitse spechtenveren aan de stuit vormen de steunstaart (familie Picapau).
  - Daaruit komt één dunne zwarte veerschacht, als bij een racketstaart (drongo/motmot), met de grote bliksem als "racket" aan het eind.
  - De schacht krult rechts om en loopt onder de poten door naar de bliksem linksonder.
- **Vleugel.** Een echte vogelvleugel, half open, opgebouwd uit lagen. Elke laag ligt iets dichter naar de kijker, zodat de randen als dakpannen lezen:
  - ronde voorrand;
  - rij kleine dekveren;
  - rij grote dekveren met per veer een ronde lichte stip;
  - drie armpennen;
  - zes handpennen in een waaier.

  De pennen zijn donkerder kastanje. Er zijn geen ronde wantlobben en geen drakenvingers.
- Ongewijzigd ten opzichte van r3: de kleuren, de crème buik (nu als borst/buik van een vogel), de wangvlek, de beitelsnavel (iets korter, in verhouding tot de kleinere kop) en de vorm van de bliksem. Het vlak van de bliksem draait nu mee met de lijfdraai.

## Draaien: varianten en keuze
| variant | lijf | kop extra | kop totaal | oog_az |
|---|---|---|---|---|
| V0 | 40 | +20 | 60 (= r3) | 75 |
| V1 | 40 | +10 | 50 | 70 |
| **V2 (gekozen)** | 35 | +5 | 40 | 65 |
| V3 | 30 | 0 | 30 | 60 |

- Waarom V2: het oog staat vooraan op de kop, vlak achter en boven de snavelvoet, net als bij Taillow, Staraptor en Picapau. De snavel staat bijna in profiel naar links.
- De kop draait nog net iets meer naar de kijker dan het lijf. Dat is de Gen 3-regel.
- V3 leest ook als vogel, maar daar staat de kop in hetzelfde vlak als het lijf, en dat heeft bij Picapau al eens een platte profielkop opgeleverd.
- V0 en V1 tonen weer een groot gezicht met het oog naar de zijkant, en dat is precies waar Jordi over klaagde.

## Hoofdvraag: leest het op 1× als een vogel (specht) die aan Raichu doet denken?
- **Vogel: ja.**
  - Nek, vooruitstekende borst, schuin lijf, poten eronder en een gelaagde vleugel met waaier.
  - De beitelsnavel met het oog vooraan geeft een duidelijk vogelhoofd.
  - Het "alien"-gevoel van de ronde bol is weg.
- **Raichu: half.**
  - De bliksem en de dunne zwarte staartlus lezen meteen.
  - De zwarte oren lezen op 8× als Raichu-oren met krul. Op 1× zijn ze een zwarte vlek boven op de kop en is de krul nauwelijks te zien (zie hieronder).

## Eerlijke zwakke punten (de coördinator wilde eerst de render zien)
1. **Nog niet "groot/imposant".**
   - Naast Staraptor, Braviary en Talonflame leest hij als een rechtop staande zangvogel (lijster of roodborst), niet als een grote, machtige vogel.
   - Oorzaken: een rechtop lijf, smalle en korte vleugels ten opzichte van Talonflame, dunne pootjes zonder klauwen, en de vogel zelf vult maar ±35 px van het frame. Bliksem en staartlus nemen de rest in.
   - Voorstel voor een volgende modelronde, eerst ter keuze:
     - lijf 15–20° meer voorover (de Talonflame-diagonaal);
     - vleugels hoger en breder open;
     - de bliksem iets kleiner, zodat de vogel groter in het frame kan;
     - grotere voeten met klauwen.
2. **Oren op 1×.** Als massa zitten ze op de goede plek (achter op de schedel, zwart), maar de krul gaat bij het verkleinen verloren.
   - In de sprite moet de krul met de hand als haak van ≥ 2 px worden getekend.
   - Of de oren worden ±15% groter. Dat raakt Jordi's "too much", dus eerst vragen.
3. **Poten.** De twee poten staan bijna naast elkaar en zijn dun (1 px op 1×). De verre poot moet hoger en verder naar achteren, of dat wordt in de sprite opgelost.
4. **Snavel.** De render toont een licht hoornkleurige kegel die op een hoorn lijkt. In de sprite krijgt hij de grijze snavel met donkere punt van Picapau (zoals r2).
5. **Steunstaart.** De drie spitse veren lopen op 1× samen tot één bruine punt. Als spechtenstaart leest dat wel, maar de schacht die eruit komt is pas onder de veren te zien.

Deel B (sprite) is nog niet begonnen; dat wacht op de coördinator.
