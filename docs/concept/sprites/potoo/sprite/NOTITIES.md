# Potoo-frontsprite (frame 1, bek open)

## Ronde 1 (`ronde1/`)
Bestanden: `potoo.png` (64×64, geïndexeerd, 16 kleuren incl. transparant), `normal.pal`, `raster.txt` (tekstraster), `maak.py` (rijen met de hand; bouwt het raster), `keurvel.png` + `.keuring.md` (zelfkeuring), `controle.txt`. Gereedschap: `palet.py` (palet + png/pal), `controle.py` (open randen, losse pixels, clusters < 3 px, gaatjes, diff met vorig raster), `toon.sh`.

Werkwijze: poppetje r14 verkleind tot 58 px hoog als onderlaag (27 px breed, figuur x19–45); studie op 8× van Taillow (open snavel: lichte kaakrand rondom, donkere holte, lichtere tong onderin), Pelipper, Noctowl, Farfetch'd, Xatu. Daarna rij voor rij met de hand.
- Figuur x14–46, y3–61 (59 px hoog), 1121 px.
- Kop ±15% groter dan het verkleinde poppetje (op 58 px was het oog 4 px en de muil te klein om te lezen).
- Snavel: hoornstukje (F) bovenop vóóraan, snijrand + haak (E) als één vorm, haak dun omlaag met de punt terug; mondlijn donker naar de mondhoek.
- Mondhoek x32/y16, onder/achter het oog; plooi 3 px de wang in.
- Onderkaak: kaakrand D langs verre en nabije kaak (2 px aan de nabije kant), binnenrand 9, punt hoorn (E); bevederde kin onder de nabije kaak, bovenaan licht en zonder lijn overgaand in wang/keel, onderaan in schaduw met de lijn alleen waar de kin over het lijf valt.
- Muil: dunne gehemelteschaduw, V-spleet midden, keel donker achterin bij de mondhoek, kaakbodem lichter (B), tong (C).
- Lijf: borstrand volgt het poppetje (niet uitbuikend), vleugelvoorrand als binnenlijn 2, dekverengrens en één veerlijn (3), getrapte vleugelpunt op de staart; staart lang, onderaan iets uitwaaierend met middenveerlijn; ruige rugrand (3 veerpuntjes van 1 px).
- Patroon: schorsvlekjes (7, grijsbruin, 3 px, gemengde vormen) dicht op mantel/vleugel/staart, ijl (4) op kruin en wang.

Zwakke punten (eerlijk, voor keurder/blinde test):
- Haak is op 1× klein (3–4 px); als de blinde test de snavel mist: haak 1 px langer/donkerder.
- Gehemelteschaduw + V-spleet lezen op 8× als een "T".
- De kinlijn rechts (van de keel naar de kaakpunt) is een lange donkere diagonaal; kan als "kom-rand" lezen.
- Schorsvlekjes zijn blokjes; fijner (2-px-streepjes) mag niet door de clusterregel. Op 1× lezen ze als grijs gemêleerd.
- Contrast lijf is laag (bewust C2, bijna wit); naast Taillow oogt het bleek.
- Vleugel heeft weinig vorm (één veerlijn, één dekverengrens).

## Ronde 2 (`ronde2/`)
Blinde tests r1: beluga/kabeljauw/zeehond/grondel; "worstvormige blob", "staart een steel", "spikkels zonder richting", "palet vlak", "bek als losse trechter", "bek lijkt de kop". Opnieuw met de hand (`maak.py`, eigen `palet.py`; F is nu de vleugelschaduw, de hoornrug gebruikt 4).
- Koepel groter (y1–15, 19 px breed), muil iets kleiner (punt op y28); haak 2 px langer (tot y19, punt terug).
- Kin: de vacht loopt direct over de nabije kaakrand door naar de keel; geen losse kaaklijn meer, alleen een schaduwsikkel onder de kaakpunt.
- Gevouwen vleugel (Noctowl-studie): eigen tonen 4/3/F, omlijnd, licht aan de voorrand, boeg bij de schouder, schouderveren onder de mantel, twee schuine dekverenrijen + dekverengrens, drie pennen met getrapte punten, vleugelpunt steekt achter de staart uit.
- Buik buigt eerder terug, zodat er meer staart zichtbaar is; de staart eindigt in drie veerpunten.
- Veerpuntjes van 1 px op rug en borst; patroon in rijen (mantel 7, pennen F, staart 7), gezicht/borst rustig.
- Valkuil: U-vormige dekveertjes van 5 px naast elkaar lezen als bakstenen of tanden; schuine lijnen lezen rustiger.
Zwakke punten: borst is een groot leeg vlak; zichtbare staart is nog kort; kruin is glad; dekverenrijen zijn rechte lijnen.

## Ronde 3 (`ronde3/`)
Blinde tests r2: "bek leest niet als snavel (paarse vlek/zakje)", "borst vlak", "dunne staaf onderaan", "oog los". `maak.py` laadt het raster van ronde 2 en tekent kop/muil (y11–31, x8–32) en buik/staart (y44–62) opnieuw; rest van ronde 2 ongewijzigd. Palet: 7 iets warmer grijsbruin (160,140,132) = hoorn én schorsstreepjes.
- **Bovensnavel**: eigen hoornvorm met zwarte outline: gewelfde snavelrug (lichte rand 4, hoorn 7, schaduw E) vanaf het voorhoofd (x17,y11) naar voren tot x9, in één vorm doorlopend in de haak (x9–12, y15–21) met de punt terug. Daarachter loopt de hoorn als taps toelopende snijrand (E, y16) tot halverwege de mond, daaronder de zwarte mondlijn tot de mondhoek onder/achter het oog (x29–30, y17). Mondrand 1 rij lager dan in r2: meer gezicht tussen oog en muil.
- **Onderkaak**: verre kaakrand D begint direct achter de haak (licht vlak achter de donkere haak, zodat de haak loskomt) en loopt naar de kaakpunt (E, y28); nabije kaak = D-rand + donkerlila lijn (2) vanaf de mondhoek naar de punt, schaduwsikkel 4 eronder.
- **Muil**: geen V-spleet meer (las als "T"); gehemelteschaduw 9 onder de snijrand, A, B onderin, tong C.
- **Gezicht/borst**: borstelveertjes (3, twee korte trapjes) tussen oog en snavelbasis over de snavelwortel; borst 1 px voller links (y36–43), schaduw 4 langs de vleugelrand, vier korte verticale streepjes 4 op borst/keel.
- **Onderkant**: buik buigt trager in; staart breed en plat (x30–40, y51–62) met middenveerlijn, drie dwarsbanden (3) en twee veerpunten; vleugelpunt ligt schuin tegen de staart tot y57.
Zwakke punten (eerlijk): de bovensnavel is nog vrij rond van voren (kan als eend/duif lezen; haak 1 px langer/scherper zou helpen); borstelveertjes zijn op 1× nauwelijks zichtbaar, het oog staat nog redelijk los; onderste vleugelhelft heeft minder pennenstructuur dan de bovenkant; borststreepjes zijn heel subtiel. Controlescript: geen open randen/gaatjes; resterende 1-px-"clusters" zijn de diagonale lijnen (kaakranden, gehemelte) en de snavelrug-glans, zoals in ronde 2. Nog niet blind getest en niet gekeurd.
