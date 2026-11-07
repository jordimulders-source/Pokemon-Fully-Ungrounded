# Keuring stap 3b (6 nov), onafhankelijke keurder

Bron: `vel_stap3b.png`, `vel_delen.png`, `optie_A–D.png`, `NOTITIES.md`, `stap3b.py` (skeletpunten Q uit stap 2, D14), bronsprites Hitmontop/Hitmonchan/Tyrogue/Hitmonlee, ter vergelijking `../stap3/vel_stap3.png`.
Bekeken: 8× (vel) en 12× met raster (eigen vergroting van optie_A–D en van elk los deel, nearest), en 1×/2× op het vel.
Getoetst op Jordi's punten 1–5; naden tussen delen en shading niet gekeurd.

## Jordi's punten

1. **Kop draait mee: JA (alle opties).** De kop wordt langs zijn as gedraaid (bron nek -> hoorntop op skelet nek (26,38) -> kop (22,35)), net als de andere delen; niet meer los op/neer gezet zoals in stap 3. Wel: met `rek=False` loopt de grote kop (A/B) 22 px voorbij de nek, terwijl het skeletsegment 6 px is (skelet "kop 14"). De kop is dus bijna 3× te groot voor het skelet. De kop van de overworld-sprite (C/D, ±16 px) past wel.
2. **Meegeknipte handen/polsbanden/armstokjes: grotendeels weg.** Kop (frontsprite): geen blauw, geen handen, geen stokjes. Restanten:
   - Op de plek waar de rechterhand is weggeknipt (bron rond (43–51,36–41)) blijft een **inkeping met een omhoog gekrulde punt** over: in A/B is dat de vreemde "staart" linksonder op (6–12,43–50), inkeping rond (13–19,44–48) en een zwart restpunt rond (18,46). Daardoor is de kop scheef: de ene rand is rond, de andere een haak.
   - Overworld-kop (C/D): onder de kin hangen **3–4 zwarte stompjes van het lijf/de benen van de overworld-sprite** (bron (27–28,39–40), (31,39), (35,40)), in C/D rond (23–29,36–41), zichtbaar als zwarte pixels op (23–24,40–41).
   - Arm, romp, dij, scheen: geen handschoen, geen huid, geen restanten van een andere soort. Goed.
3. **Netjes geknipt: grotendeels JA.** Op de knipnaden zit een gesloten omlijning (zwart, of Hitmontops eigen bruine omlijning (131,90,41) op de linkerrand; dat is bronkleur, geen gat). Restpixels: arm onderaan één uitstekende zwarte pixel (bron (24,53)); romp_chan heeft binnenin een losse zwarte streep (bron (28–33,29), de oude halslijn) waardoor de bovenkant als een hoedje leest. Veel beter dan stap 3.
4. **Lichaam zichtbaar en te beoordelen: NEE.** Dit was het doel van deze stap.
   - **A/B:** de grote kop ligt precies over de romp (kopbreedte loopt bijna evenwijdig aan schouder (27,41) -> heup (37,24)). Van de romp is alleen een paars randje op (28–35,37–43) en (40–43,30–38) te zien. Schouder, borst en heup zijn niet te zien; het lichaam is niet te beoordelen.
   - **C/D:** de kop bedekt nog de schouderkant (15–30,27–42). Het midden van de romp (29–40,26–39) zit vol met: de vrije arm (omgekeerde V, elleboog (30,26)), de grote vrije hand (32–39,32–39), de aanzet van beide dijen en het rode koord. De romp leest niet als één doorlopend lijf tussen schouder en heup. Waar de steunarm aan de romp vastzit (27,41) is redelijk te zien; de heup/beenaanzet (37,24) niet.
   - De vrije arm valt weg tussen de beenaanzetten (donker blok (27–33,24–30) in C/D); boven- en onderarm zijn niet als arm te lezen.
5. **Verder raar:**
   - Volgens het skelet zit de nek (26,38) ín de romp, 3 px boven de schouder, en wijst de kop naar boven/opzij langs de borst. Elke kop moet daardoor over de romp liggen. Bij een handstand hoort de kop onder/naast de schouders (richting grond). Dit komt uit het goedgekeurde skelet van stap 2, maar Jordi moet het zien: het verklaart waarom het lichaam verdwijnt.
   - Het rode koord is een kale lijn van 1 px (200,60,40) zonder omlijning, getrokken over de romp (37–39,24–31). Het is geen geknipt deel en leest als een kras.
   - De Tyrogue-romp (B/D) is alleen een broekstuk van ±10 px, ±2× gerekt (nearest), en daardoor blokkerig; in D is het een oranje vlek op (40–43,27–33). Het leest niet als romp.

## Per onderdeel

| Onderdeel | Lijkt op | Wijkt af in |
|---|---|---|
| kop (frontsprite) | Hitmontops kop met hoorn en gezicht, gaaf geknipt | haak/inkeping op de plek van de weggeknipte rechterhand; 3× te groot voor skeletsegment; dekt de romp |
| kop_overworld | dezelfde kop klein, past bij skeletmaat | zwarte lijf-/beenstompjes onder de kin |
| arm (Hitmonchans been) | nette buis, omlijnd | 1 uitstekende pixel onderaan; leest los als been (knie/laarsaanzet), na rekken acceptabel als steunarm |
| romp_chan | Hitmonchans tuniek zonder armen | losse zwarte halslijn binnenin (hoedje-effect); in de opties nauwelijks zichtbaar |
| romp_tyro | broek + stukje shirt | te kort (2× gerekt, blokkerig); leest niet als romp |
| dij/scheen (Hitmonlee) | ongewijzigd, Jordi akkoord | – |

## NODIG (64×64)
1. **Romp zichtbaar maken**: het lichaam tussen schouder (27,41) en heup (37,24) moet als één doorlopend vlak te zien zijn. Bijvoorbeeld de kop achter de romp tekenen (`kop_voor=False` bestaat al), of de kop/nek laten aansluiten aan het schouder-einde in plaats van langs de borst; daarbij de vrije hand (32–39,32–39) niet midden op de borst. Liever een vel met de romp één keer zonder kop en zonder vrije arm, zodat Jordi het lichaam zelf kan beoordelen.
2. **Grote kop (A/B) niet gebruiken** zolang het skelet "kop 14" is; door die kop verdwijnt het lichaam. C/D (overworld-kop) is de juiste maat.
3. **Restant van de rechterhand bij de kop**: de haak/inkeping (A/B rond (6–19,43–50)) gladmaken naar de ronde rand, zoals de andere kant.
4. **Overworld-stompjes weg**: zwarte pixels onder de kin (C/D rond (23–29,36–41)).
5. **Skeletpunt kop/nek aan Jordi voorleggen**: de nek ligt in de romp en de kop wijst langs de borst (zie punt 5).

## POLIJSTEN
- Rode koord (37–39,24–31): als echt onderdeel met omlijning, of weglaten tot later.
- Losse zwarte halslijn in romp_chan (bron (28–33,29)) en de uitstekende pixel onderaan de arm (bron (24,53)).
- Vrije arm (28–37,26–36) leesbaar maken: nu een donkere knoop tussen de beenaanzetten.

Vergeleken met stap 3 is het een duidelijke verbetering: de kop draait mee, de handen en stokjes zijn eruit en de knipranden zijn gesloten. Alleen het doel van de stap, het lichaam laten zien, is niet gehaald: in A/B ligt de kop eroverheen, in C/D liggen kop, vrije arm en vrije hand er samen overheen.

Oordeel: FAIL
