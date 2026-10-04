### The Spire: slankere toren (voor de changelog)
- Jordi: "het ontwerp is goed, maar hij mag dunner; het moet echt een spits zijn." De toren in BattleFrontier_OutsideWest is nu een slanke spits in dezelfde Frontier-stijl (Battle Tower-gevel: wit glas, baksteenrode pijlers, blauwe ruiten, leien luifel, oranje/rode dakranden).
- Voet 9 breed (x 29-37) i.p.v. 15, met de echte Battle Tower-ingang (luifel, glazen zuildeuren, geanimeerde schuifdeur op (33, 26), warp id 11 naar de lobby, ongewijzigd).
- Trappen 9 -> 7 -> 5 -> 3 breed, elke trap korter dan de vorige (schacht 7, 4, 3 en 2 rijen), met een dakrand per trap; bovenop een lange antennenaald van 4 rijen met rood baken en drie oranje ringen. Totaal 28 rijen hoog.
- Smalle pijlers en ruiten zijn samengesteld uit twee halve Battle Tower-kolommen (linkerhelft + rechterhelft), zodat ze beide randen houden; alleen kleuren uit de bestaande paletten 9/10 (gelijk aan East).
- Plein hersteld: hek op de noordrand loopt weer tot tegen de toren, vlaggen op x 27 en 39 staan er weer, de rots in zee rechts van de toren (x 41-42) is terug.
- Kost nu 41 metatiles en 47 tiles (vorige versie meer); de rest van de oude brede toren is vrijgegeven.
- Bouwscript: `tools/grounded/maptools/spire_tower.py` (idempotent vanaf commit 6744d697). Getest in de emulator: plein -> deur -> lobby -> terug naar buiten.
