# Stap 4: het hoofd (6 nov)

Jordi: "we gaan er eerst een goed hoofd op zetten. Gebaseerd op Hitmontop, die maken we zodat die goed past in de hoek en de pose die we van plan zijn. De stekel bovenop het hoofd van Hitmontop wordt iets minder aanwezig en de 'haren' kammen we naar achteren in een klein staartje of knotje, maar het lijkt me niet dat die te zien is in de pose, of juist net wel, voor de rest gaan we nog nergens aan zitten". Aanvullingen: "ogen, wenkbrauwen, mond blijven hetzelfde, maar we kunnen een beetje met de uitdrukking spelen" en "pixel voor pixel is misschien niet mogelijk, vanwege pose en hoek".

Basis: `stap3b/optie_C.png`. Alleen het hoofd is veranderd. `stap4.py` bouwt optie C opnieuw zonder hoofd (stap3b `bouw` met een lege kop) en plakt het nieuwe hoofd erop. De hoofden zijn met de hand als tekstraster getekend: `STAND` in `stap4.py`.

## Opties
| optie | stand | knotje | uitdrukking |
|---|---|---|---|
| 1a / 1b / 1c | ±15°, meer naar de kijker | geen / net zichtbaar / geen | e1 / e1 / e2 |
| 2a / 2b / 2c | ±40°, zoals de foto (as nek → kruin van het skelet) | geen / net zichtbaar / geen | e1 / e1 / e2 |
| 3a / 3b / 3c | ±65°, kruin naar links, kin tegen de nek | geen / net zichtbaar / geen | e1 / e1 / e2 |

- **e1** = Hitmontops uitdrukking (ogen, wenkbrauw, mond met het donkerbruine staartje).
- **e2** = de 2 donkerbruine pixels van het mondstaartje weg: een kortere, rechte mondstreep, dus rustiger en ouder. Verder gelijk aan e1.
- Bestanden: `optie_XX.png` (64×64), `hoofd_XX.png` (het hoofd los op 8× naast Hitmontops front- en overworldkop), `vel_hoofd.png` (alle opties: 8×-uitsnede, 1× en 2× naast Hitmontop), `controle.txt`.

## Welke pixels uit welke bron (`graphics/pokemon/hitmontop/anim_front.png`, palet `normal.pal`)
- **Kleuren:** alleen Hitmontops palet: huid 2/3/4 (255,222,156 / 222,189,131 / 180,139,90), donkerbruin 5 (131,90,41), wit, omlijning (16,16,16). Er komen geen nieuwe kleuren bij.
- **Groot oog** (rechts in het gezicht): Hitmontops linkeroog (x23–27, y40–43; 5×4: `.FF.. / F1FF. / FFFFF / .FF..`). Ik heb het met het gezicht gespiegeld en de glimpixel 1 px naar links gezet, zodat het licht van linksboven komt. Stand 2 en 3: dezelfde vorm, alleen verplaatst langs de gekantelde ooglijn.
- **Klein oog** (links): Hitmontops rechteroog (x33–36, y42–45; `.FF. / F1FF / FFFF / .FF.`), de vorm is ongewijzigd.
- **Wenkbrauw:** Hitmontops donkerbruine streep boven het kleine oog (x29–35, y38–40, in de vorm 1-2-3 px), gespiegeld met het gezicht. Stand 1 heeft hem ongewijzigd. Stand 2 heeft door de kanteling een vlakke streep; daar staat alleen het buitenste deel (3 px) erin, want het binnenste deel liep tegen het oog aan en las als een knipoog. Stand 3 heeft dezelfde streep meegedraaid (1-2-2 px).
- **Mond:** Hitmontops streep (32,46), (33–34,47) zwart plus (35–36,47) donkerbruin, gespiegeld. In stand 2 en 3 is hij meegedraaid (steiler). In stand 3 staat hij 1 px verder van het kleine oog, anders raakten ze elkaar.
- **Afstand tussen de ogen:** 1 px kleiner dan bij Hitmontop (4 i.p.v. 5), omdat de kop kleiner is. De hoogte tussen de ogen is gelijk (het grote oog staat 2 px hoger).
- **Stekel/hoorn:** Hitmontops hoorn (7×8 px, x27–33, y49–56) is teruggebracht tot een puntje van ±3×3 px op de kruin, in dezelfde tinten 3/4 met omlijning. Hij wijst langs de as van de kop: omhoog (1), linksboven (2) of links (3).
- **Haar:** Hitmontops 'top' (de brede bruine rand: basis 4, lichte ruggen 3, strepen 5 die vanuit de hoorn uitwaaieren) is naar achteren gekamd. Het ligt nu plat als een kap over de schedel; de strepen lopen vanaf de haargrens naar de kruin. Het lichte vlak zit linksboven, de haargrens is de basistint 4 tegen de huid (geen zwarte lijn).
- **Knotje:** een bolletje van 4×4 px in dezelfde haartinten. Het zit achterop, aan de kant van de kruin die van de kijker af ligt, en wordt achter het hoofd getekend; alleen de rand steekt uit.
- **Huid:** de verdeling van Hitmontops gezicht: basis 3, licht 2 linksboven onder de haargrens, schaduw 4 als sikkel rechts en onder.

## Maten en zone
- Stand 1: schedel 18 px breed (x9–26) × 19 px hoog, plus 2 px hoorn. Stand 2: 19 × 20. Stand 3: 17 × 19, plus de hoorn links. Ter vergelijking: het oude overworldhoofd was 15–18 px, de frontkop 37 px.
- **Bewijs:** `controle.txt`. Bij alle 9 opties is de pixeldiff t.o.v. `stap3b/optie_C.png` 0 buiten de hoofdzone. De zone bestaat uit de pixels van het nieuwe hoofd (268–294 px) plus de 169 px van het oude hoofd. Het omhullende vak is x5–29, y22–42 (per optie in controle.txt). Waar het oude hoofd weg is, zie je weer stap 3b zonder hoofd: wat schouder- en armpixels bij x26–29, y35–40.
- Geen open randen (elke niet-zwarte pixel van het hoofd grenst aan hoofd of omlijning). Geen tintvlakjes < 3 px, behalve de dunne lijnen (strepen, wenkbrauw, mond) en de hoorn.

## Keuze die Jordi moet zien
- Bij Hitmontop staat de hoorn ónder het gezicht (hij tolt op zijn hoofd). Hier staat de hoorn op de kruin ("de stekel bovenop het hoofd"), en het gezicht staat zoals de kijker het bij Hitmontop ziet. Het gezicht is **gespiegeld** (groot oog rechts) zodat de kanteling met de pose meegaat: kruin naar links, kin naar de nek. Niet gespiegeld zou de kop de verkeerde kant op hellen.

## Eerlijke zwakke punten
- Zonder de brede rand leunt het Hitmontop-gevoel op de ogen, de wenkbrauw, de huidkleur en het gestreepte haar. Op 1× leest het als een ronde bruine kop met een puntje; minder direct "Hitmontop" dan met de rand.
- Het hoofd is groot ten opzichte van het nog dunne lijf (lijf en armen zijn stap 3b-knipwerk). Bij stand 2 dekt het 1–2 px van de omlijning van de vrije bovenarm af (x25–26, y29–36). Het hoofd staat ervoor, dat is bewust.
- Het knotje is klein ("net zichtbaar"). Bij 2b en 3b kan het op 1× als een tweede puntje of oortje lezen; bij 1b valt het het minst op.
- Stand 3 (65°) leest het minst snel als gezicht, omdat de ogen bijna boven elkaar staan.
- e2 verschilt maar 2 px van e1; op 1× zie je het nauwelijks.
