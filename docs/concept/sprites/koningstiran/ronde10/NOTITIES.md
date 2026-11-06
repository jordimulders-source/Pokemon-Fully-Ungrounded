# Sapa Inca – ronde 10 (technische reparaties uit KEURING.md)

Basis: `kandidaat/sapa_inca.png` (= ronde 9 v3 met de puntige stafkop, door Jordi gekozen). `sapa_inca.txt` = dat volledige raster met onderaan het blok "ronde 10". Dat blok wordt geschreven door `reparatie10.py`, waarin per keuringspunt staat welke pixels veranderen.
Bestanden:
- `sapa_inca.png`, `sapa_inca.txt`
- `reparatie10.py` → `diff_per_punt.txt`
- `bouw.py` → `controle_uitvoer.txt` (controle met de strenge definitie)
- `vel.py` → `vel.png` (4× en 1× licht/donker; kop, lijf en vleugel op 8×, telkens naast de kandidaat)
- `kijk.py`

Niet aangeraakt (Jordi beslist): kopmaat en ogen, snavelvorm, klauwen, vorm van de vleugelpunt, onderrand van de kroon, kleurgebruik, kroonpatroon v3, de vorm van de stafkop, pose.

## Strengere controle (`bouw.py`)
Naast transparant mogen nu alleen K (zwart), d (donkerste bruin) en p (donker lavendel, de bestaande kroonomlijning aan de lichtkant) liggen. B/b (l/m), r, G (a) en s (t) tellen als open rand. In de kandidaat gaf dat **76 open randen**; na de reparatie **0**.

## Wat er veranderde, per keuringspunt (`diff_per_punt.txt`)
| Punt | Wat | px |
|---|---|---|
| 1 | Zwart aan de lichtkant van de stafkop tegen de kroon → donkergoud (a); waar het de rand van het kroonkwastje is → donkerrood (r) | 6 |
| 1+3 | Lijf links, vleugelwortel en alle andere open randen omlijnd: lichtkant (transparant links/boven) d, schaduwkant (rechts/onder) K | 59 |
| 2 | De lichte streep (l) aan de schaduwkant rechts van de buik → m; de overgang is nu a → m → d | 19 |
| 2 | Staf links belicht: omlijning d, licht (y) links, g, vaan t, rechts K (rij 29–41) | 28 |
| 4 | Paarse puntjes (43–44,23), (43,24), (46–47,31–32) weg; (42,23) wordt kroonomlijning K | 8 |
| 5 | Schaakbordje in de hand → twee rechte penscheidingen in d (rij 43–45) | 4 |
| 5 | Losse stippen in de borst (25,30), (27,31), (24,32), (24,34) → m; (28,34) viel al onder punt 2 | 4 |
| 9 | Kop links: (22,23) weg, (21,25–26) erbij, zodat de linkerkant rond loopt | 5 |
| 9 | Rechterflank: (38,36) weg | 1 |
| 9 | Vleugelwortel: (40,33) weg | 1 |
- Totaal **135 px**; silhouet +2 / −10 (1637 → 1629). 15 kleuren + transparant; aandeel zwart 0,12.

## Zelf gekeken (1×, 4× en 8× naast de kandidaat)
- De rand is overal dicht en donker, en de staf is links belicht. De schaduwkant van de buik leest niet meer als naad; de hand is rustiger; de paarse puntjes zijn weg.

## Eerlijk: wat nog niet klopt
- **Iets donkerder geheel:** door de strenge omlijning zijn de lichte selout-randen (l) aan de lichtkant van de vleugels, de hals en het kopje vervangen door d. De opgeheven vleugel verliest daardoor wat van zijn lichte bovenrand; Game Freak gebruikt daar juist vaak een lichte selout (Empoleon). Of dat beter is, beslist Jordi.
- **Staf dunner gelezen:** door de omlijning (d links, K rechts) zijn er per rij maar 2–3 gekleurde pixels over; rij 33–35 is nu y + t tussen twee randen.
- **Stafkop links:** de donkergouden rand tegen het oranje van de kroon scheidt minder scherp dan zwart (zoals gevraagd).
- **Staartaanzet:** het rode puntje (28,55) is K geworden (schaduwkant naast transparant), dus de hint is nog maar 1 px roestbruin op (28,54).
- **Rechte stukken:** de rechterflank heeft na het wegnemen van 1 px nog een recht stuk van 5 px (x38, y37–41); verder afronden gaat niet binnen ±1 px zonder een nieuw recht stuk op x39.
- Niet opgelost (bewust, Jordi): kop/ogen klein, snavel op 1×, platte vleugelpunt, rechte kroononderrand.

## Lessen
- Een controlescript dat de schaduw- en basistinten van een groep als omlijning telt, meldt "0 open randen" terwijl de keurder er 76 vindt. Leg de definitie vast: alleen zwart en de donkerste tint per groep (hier K/d/p).
