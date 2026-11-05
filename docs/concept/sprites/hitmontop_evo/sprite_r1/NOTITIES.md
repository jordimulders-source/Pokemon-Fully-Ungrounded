# Hitmontop-evolutie, sprite ronde 1 (5 nov): direct in sprite art

Opdracht: kop = Hitmontops kop rechtop, lijf en ledematen met de hand in de pose van `referenties/pose_eenhandsstand.webp` (gespiegeld), bouwstenen uit bestaande sprites mogen (Jordi: "ga maar sprite assets gebruiken die je al hebt en daarmee bouwen").

## Bestanden
- `sprite.png`: 64×64, 4-bit geïndexeerd, 16 kleuren; `normal.pal` (JASC).
- `raster.txt` = de sprite als tekstraster (1 teken = 1 paletindex, `.` = transparant). **Dit is de bron**; `python3 bouw.py` maakt er `sprite.png` + `normal.pal` van.
- `kop_stap1.png`: stap 1 op 8×: Hitmontop frame 1 | Hitmontop verticaal gespiegeld (= rechtop, het skelet) | de nieuwe kop zoals hij in de sprite staat.
- `vel_r1.png` (+ `.keuring.md`-sjabloon van keurvel): 8× en 1× naast Hitmontop en Hitmonlee, plus close-ups van kop en romp.
- Geschiedenis van de opbouw: `kop.py` (kop, per pixel geplaatste segmenten) → `ontwerp_draft.py` (grove vlakken, zie zwak punt 9) → `handwerk.py` (met de hand geplaatste rijen) → `patch.py` (latere reparaties r1b–r1e op `raster.txt`). Die scripts niet meer opnieuw draaien: ze overschrijven `raster.txt`.
- `pal.py`: palet. Hitmontops `normal.pal`, alleen index 14 (donkergrijs 98,98,106, alleen voor klauwschaduw gebruikt) is nu donkerbruin haar (82,52,24); klauwen gebruiken nu wit/lichtgrijs/grijs (1, c, d).

## Welk onderdeel uit welke sprite
| Onderdeel | Bron | Bewerking |
|---|---|---|
| Kop: gezicht, ogen, wenkbrauwen, plooi onder het rechteroog, schaduw onder de rand | Hitmontop frame 1, x12–53 y32–57 | verticaal gespiegeld (rechtop, hoorn boven); oogrijen per oog teruggezet zodat de glans weer linksboven zit; glans (2) van de dome naar linksboven; kin opnieuw rond gesloten |
| Haar | silhouet = Hitmontops rand (brim) | rand wordt bruine dreads, met de hand: drie strengen naar voren/omhoog naar de knot onder de hoorn, lokken links omlaag langs de wang, twee korte lokken rechts achter de kop; links en rechts korter dan de rand (anders raakt het de schouder) |
| Hoorn | Hitmontop | met de hand klein: 3 rijen, stomp, bovenop de knot |
| Beide handen | Hitmontops linkerhand (orig. x9–16 y28–35) | pixel voor pixel, 2× gebruikt |
| Witte polswikkel steunarm | Hitmontops pols (1/d) | met de hand, 2 rijen |
| Nabije voet (linksboven, zool naar voren) | Hitmontops linkervoet | met de hand ±70 % nagetekend: blauw, zoolkussen, 3 klauwen, witte enkelwikkel |
| Verre voet (rechtsboven, zijaanzicht) | Hitmontops rechtervoet (orig. x40–55 y14–22) | 1:1 verschoven, hielklauw ingekort, donkergrijs → grijs/zwart |
| Broek, benen, romp, hals, armen, koordjes | geen (pose van de foto, verhoudingen van `ontwerp/pop2_55_64.png`) | met de hand; zie zwak punt 9 voor de grove eerste laag |

## Stap 1: kop (eigen toets)
"Is dit duidelijk Hitmontops kop, ouder?" Hitmontops kop: ja. Hetzelfde gezicht, dezelfde ogen, dezelfde 3/4-hoek en scheve stand, de randvorm komt terug als haar, de hoorn zit nog bovenop. Ouder: nauwelijks; het gezicht is ongewijzigd (zelfde frons). Eerdere versies las ik zelf als "mensje met pony/paardenstaart" (eigen rond gezicht) en als "hoed met streepjes" (fijne strepen); die zijn weg. Daarom is het gezicht 1:1 Hitmontop gebleven.

## Anatomiecontrole op 8× (Jordi: "pas zien als niet zijn haren opeens half op zijn keel zitten of andere rare shit")
- **Haar alleen op de schedel en logisch door de zwaartekracht:** ja. Kruin + knot onder de hoorn; links hangen de lokken recht omlaag langs de wang tot kaakhoogte (aan de buitenkant, ver van de keel); rechts twee korte lokken achter de kop. Niets over gezicht, keel of schouder: de pony eindigt op de wenkbrauwlijn (zoals Hitmontops rand). De rechterpunt is 2× ingekort; er zit nu 1–2 px lucht tussen haar en de vrije bovenarm (r1d).
- **Kop met een nek op de romp:** ja, maar kort: de hals zit tussen kaak en schouderlijn (rij 41–45) en wordt grotendeels door de kaak bedekt (zie zwak punt 4).
- **Ledematen aan het juiste gewricht, aantallen:** 2 armen, 2 handen, 2 benen, 2 voeten. Steunarm vanaf de nabije schouder (onderste eind van de schouderlijn) recht omlaag, pols, bal op de grond. Vrije arm vanaf de verre schouder (achter de kop), bovenarm langs de bovenflank naar de elleboog bij de taille, onderarm naar de hand op de heup. Beide benen uit het bekken; het nabije been ligt bij de heup vóór het verre (contourlijn 9).
- **Geen zwevende of losse stukken, geen restpixels:** script-gecontroleerd: 1 samenhangend deel, 0 zwevende pixels; handen, lijf en blauw van de Hitmontop-uitsnede zijn weg. Kleine tintclusters < 3 px (8-buren): 70, Hitmontop zelf 87 (vooral 1-px lijnen en glans).
- **Dubbele omlijning op naden:** grotendeels weg. Rest: bij de knoop (x49–52, y29–34) liggen het zwart van de handbal, de flank en de knoop vlak naast elkaar (zie zwak punt 5).
- **Koordjes echt om broek en arm:** cordão loopt als rood-donkerrode band schuin over de taille (deels onder de onderarm), knoop aan de onderflank, twee einden hangen recht omlaag (zwaartekracht). Prajiad: band om de bovenarm van de steunarm met een kort hangend eind, en een band om de vrije bovenarm.

## Zwakke punten (eerlijk)
1. **Haar leest nog niet echt als Eddy Gordo-dreads:** eerder dik, naar achteren gezet haar met lokken opzij. De losse lokken lezen alleen aan de onderkant (punten links). Geen paardenstaart/bundel; de rand-vorm van Hitmontop ging voor.
2. **Romp is een lange, rechte schuine plank** zonder borst of buik; de vrije bovenarm leest vooral als een band over de flank, de prajiad daarop als een rood vlekje.
3. **Benen zijn rechte, dunne buizen zonder knie**; het nabije been is erg lang; het bekken is een grote, vlakke blauwe driehoek (rechts nu wel ronder, r1c).
4. **Hals** is nauwelijks zichtbaar; de kop lijkt direct op de schouder te zitten.
5. **Knoop + handbal + flank** vormen bij de heup een druk, zwart cluster.
6. **Voeten:** de verre voet is Hitmontops voet op ware grootte, de nabije ±70 %. Ten opzichte van de nu veel langere benen zijn ze kleiner dan bij Hitmontop, maar de nabije voet blijft groot.
7. **Gezicht** is Hitmontops frons, niet ouder of zelfverzekerder gemaakt; het linkeroog plakt aan de gezichtsrand (zo staat het ook in Hitmontop).
8. **Compositie:** de figuur vult het hele vak (voet in rij 1, klauw tegen x63, hand op de onderste rij); de kop is groot en laag, dus op 1× leest de houding deels als "liggend" in plaats van handstand.
9. **Werkwijze:** de grove vlakken van romp, broek en benen (rand + simpele tintbanden langs de pose-lijnen) heb ik met een hulpscript gelegd (`ontwerp_draft.py`) en daarna met de hand herwerkt. Dat ligt dicht bij de "geen buizen-scripts"-regel; de romp/benen-zwakte (punt 2–3) komt daar deels vandaan. Een volgende ronde kan die delen beter rij voor rij uit de hand natekenen, met Hitmonlee (benen) en Hitmonchan (romp) als bouwstenen.

Niet gedaan (bewust): frame 2, rugsprite, icoon, shiny, naam/data. Niet gecommit.
