# Keuring stap 4 hoofd, ronde 2 (6 nov)

Bron: `ronde2/optie_1L/1M/2L/2M.png` (64×64), `ronde2/vel_hoofd.png`, `ronde2/hoofd_*.png`, NOTITIES.md, controle.txt; vergeleken met `graphics/pokemon/hitmontop/anim_front.png` (bovenste 64×64) en de afgekeurde ronde 1 (`stap4_hoofd/vel_hoofd.png`). Coördinaten = schermpixels van de 64×64-sprite.
Bekeken: 8× en 10× (eigen vergroting, nearest, met raster), 2× en 1× (op wit en op groen, naast Hitmontop).

## Hoofdvraag eerst
- **Stand 1 (1L, 1M):** leest op 2× als Hitmontops gezicht (halfdichte ogen, fronslijnen, kleine hoorn), ouder en met een bruine haarmassa bovenop. Duidelijk beter dan ronde 1: het hoofd is geen eikel met kraalogen meer. Op 1× leest het als een breed broodje met een bruine kap en een balletje linksboven. Dat komt vooral door de rechte linkerwand en de platte onderkant (zie NODIG).
- **Stand 2 (2L, 2M):** leest niet als Hitmontop. De gekantelde hoorn (x7–10, y24–27) staat linksboven als een kattenoor, en de knot (x0–5, y28–33) steekt op ooghoogte opzij uit als tweede oor. Samen geeft dat een berenkop of kattenkop. Het haar ligt als een schuine helm. De maker noemde dit zelf als zwak punt. Volgens SPRITE_KERN ("zelfgenoemd zwak punt = terug") valt stand 2 af.

## Per onderdeel (stand 1, tenzij anders vermeld)
| onderdeel | lijkt op | wijkt af in |
|---|---|---|
| ogen | Hitmontops oogvormen met glimpixel, de plooi eronder (x13–16, y41–42 bij het kleine oog) en de halfdichte, zware bovenrand. Geen kawaii-stippen. | Het grote oog (x22–27, y35–40) raakt de kopomtrek op x27 en ligt direct tegen de arm (x28). Op 1× wordt het een deuk in de omtrek. Bij Hitmontop liggen beide ogen vrij in het gezicht en raken ze de rand niet; de bewering in NOTITIES klopt dus niet. |
| wenkbrauwen | V-fronslijnen in donkerbruin (x14–19, y33–35 en x20–21, y33–34) zoals bij Hitmontop. Met de glimlach geeft dat een zelfverzekerde grijns, wat binnen "met de uitdrukking spelen" valt. | Ze bestaan uit losse 1-px-stippen; op 1× verdwijnen ze bijna. Dat mag (bij Hitmontop zijn ze ook klein). |
| mond | 1M: een duidelijke kleine U (x19–23, y42–43) met zwarte hoeken die omhoog staan, dus blijer dan Hitmontop. 1L: dezelfde U met donkerbruine hoeken. | 1L is op 1× vrijwel onzichtbaar. Bij beide raakt de onderkant (x20–22, y43) de schaduwband van de kin (x21–25, y44) en de rechterhoek de wangschaduw (x25–26, y42–43). Op 1× smelt de mond daardoor met de kinschaduw samen. 2L en 2M: kleine streep (x14–17, y42), weinig vreugde. |
| hoorn | Hitmontops hoorn als geheel kleiner (x12–15, y22–26, punt 2 px breed), zelfde vorm en tinten, licht links. Voldoet aan "kleiner in zijn geheel". | Niets wezenlijks. In stand 2 leest hij als oor (zie boven). |
| haar | De puntige haarrand is weg en er is een gladde donkere haargrens (y27–30). | Het haar is een horizontale band van 4–5 px over de hele breedte en leest als een pet of hoofdband, niet als haar dat naar achteren gekamd is. De kamstrepen (y28–30) zijn losse donkere pixels tussen huidkleurige stippen (bijv. (10,28), (9,29), (16,29), (20,29)): ruis, tintvlakjes kleiner dan 3 px. Ze lopen niet zichtbaar naar de knot. Daaronder loopt een glimlijn van losse pixels (o: (12–13,31), (10–11,32), (9,33), (8,34), (6–7,36)) als een diagonale trap: banding langs de haargrens. |
| knot | Is er, 6×6 linksboven (x2–7, y22–27), met donkere omlijning en een bandje. Hij staat aan de achterkant van de kop (het gezicht kijkt naar rechts), dus de plek klopt. | Hij zit alleen met een hals van 2 px (x7–8, y26–27) aan de schedel vast en steekt boven de schedellijn uit. Op 1× en 2× leest hij als een los balletje of oortje, niet als haar dat in een knot samenkomt. Binnenin een dambordpatroon (h/i om en om, x3–6, y24–26). |
| maat | De schedel is 23 px breed (ronde 1: 17–19, Hitmontop: 37). Dat is "iets groter" en naar verhouding nog steeds groot, maar geen mens. Voldoet. | Het grotere hoofd dekt de schouder en bovenarm af (x25–28, y29–41); dat valt binnen de zone, maar Jordi moet het zien. |

## Netheid (alleen het hoofd, SPRITE_KERN)
- Linkeromtrek x5 is een **rechte verticale lijn van y29 tot y42 (14 px)**, en de onderkant y47 is plat van x12 tot x21 (10 px). Een ronde kop met een rechte wand en een platte bodem: daardoor het broodje of blok.
- Ruis in haar en knot (zie tabel), banding van de glimlijn.
- Kleuren alleen uit `normal.pal`, per groep ≤ 3 tinten: in orde. Licht linksboven, schaduwsikkel rechtsonder (y44–46): in orde.

## Bevroren
Zelf nagerekend tegen `stap3b/optie_C.png`: bij alle 4 opties 0 px anders buiten de opgegeven zone (1L/1M x2–29, y22–47; 2L/2M x0–29, y24–47). controle.txt klopt.

## NODIG (stand 1, basis 1M)
1. **Linkeromtrek rond maken:** x5 alleen op y34–38; x6 op y30–33 en y39–42; x7 op y29 en y43 (of vergelijkbaar), zodat de kop een boog wordt en geen rechte wand. Onderkant y47 x12–21 iets laten buigen (midden op y47, uiteinden op y46).
2. **Groot oog los van de rand:** het oog (x22–27, y35–40) 1 px naar links, of de omtrek op x27–28 rond het oog 1 px huid geven. De oogvorm zelf niet aanpassen.
3. **Mond los van de kinschaduw:** de U 1 px omhoog (x19–23, y41–42) of de schaduw op y44 onder de mond 1 px terugleggen, zodat er een rij huid tussen zit. Zwarte hoeken van 1M houden.
4. **Knot als haar, niet als bal:** breder aan de schedel vast (hals ≥ 4 px, bijv. x6–9, y25–28), 1–2 px lager en naar rechts zodat hij op de haarmassa ligt, en 2–3 kamstrepen die vanaf de haargrens zichtbaar in de knot uitkomen. Het dambord in de knot vervangen door gewone schaduw (licht linksboven, donker rechtsonder).
5. **Haar als gekamde massa:** de haargrens als een boog die achter het oor naar de knot afloopt (links lager dan rechts), en minder als een rechte band. Kamstrepen als 2–3 doorlopende lijnen van ≥ 3 px in donkerbruin, zonder huidkleurige stippen ertussen.

## POLIJSTEN
- De glimlijn onder de haargrens (x6–13, y31–36) vervangen door een klein vlak van 2–3 px boven het kleine oog, of weglaten.
- Fronslijnen mogen blijven; eventueel de middelste twee stippen (x15–16, y34) tot één streepje.

## Advies
**1M** als basis: de mond is zichtbaar en blijer, hoorn en ogen kloppen. 1L is gelijk, maar de mond leest op 1× niet. 2L en 2M laten vallen (twee oren, helm, leest niet als Hitmontop). Na NODIG 1–5 opnieuw keuren, daarna pas naar Jordi.

Oordeel: FAIL
