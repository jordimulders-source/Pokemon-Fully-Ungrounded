# Fakemon-checklist: vorm, pose en kenmerk

> De Gen 4–9-sprites in de expansion zijn **niet van Game Freak** maar door fans in Gen 3-stijl gemaakt (bijv. Galar-Linoone, Obstagoon). Ze lezen toch als echte Pokémon: het bewijs dat deze checklist met eigen pixelwerk haalbaar is (Jordi, 23 okt).

Verplicht voor **elke** fakemon-sprite (silhouetronde én volledige sprite), naast `SPRITING.md` §0 en `SPRITE_OPDRACHT.md`. Onderbouwing, cijfers en vellen: `docs/lessen/vormstudie/STUDIE.md` (1024 echte sprites, Gen 1–9). Het doel is niet "precies Gen 3", maar **duidelijk een Pokémon** (Jordi): de punten hieronder gelden in alle generaties.

**Gebruik:** de sprite-agent vinkt elk punt af in NOTITIES.md (`A1 ok` / `A1 fout: …, gerepareerd door …`); de keurder keurt met dezelfde nummers. **H** = harde eis (vrijwel alle Pokémon; een fout is een afkeur). **R** = richtlijn (afwijken mag met een reden in NOTITIES.md). Meten kan met `vormstudie/tools/` (`metrics()`/`shape()` in `lib.py`/`shape.py`; `zoom.py` zet je sprite naast echte).

## 0. Pose kiezen (vóór de eerste pixel)
Vul dit sjabloon in NOTITIES.md in en laat het bij de silhouetronde keuren:
```
Bouwtype:        (kleine/grote viervoeter, tweevoeter klein/groot, vogel, slang/vis, bol, insect, aap, langnek)
Fase:            1 / 2 / 3 / losse soort   → doeloppervlak en box (tabel D)
Type+karakter:   (bijv. Dark, dief, brutaal)
Pose (P1–P15):   uit de catalogus in STUDIE.md, met reden
Skelet-sprite:   2–3 echte sprites in die pose en dat formaat (vormstudie/vellen/)
Snuit:           lang → één oog / kort → twee ogen (B2)
Dominant kenmerk: wat steekt uit het silhouet, en waar (A2)
Tegenwicht:      wat staat rechts(boven) tegenover de kop (A3)
```
Pose naar karakter (R): Fighting → P7 vechthouding (brede A-stand, nabije vuist voorop); Psychic/Fairy/genezer → P8 rechtop/zwevend, één hand met gebaar; Dark/dief/jager → P3 laag sluipend, kop op schouderhoogte; Ghost → zwevend zonder grondlijn; Normal/Fire/Electric-hond → P1 alert; hoefdier → P2 één voorpoot geheven; knuffeldier → P4/P5 zittend; aap → P9 dynamisch met staart; tank (Ground/Rock) → P15 laag en breed; bol → P14.

## A. Silhouet en kenmerk
| # | Eis | Toets | Voorbeelden |
|---|---|---|---|
| A1 | **H** Silhouet leest als de soort | Eén kleur op 1× naast de referentiefoto en 2 echte sprites: een buitenstaander noemt het dier | Pikachu, Eevee, Poochyena |
| A2 | **H** Eén dominant kenmerk breekt de omtrek | Het kenmerk steekt uit het silhouet (niet binnen de romp) en is op 1× als vorm te zien; een accessoire is hooguit het tweede kenmerk | Cyndaquil-vlam, Vulpix-staarten, Chikorita-blad |
| A3 | **H** Diagonale compositie | Kop linksboven; massa loopt naar rechtsonder; staart/kenmerk geeft tegenwicht rechts(boven). Kijkrichting links(-voor) | Growlithe, Skitty, Meowth, Luxray |
| A4 | **H** Negatieve ruimte | Soliditeit 0,65–0,80 (bol/vachtberg: richtlijn, echte haalt tot ±0,93, Piloswine); lucht tussen poten, tussen staart en lijf, tussen arm en romp | Mightyena 4 poten los, Meowth staartboog |
| A5 | **H** Niet symmetrisch | Symmetrie-score < 0,80 (bol/vachtberg: richtlijn, echte tot ±0,90: Jigglypuff 0,87, Wooloo 0,89); geen gespiegelde ledematen, oren of ogen | Teddiursa, Jigglypuff (gezicht links) |
| A6 | **R** Geen bouwblokken | Geen zuil (evenwijdige randen > 6 px), doos (rechte rug/buik > 4 px) of stok (rechte poot zonder knik) | Ponyta-nek taps, Mightyena-buik in boog |

## B. 3/4-constructie en gezicht
| # | Eis | Toets | Voorbeelden |
|---|---|---|---|
| B1 | **H** Kop draait meer naar de kijker dan het lijf | Lijf 3/4–profiel (verre poten/flank zichtbaar en kleiner); kop 3/4–bijna frontaal. Kop en lijf nooit allebei profiel of allebei frontaal | Growlithe, Eevee, Vulpix, Lillipup |
| B2 | **H** Snuitlengte bepaalt de ogen | Lange snuit (±⅓ van de kop of meer voorbij het oog) → één oog, neus = meest linkse punt van de kop. Korte snuit → twee ogen, neus tussen en 1–3 rijen onder de ogen. Twee ogen op een lange profielsnuit = afkeur | één oog: Poochyena, Ponyta, Charmander, Torchic; twee: Shinx, Eevee, Mudkip |
| B3 | **H** Twee ogen = perspectief | Verre oog 1–2 px smaller en dichter bij de kopomtrek; neus/mond links van het kopmidden; oogmiddens niet op exact gelijke afstand van het midden | Growlithe, Meowth, Jigglypuff |
| B4 | **H** Snuit is één vorm in de kijkrichting | Oog-as en snuit-as wijzen dezelfde kant op (links-voor/-onder); de snuit komt schuin uit het gezicht, niet recht opzij uit de schedelrand | Poochyena, Mudbray, Vulpix |
| B5 | **R** Oren volgen de draai | Verre oor hoger/achter of deels bedekt; de twee oren verschillen in vorm of hoogte | Poochyena, Eevee, Teddiursa |
| B6 | **H** Kop overlapt het lijf | Kleine soort: kop vóór de borst, nek onzichtbaar. Langnek: nek schuin naar voren en taps, kop schuin op de nek | Eevee, Growlithe; Girafarig, Ponyta |
| B7 | **H** Gezicht compleet en niet menselijk | Ogen, mond (ook als 1–2 px), neus/snavel; geen menselijke neus | Machamp, Hitmonchan |

## C. Pose en ledematen
| # | Eis | Toets | Voorbeelden |
|---|---|---|---|
| C1 | **H** Alles geteld | Aantal poten/armen/oren/ogen klopt met het dier; verre kant aanwezig (kleiner, donker), niets geamputeerd | Mightyena, Treecko |
| C2 | **H** Viervoeter: 4 kolommen, 3–4 voethoogtes | Nabije voorpoot laagst en meest links; verre voorpoot 1–3 px hoger en rechts erachter; verre achterpoot tussen de nabije in, hoger; ≥ 1 kolom lucht of omlijning tussen poten | Mightyena, Mudbray, Poochyena |
| C3 | **H** Elk ledemaat hangt onder zijn eigen schouder of heup | Trek een lijn van schouder/heup naar voet: geen poot midden onder de buik, geen verre poot vóór de nabije (Escher) | Mightyena, Luxray |
| C4 | **H** Gewrichten | Achterpoot met hak naar achteren, voorpoot of arm met knik; geen twee rechte evenwijdige stokken | Ponyta, Liepard, Mudbray |
| C5 | **H** Ledematen groeien uit de romp | Schouder en heup zijn bollingen in de omtrek; de poot begint binnen de romp (overlap), nooit als T onder een rechte buik | Growlithe, Mightyena |
| C6 | **H** Nabij ≠ ver | Verre ledematen korter, hoger, in schaduwtint, deels achter de nabije; ze doen iets anders (hoek, hoogte) | Pikachu, Chimchar, Treecko |
| C7 | **H** Eén houding met gewicht | De voeten op de grond dragen het zwaartepunt; geen ledematen die "in de lucht grijpen" terwijl de rest stilstaat | Hitmonchan (stand + vuisten), Ponyta (3 dragen, 1 geheven) |
| C8 | **R** Staart sluit aan en buigt | Staart begint aan achter-/bovenkant van de heup, boog of S, liefst omhoog als tegenwicht; geen rechte buis | Growlithe, Skitty, Pachirisu, Aipom |
| C9 | **R** Pose past bij het karakter | Pose uit het sjabloon (§0) is herkenbaar: een keurder zonder briefing raadt het karakter (vechter, sluiper, kalm, speels) | Primeape, Liepard, Gardevoir, Aipom |

## D. Verhoudingen en formaat
| # | Eis | Toets | Voorbeelden |
|---|---|---|---|
| D1 | **H** Oppervlak per fase | Fase 1: 700–950 px (box ±36–42); fase 2: 1100–1550 (±47–53); fase 3: 1700–2600 (±58–63); baby 450–700; losse soort 1200–1600 | starters 798 / 1226 / 2082 |
| D2 | **H** Kop per fase | Kophoogte/totale hoogte: fase 1 ±40–55%, fase 2 ±30–35%, fase 3 ±20–30% | Torchic 50%, Combusken 30%, Blaziken 20% |
| D3 | **H** Fase 1 = compacte romp | Romp peer/boon, grotendeels achter of onder de kop, ledematen kort en stomp; geen lange volwassen romp | Poochyena, Cyndaquil, Teddiursa |
| D4 | **R** Breedte past bij de fase | Box breedte fase 1 ≤ 48 px inclusief staart; daarboven eerst de staart opkrullen of de romp inkorten | Vulpix 48, Zigzagoon 56 (uitzondering: laag dier) |
| D5 | **R** Groei binnen de lijn | Fase 2 ≈ 1,5–1,7× fase 1, fase 3 ≈ 2,3–2,6×; dezelfde kenmerken, kop relatief kleiner | Treecko→Grovyle→Sceptile |

## E. Omlijning, shading en kleur (aanvullend op SPRITING.md §0)
| # | Eis | Toets | Voorbeelden |
|---|---|---|---|
| E1 | **R** Verre kant donkerder | Verre ledematen, verre flank en verre oor in de schaduwtint of donkerder; dat verkoopt de diepte meer dan omtrek alleen | Mightyena, Mudbray |
| E2 | **R** Overlap met omlijning | Waar een nabij deel over een ver deel ligt, scheidt een omlijning in de omlijningsbasis (niet zwart) ze | Growlithe-poten, Meowth-staart |
| E3 | **R** Omlijningsdonkerte binnen de Pokémon-band | Aandeel zeer donkere pixels ±0,10–0,25 (Gen 3 ±0,13, Gen 4–9 ±0,20); hoger mag bij een Dark-type of donkere vacht | Umbreon, Poochyena |

## Mini-sjablonen per bouwtype
- **Kleine viervoeter fase 1** — skelet: Poochyena, Growlithe, Shinx, Lillipup, Eevee (staand); Vulpix, Skitty (zittend); Nickit, Purrloin (laag). Oppervlak 750–950, box ±40×40. Kop ±45–50% van de hoogte, overlapt de borst. Lange snuit → één oog (Poochyena), korte → twee (Shinx). Vier poten, korte stompjes, 3 voethoogtes. Staart omhoog als tegenwicht.
- **Grote viervoeter fase 2/3** — skelet: Mightyena, Luxray, Arcanine, Liepard, Mudsdale. Oppervlak 1400–2400, box 55–63. Kop ±25–30%, hoger dan de rug. Vier lange poten met hak en lucht ertussen, soliditeit ±0,66. Eén voorpoot vaak vooruit of geheven.
- **Langnek/hoefdier** — skelet: Ponyta, Mudbray, Deerling (fase 1); Girafarig, Rapidash, Sawsbuck (later). Nek schuin vooruit en taps, kop schuin erop met één oog (lange snuit). Romp = grootste massa. Hakken naar achteren, één voorpoot geheven (R).
- **Kleine tweevoeter fase 1 (starterhouding)** — skelet: Charmander, Torchic, Chimchar, Piplup, Riolu, Pikachu. Oppervlak 700–900, box ±36×42. Kop 40–55%. Voetjes wijd en verschillend; nabije arm voor de romp, één arm iets omhoog; staart rechtsachter.
- **Zittende tweevoeter/knuffeldier** — skelet: Teddiursa, Munchlax, Bidoof, Grookey. Romp schuin achter de kop, één oor hoger, één arm naar mond of omhoog; beentjes vooruit en verschillend.
- **Aap/klimmer** — skelet: Aipom, Chimchar, Monferno, Mankey, Pansage. Kop rond, gezicht met twee ogen naar de kijker, ledematen in verschillende richtingen, staart als krul of vijfde ledemaat.
- **Grote tweevoeter fase 3** — vechter: Hitmonchan, Infernape, Incineroar (A-stand, vuist voor); Psychic: Gardevoir, Alakazam, Gothitelle (rechtop, één hand); tank: Ursaring, Swampert, Pangoro (laag en breed). Box 58–63, kop 20–30%.
- **Vogel** — skelet: Starly, Taillow, Murkrow (staand); Pidgeot, Braviary (vliegend); Hoothoot/Rowlet (uil, twee ogen). Snavel in profiel → één oog. Nabije vleugel groot en open, verre kleiner en achter.
- **Slang/vis** — skelet: Ekans, Dratini, Seviper, Milotic; vissen Goldeen, Magikarp, Barboach. Kop hoog links, lichaam in S of lussen rechts-onder met overlap; vissen schuin gekanteld.
- **Bol/blob** — skelet: Jigglypuff, Clefairy, Whismur, Wooloo, Mareep. Gezicht links van het midden (symmetrie < 0,85), één kenmerk dat de bol breekt (kuif, oren, staart), pootjes op verschillende hoogte.
- **Insect** — skelet: Ledyba, Venonat, Kricketot, Nymble, Joltik. Mag het meest frontaal; gelijke dunne pootjes mogen (Dragonfly Cave-gids), maar vleugels en voelsprieten verschillen per kant.


> Uitzondering uit de keuring (23 okt): **langnekken** (alpaca, Mudbray 42×51, Girafarig) halen de kopverhouding en de box van ±42 px niet; voor hen is dat een richtlijn.
- **Zijaanzicht mag (Jordi, 25 okt):** naast 3/4 bestaan veel echte sprites in (bijna) zijaanzicht, vooral vliegers en vissen (Yanma, Ninjask, Swellow, Taillow, Wingull, Skarmory, Latias, Magikarp, Wailord); kies wat bij het dier past.
