# Kudu sprite ronde 10: minder wollerig (maker)
Jordi over r9 (letterlijk): "het is qua vorm nu iets te wollerig". Uitgangspunt: B6 en B9 (lang hangend). Oog K4.
Scripts: `sprite/r10.py` (varianten), `sprite/vel10.py` (pngs, vel, telling, bronnen); de vorm zit in `sprite/r9lib.py` (`Vorm9(N, slank)`).

## Varianten (`vel.png`)
- **B6a / B9a – zelfde omtrek, rand rustig.**
  - De omtrek is die van B6/B9.
  - Alle bulten en punten aan de zijkanten, op de kam en bij de schouder zijn weg.
  - Over blijven alleen de Arcanine-borstkraagpunt (19,47)-(23,51): 4× op de onderrand en 1× onder de kam, waar die op de rug ligt.
- **B6b / B9b – slanker en hangend.**
  - De rechterrand van de manen loopt van achter de oren (20,25) gebogen naar de schouder (27,40): `R(y) = 20 + 7·((y−25)/15)^1,3`. Smal bovenaan en het breedst waar de manen over de schouder vallen.
  - De bolle kam over de rug is daarmee weg. Wat vrijkomt, wordt nek/rug in de lijftinten L/M uit de modelhelderheid, zoals bij de borst in r9.
  - Boven een nek-/ruglijn van achter de oren (20,25) naar de schoft (32,31) is het lucht. De bovenlijn van de nek is D, net als de bestaande ruglijn van r6.
  - De oude kamomtrek boven die lijn is verwijderd.
  - De onderrand heeft dezelfde 4 Arcanine-punten.
- **Alle vier:**
  - De schaduw van het manenvlak is de Arcanine-rugpluk, net als in r8/r9.
  - De borst is zoals in r9 en heeft 1 px slagschaduw onder de manen.

## Controle (`telling.txt`)
- **Pixeldiff:** 0 px anders buiten de manen + de vrijgekomen zone. Oogvlak K4 en halsstrook: 0 px.
- **Afstand manen-voorpoot:** 5 px (N=6) en 6 px (N=9).
- **Rechte manenlijnen > 3 px:**
  - In alle vier: de lijnen langs de halsstrook (x12/13 en x15). De halsstrook zelf is recht en ligt vast.
  - Alleen in a: de schouderrand x26, y32–36, omdat de bulten daar nu bewust weg zijn ("zijkanten glad").
  - b heeft aan de buitenkant geen rechte stukken.

## Zelf gekeken op 1×
- **a:** de rand is rustiger, maar de vorm is nog steeds een bol kussen op de schouder. Dat leest eerder als een kraag of cape.
- **b:** dit leest het meest als nekhaar dat langs de hals naar beneden hangt. De nek en rug erachter zijn nu zichtbaar.
- **b, bovenlijn nek:** die is D, net als de ruglijn van r6, maar op 1× zwakker dan de zwarte omtrek van de kop. Hij loopt ook als vrij rechte trap van achter de oren naar de schoft (verzonnen snedelijn; het model heeft daar manen).
- **b, nek:** op de nek komt een lichte L-vlek (lichtste kwart van de modelhelderheid). Die leest als licht van boven.
