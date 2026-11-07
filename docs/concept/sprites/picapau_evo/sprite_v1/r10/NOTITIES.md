# Picapau-evolutie: sprite r10 (Swellows snavel letterlijk, op r9)

r9 blijft staan. Alleen de snavelzone (x6-22, y7-15) is veranderd.

## Jordi letterlijk
- Over r6: **"ik wil beide krullen bovenop naar achteren en die snavel is geen snavel, kijk bijv naar fearow of andere vogels, echt lelijk. Voor de rest is die wel prima. Alleen de buik is niet meer mooi ovaal. De pose is prima"**
- Over de snavel van r7: **"niet mooi, past niet bij het hoofd en is niet zo mooi als bij normale pokemon sprites"**
- Over r8: **"nee ik vind het ook nog niet zo mooi, hoe kunnen we dit beter maken, daarnaast is 1 van die slingers op zijn hoofd bijna een rechte lijn"** · op het voorstel "gezicht naar Swellow": **"probeer maar"**

## Coördinator over r9
De snavel was nog steeds een eigen ontwerp: een grote grijze steen met banden. Swellows snavel is klein en rond, met tinten die de vorm volgen. → **r10: Swellows snavel letterlijk overzetten**, daarna alleen de lengte (+2 px aan de punt) en een opening van 1 px.

## Werkwijze (bewijsbaar letterlijk)
1. **`swellow_snavel.py`**
   - Knipt de snavelpixels uit Swellow (`graphics/pokemon/swellow/anim_front.png`, eerste frame, x4-16 y11-19).
   - Neemt alleen Swellows snaveltinten mee, en het zwart aan de schaduwkant van de ondersnavel.
   - Kleurt ze om met een vaste tabel en verschuift ze naar onze snavelvoet: (x, y) → (x+8, y−4).
   - Uitvoer: `snavel_swellow.txt`.
2. **Kleurtabel** (Swellow → ons palet):

   | Swellow | rol | ons |
   |---|---|---|
   | m (230,180,98) | lichtste hoorn | a (crème licht) |
   | j (222,164,49) | lichte hoorn | b (crème basis = lichte hoorn) |
   | n (148,90,16) | midden | g (grijs) |
   | g (82,65,32) | donker, omlijning en mondlijn | G (donkergrijs, onze donkerste snaveltint) |
   | f (16,16,16) | zwart, schaduwkant ondersnavel | k |

3. **`maak.py`** = r9-tekening + Swellows bovensnavel (rij 8-11, letterlijk uit `snavel_swellow.txt`) + `aanpassing.txt`, daarna zet, bouw, controle, diff en platen.
4. **`aanpassing.txt`** bevat alleen deze aanpassingen:
   - **Gezicht rond de voet**: waar Swellow gezicht heeft, krijgt de onze gezicht. Rood b → oranje 2, de donkere naad e → 3. Dat geldt ook op de plekken waar de r9-snavel lag.
   - **Vleugel**: weer dicht waar de r9-snavel lag. In de mondopening vóór de ondersnavel is dat schaduw (4).
   - **+2 px aan de punt**: Swellows punt is doorgetrokken. De onder- en bovenkant van de bovensnavel blijven G, zonder nieuwe tint of band.
   - **Licht open**: Swellows ondersnavel staat 1 rij lager (rij 13-15). Daartussen loopt een dunne zwarte mondspleet (rij 12, x15-22).
   - **Twee kleine afwijkingen onderaan**, beide nodig om niets buiten de zone te breken:
     - Swellows laatste ondersnavelpixel valt achter de keel weg; (19,15) blijft de crème selout van de keel.
     - Zijn g op (10,18) wordt k, anders blijft er een losse G-pixel over.
5. **`bewijs.png`** (16×): Swellows snavel, de omgekleurde Swellow (`swellow_omgekleurd.png`; alleen de snavel in onze tinten) en onze snavel in r10. Pixel voor pixel dezelfde vorm, met de verlengde punt en de opening als enige verschil.

## Bevroren: bewijs
- `diff_uitvoer.txt`: **0 px verschil met r9 buiten de snavelzone**, in het raster én in de png.
- Binnen de zone veranderen 55 px; de lijst per pixel staat erin.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- 15 kleuren + transparant, 1740 px.
- **3 tintclusters kleiner dan 3 px, bewust, want het zijn Swellows eigen pixels:**
  - b (15,10) = Swellows losse j (7,14);
  - a (16-17,10) = zijn m m;
  - g (17,11) = zijn n (9,15). Die raakt los doordat de ondersnavel 1 rij zakt (bij Swellow hing hij aan de n van de ondersnavel).
- Opdracht 3 ("waar Swellow een tint heeft, krijgt de onze die tint") gaat hier vóór de clusterregel.

## Bestanden
- `picapau_evo.png`, `normal.pal`, `raster.txt` en `tekening.txt`.
- `controle_uitvoer.txt` en `diff_uitvoer.txt`.
- `vel.png`: 1× en 8×, r10 naast r9 en Swellow.
- `kop_closeup.png`: 16×, kop r10 en r9 naast Swellow.
- `bewijs.png` en `swellow_omgekleurd.png`.
- `snavel_swellow.txt` en `aanpassing.txt`.
- Draaien: `python3.11 swellow_snavel.py && python3.11 maak.py`

## Eerlijke zwakke punten
1. **Hij is nu klein.** De snavel is 11 px van punt tot voet, Swellow-formaat. Op 8× leest hij als een kleine, ronde zangvogelsnavel. Spechtachtig is hij nauwelijks: +2 px maakt geen beitel.
2. **Contrast met de vleugel.** De snavel ligt tegen de donkere verre vleugel. De omlijning G (donkergrijs) en de vleugel (v/4) liggen dicht bij elkaar in helderheid, waardoor de punt en de onderkant op 1× wegvallen. Bij Swellow ligt de snavel tegen de lichtgroene achtergrond.
3. **Warm en grijs gemengd.** De tabel geeft crème (a/b) bovenop en grijs (g/G) onder. Dat is hoorn-achtig, maar a/b liggen dicht bij de crème van de keel en het witte vlak.
4. **Mondspleet.** Door de opening van 1 px liggen twee donkere lijnen onder elkaar: de zwarte spleet en Swellows G-mondlijn op de ondersnavel. Op 16× is dat iets zwaar.
5. **Donkere vlek op het voorhoofd.** Swellows donkere naad (e → 3) wordt bij ons een bruine vlek op (18-19,9) en (20-21,10) boven de snavel. Bij Swellow is die naad rood-op-rood; bij ons valt hij meer op.
6. **Tintclusters.** Er staan 3 tintclusters van 1-2 px in de snavel (zie Controle). Dat is volgens de opdracht, maar tegen de norm.
7. **Niet gekeurd.** Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd.
