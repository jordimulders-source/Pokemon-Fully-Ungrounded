# Eindkeuring regionale Hitmonchan (Dragonfly Cave): ek1

Gekeurd: `../sprite/kandidaat.png` (maker r7) tegen het model `../gemini/r3.png` (natief 50×81, dezelfde stuksgewijze afbeelding als `meet.py`: gezicht 1-op-1, de rest ±76 %), naast Gen 3 Hitmonchan (`anim_front_gba.png`), Dundragoon en Skinguin. Ik heb eerst zelf geoordeeld en pas daarna de notities van de maker gelezen.

**Resultaat:** `ek1.png` (64×64, geïndexeerd, zelfde 7 kleuren + transparant, geen nieuwe tint), `ek1_8x.png`, `vel.png` (kandidaat | ek1 | model | Gen 3 op 8×, 1×/2× op licht en donker, diff). Scripts: `ek1.py` (asserts op de oude waarde), `vel.py`.
**25 pixels gewijzigd, alleen de tint; silhouetdiff 0; de gezichtszone (rij 18–26 × kol 33–43) is niet aangeraakt.**

## Oordeel per eis
- **(1) Accuraat op het model: PASS.** Pose, kubussen, kuif, gezicht, riem, rok en benen volgen het model per pixel. Het gezicht is gelijk aan het gekwantiseerde model (gecontroleerd). Het hoofd is naar verhouding ±1,3× groter, en dat volgt uit "ogen niet kleiner".
- **(2a) Schaduw: PASS.** Licht linksboven klopt op alle delen. De facetten lezen als uitgehakt ijs. Beide kubussen hebben drie vlakken: boven licht, de ene zijkant midden en de andere donker. De glanspunten (wit) staan op kubusranden, de kuif en de rok, allemaal op modelplekken.
- **(2b) Belijning: kandidaat BIJNA, ek1 PASS.** Een open lichte rand, gaten in de schaduwlijn en selout die om-en-om wisselde zijn gerepareerd (zie onder).
- **(2c) Kleurtinten: PASS.** Er zijn 7 tinten met stappen van ±30–45 helderheid. De kleine clusters zijn facetranden en glans uit het model (gemeten met M_gem/M_licht). Ik heb ze bewust niet weggepoetst (pixelblur-regel).

## Wijzigingen (x,y oud→nieuw)
**Opgeheven arm en kubus**
- (16,14) 1→2, (16,15) 1→2: selout aan de lichte kant van de onderarm. Model 127/140; vanaf rij 17 is het model donker (≤93), dus daar blijft navy. Dit haalt ook het om-en-om 1/2/1 bij (17,16) weg.
- (17..21,13) 1→2: de naad tussen kubus en onderarm wordt een binnenlijn in de eigen donkerste tint. Het model meet daar 54–84, dichter bij 2 (71) dan bij navy (26). De naad blijft zichtbaar, maar leest minder als een "opgeplakt" blok. De hoekpunten (15,13), (16,13) en (22,13) blijven navy.
- (22,24), (22,25) 1→2: een los navy-streepje tussen arm en schouder; het model meet 108 en G=2.

**Kuif**
- (29,11) 3→4: de linkerrand ging 4/3/4 om-en-om.

**Wachtkubus**
- (50,30) 4→1: een lichte pixel in de rechter schaduwlijn liet een gat tussen (50,29) en (51,31).

**Rok**
- (24,45) 1→2, (25,46) 1→2: de zoom van de rok over de dij is een binnenlijn in de eigen tint (model 131/103). De buitenrand van het kruis blijft navy.

**Benen**
- Verre dij rechtsboven (43,44) 4→2, (44,45) 4→2, (45,46) 4→1, (45,47) 4→1: hier was een open, lichte rand aan de schaduwkant. Het model heeft daar zelf ook geen lijn; die is toegevoegd als Gen 3-eis, alleen als tint en zonder vormwijziging.
- Nabije been links (19,48) 4→3, (17,51) 4→3, (15,55) 3→2: de selout wisselde om en om. Nu is hij 3 op dij en knie en 2 op de scheen.
- (22,51) 3→1: een lichte pixel in de navy schaduwlijn van de scheen (model 76).
- (38,49) 3→2: de binnenkant van de verre knie ging 2/3/1; nu 2/2/1.
- Verre voet, bovenrand (44,55) 4→3, (45,55) 2→3, (46,56) 4→3: de rand ging 4/2/4; nu een rustige 3 (model 117–140).

## Open / ter info voor Jordi
- De navy binnenlijnen voor kin, riem en kuifsneden zijn gebleven. Het model meet daar 23–60 (dichter bij navy), en Gen 3 Hitmonchan heeft daar ook zwart.
- Naad onder de opgeheven kubus: in ek1 is het midden een donkerblauwe binnenlijn. Wil Jordi de harde navy-naad van het model terug, dan zijn dat 5 pixels terug naar 1.
- Het oog (7×5, uit het model) leest op 1× als een smal, boos oog. Ik heb het niet veranderd (Jordi: ogen het belangrijkst, niet kleiner).
- Er zijn 8 paletplaatsen vrij gebleven. Een extra tint was niet nodig.
