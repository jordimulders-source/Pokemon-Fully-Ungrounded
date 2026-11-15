# Gengas sprite v8a / v8b (15 nov) – geen vlak meer om de ogen

Jordi over v7: "nu is het een soort vlak om de ogen heen wat totaal niet meer bij de rest van de sprite past" · "ja het moet er allemaal consistent uit zien ook".
Keten: `python3 v8.py && python3 maak.py && python3 vel.py` (v8.py bouwt beide vanaf `../sprite_v5/raster.txt`; reden per pixel in `raster_v8a.txt.log` / `raster_v8b.txt.log`).
**Diff t.o.v. v7 buiten x 6–36, y 24–48 en de krulzone x 34–47, y 27–40: 0** (v8.py meet het, beide varianten).

## Gemeenschappelijk
- Gengar-gezicht als één blok op (x−6, y+5), zoals v7; Gengars d-pixels worden niet geplakt: daar blijft de bandtint eronder (geen ring).
- Slot u vrijgemaakt: de 13 oude u-pixels (randvlek linksboven, rest van de wig) → b (ΔE 8,6); slot u = Gengars tandlijn (106,98,123) exact. Tandschaduw 2/7 blijft H.
- Krul (MOET 1 keuring v7): hoeken (38,34) en (38,36) van de binnenlus weg → lus loopt rond met 1-px trapjes; losse pixels (38,28), (36,29), (39,37), (39,33), (43,34) opgenomen. Lijntint (b) blijft modeltint.
- Niet gedaan: tint a/b uit elkaar trekken (±17 helderheid): dat zijn modeltinten die over de hele bol gebruikt worden; voorleggen.

## v8a – banden zoals het model
Lijftinten in de gezichtszone = v5 (model met gezichtsblok +5/+1); oud modelgezicht weggehaald en gevuld met de buurtint. De donkere band loopt doorlopend van rechtsboven door het gezicht naar de linkerrand, zoals in het model; de lichte modelstrook tussen de ogen (l, rij 29–30) blijft.

## v8b – band als strook over het voorhoofd
Donkere band (b) loopt vanaf de bestaande band rechts over het voorhoofd naar de linkerrand, golvende onderrand 1 rij boven de ogen (rij 29–32, trapjes 1–4 px), bovenrand rij 25–29 met een m-rij als overgang naar l (zoals de andere banden). Onder de band: ogen op m (sluit rechts aan op de lichte band naast het gezicht, links op l); onder de grijns de modelbanden.

## Zwakke punten (eigen)
- v8a: het gezicht ligt weer in de donkere band (zoals het model); het rode oog-op-donker kan Jordi's oude "kuil"-gevoel teruggeven.
- v8b: de m-strook onder de band links van het linkeroog (x8–16, y32–37) is het meest "effen" stuk; links boven wordt de rand een grote b-vlek doordat u → b ging.
- Beide: tandschaduw (Gengar 2) nog als H.
