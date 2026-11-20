# Kelp-Oddish frontsprite, ronde 1

Bestanden: `oddish_r1.png` (64×64, geïndexeerd, index 0 transparant), `vel.png`, `kaal.png` (kale reductie zonder opschoning), `bouw.py`.
Gereedschap: `../gereedschap/` (natief.py, klassen.py, gemeen.py, vel.py).

## Wat uit het model komt
- Natief raster teruggehaald: pitch 10,24 px (fase 9,25) → 99×99, figuur 57×60 (`gereedschap/natief.png`).
- Verkleind tot 33×35 (schaal 35/60) op de plek van de Oddish uit de game (x21–53, y14–48; voeten op y48), met **oppervlakteweging per spritepixel**: achtergrond als > 50 % wit; zwart als ≥ 25 % van de pixel modelzwart is (zo blijven 1-px modellijnen doorlopend); verder de groep (turquoise/olijf/rood) met het grootste oppervlak, binnen turquoise de modelklasse met het grootste oppervlak, binnen olijf de gemiddelde modelhelderheid (lange donkerbruine modellijnen ≥ 5 natieve px blijven lijn).
- Gezicht (8 px) op de gemeten modelplek: rood-oppervlak per spritepixel uitgerekend; ogen 1×2 (model 2×3 natief = 1,2×1,75 spritepx; rechteroog 1 px lager, zoals in het model), mondje 2×2 met donker linksboven en rood rechtsonder (zoals het model). De lichte glans in de modelogen is < ½ spritepixel en valt weg.
- Kleuren = modelkleuren per klasse (turquoise 4, kelp 4, rood 2, zwart).

## Technisch opgeschoond (t.o.v. de kale reductie: kelp 58, lijf+gezicht 19, voeten 14 px)
- Buitenlijn (59 px): geen open of lichte rand; rand met achtergrond rechts/onder = zwart, lichtkant = donkerste tint van de groep (gekleurde selout), zoals het model zelf al grotendeels doet.
- Ontkorrelen (19 px): tintvlekjes < 3 px (hooglicht < 2) naar de buurtint van dezelfde groep.
- Zebra (5 px): een korte kelplijn die 3× op 2 px naast een andere lijn liep (ladder) wijkt voor de vlaktint.

## Zelfgenoemde zwakke punten (→ r2)
- Hooglichten in de kelp grotendeels weggemiddeld (drempel 0,3 te streng).
- Eén lichte kelppixel ingesloten door zwart aan de punt van het onderste rechterblad (52,28).
