# Regicosmo frontsprite, ronde 2 (maker)

r2 = r1 (`../r1/r1.npy`) + drie benoemde reparaties van Claude. Bouwen: `cd docs/concept/sprites/regicosmo && python3 sprite/r2/bouw.py && python3 sprite/r2/vel.py`.
Bestanden: `regicosmo_r2.png` (64×64, P, index 0 transparant, 16 kleuren incl. transparant, 62×47, 7 losse delen), `vel.png` (r2 8× | r1 8× | model; close-ups 16× Saturnus en asteroïde: r2 | r1 | natief model; 1×/2× op licht en donker; r2 naast Regiaqua/Regirock/Registeel gba).

**Bewijs:** `bouw.py` telt de diff r1→r2 per zone; **buiten de drie zones 0 px**. Saturnus 37 px, asteroïde 16 px, ijs 4 px.

## 1. Saturnus (37 px): ronde bol + schuine ellipsring, gemeten (`saturnus.py`)
- Bol: cirkelfit (kleinste kwadraten) op de planeetrandpixels die aan de achtergrond grenzen: natief c=(173,45; 55,04) r=8,60 → sprite c=(55,11; 30,28) **r=4,10 (diameter 8,2 px)**. Pixels met middelpunt binnen r. Kleur per pixel = meerderheid van de planeetkleuren (perzik/oranje/rood/donkerrood) in de modelcel. Buitenlijn: lichtkant donkerrood, schaduwkant zwart (normaal vanuit het middelpunt).
- Ring: de twee uiterste ringpunten natief (159,5; 62,5) en (189,5; 46,5) → **kanteling −28,1°**, halve lengte 17,0 natief; middenlijn = halve lengte − ½ ringband (1,75) → **a=7,27 px**; halve korte as = mediane afstand van de grijze ringmiddenlijn vóór de bol (3,53 natief) → **b=1,68 px**; centrum (55,61; 30,02).
- Ringband = pixels binnen 0,95 px van de middenlijn (modelband 3,5–4 natief = 1,7–1,9 px); de pixel het dichtst bij de middenlijn grijs (middenlijn doorlopend gemaakt met de dichtstbijzijnde bandpixel), de rest donkere ringrand (bruin donker; zwart alleen tegen de achtergrond aan de schaduwkant). Voorkant van de ring over de bol, achterkant alleen naast de bol. Gaten in beide lussen ontstaan vanzelf waar de ellips binnen de bol noch de band ligt: rechts (60,27), links (51,32), zoals het model.
- Bbox Saturnus x48–62, y25–34 (model ×0,477: x48,2–63,0, y25,5–35,0).

## 2. Asteroïde (16 px): holte en inkeping
In r1 was bijna alles bruin donker, dus de holte las niet. Nu per binnenpixel de gemiddelde modelhelderheid L van de asteroïdepixels in de cel: L < 72 → bruin donker (holte linksboven (4,43) (5,43) (3,44) (4,44), inkeping boven, schaduw rechtsonder), 72–112 → bruin midden, ≥ 112 → asteroïde licht (streep). Rand ongewijzigd, geen zwart binnen.

## 3. IJs (4 px)
Per binnenpixel de modelhelderheid: cyaan (gedeelde stipkleur) alleen onder L 208 (= midden tussen de twee ijsclusters van het model, L 183 en 232; ook het 30e percentiel van het ijs), anders bijna-wit. Uitkomst: 36 px bijna-wit, 16 px cyaan als sikkel rechtsonder. r1 had al bijna deze verdeling (34/18); het verschil zit in 4 px.

## Twijfels
- Saturnus: de bol is rond en de ring steekt links en rechts uit met twee gaten, maar de linkerarm snijdt de linkeronderkant van de 8-px-bol, waardoor de bol op 8× nog iets schuin leest. Onder de ring blijft geen rij planeetkleur over (bodem van de bol = buitenlijn).
- IJs: de sikkel is volgens de meting 2 px dik onderaan; als het cyaan te verzadigd blijft, is de tint zelf het punt (stipkleur, Jordi's wens), niet de verdeling.
