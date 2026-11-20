# Hoatzin fase 2, r19 (20 nov)

Jordi op r18: "nek is nog niet goed doorgetrokken ... de 2 poten zitten aan elkaar vast en de rechts heeft opeens rare zwarte uiteinden",
daarna: "ja en ook kleuren, schaduw, belijning. Hij moet echt op het model lijken, de onderdelen van het lichaam moeten ook niet in elkaar overgaan" ·
"alleen de kleuren die we besproken hebben mogen afwijken" (buik variant D, kuif wat bruiner).

`sh alles.sh`. Vorm = r17 (alpha-diff 0 boven y 50); alleen de poten kregen een nieuwe vorm. check.py: dambord 0, om-en-om 0, klonten 0. 16 kleuren.

## Vorm (bouw19.py)
- Neklijn: vaste lijnpositie per rij y 23–40 (LIJN), 1 px, 8-verbonden; lichte vleugelvoorrand (4/5) ernaast als eigen strook.
- Poten los: buitenlijn van de voorste voet loopt over y 56 door tot x 25 (model: donker op (25,57) en (28,56)).
- Rechterpoot per pixel uit het model: voet y 57–58 grijs, rechter teen y 56–57 met klauw (37,57), linker teen schuin omlaag met klauw (24,61), teen omlaag x 29–31 met klauw (29,63); zwarte blokjes (35–37,56–59) weg.

## Kleur (kleur19.py, delen.py, meet.py)
- Palet uit de modeltinten per zone (meting op het r17-pixelblad), alleen helderheid uit elkaar: lijn #1C101A, donker #3C2D3D (vleugel #422A3B/poot #3B3749 gedeeld), vleugel #6A4C5F, nek #8C6B7D, strepen #A8909F (model #BDA2B5, L 174→150), blauw #2E356A/#5D6FBC, oog #B05484 (model-iris), grijs #5F5B6B/#8E8A9C. Afwijkend (besproken): buik D, kuif #693D32/#925649 (bruiner).
- Onderdelenkaart: kuif, verre vleugel (de mauve veren achter de kuif), kop, nek, vleugel, buik, staart, poten, gezicht. Grenzen: binnenlijn op het achterste deel (diepte vleugel > buik > poot > kuif/gezicht > kop > nek > staart > verre vleugel); kop/nek, kuif/kop en kuif/verre vleugel via toonsprong.
- Vulling per pixel uit de gladde modeltoon; vleugel: lichte schachtstrepen (≥4/9 lichte modelcellen) 4-verbonden gemaakt (geen dambord), penscheiding (≥5/9 modelcellen L<65) in de donkere tint; verre vleugel een stap donkerder; poten 3 tinten (licht bovenkant/midden/donker onderkant, verre poot een stap donkerder).
- Opschonen: dambord → diagonaal orthogonaal verbonden (27), losse pixels (28), klonten.

## Zwak / niet gedaan
- Kuifstrengen zijn nog geen losse strengen (model ±⅓ px); het is een bruine massa met lichte en donkere vlekken.
- Vleugelstrepen zijn korte stukjes, geen doorlopende diagonaal per pen.
- Buitenlijn overal zwart (geen gekleurde selout aan de lichtkant).
- Niet naast Archeops/Braviary gelegd.
- vel.png: r19 | r17 | model op 8×, daarna kuif/nek/vleugel/poten op 16× (r19 | r18 | pixelblad | model).
