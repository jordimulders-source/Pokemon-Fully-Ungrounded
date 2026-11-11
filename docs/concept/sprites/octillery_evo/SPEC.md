# Octillery-evolutie (Water/Steel, Humboldtinktvis) – SPEC

Bevroren ontwerp: `referenties/gemini_gekozen_r5.png` (Gemini r5). Kanonpositie-voorbeeld: `referenties/gemini_r9_kanonpositie.png`. Schets van de indeling: `schets_tentakels.png`.

## Jordi letterlijk (10 nov)
- "ik vind 5 grotendeels goed, op denk ik de gekrulde vorm van de tentakels na"
- "mond mag best blijven tenzij we er echt een gatling gun van kunnen maken" (Claude: op 64×64 niet leesbaar; mond blijft)
- "ik vind de vorm van de kanonnen tof, daarvan wil ik er 2 op de schouders hebben, dan mogen 2 tentakels opgerold zijn alsof het een rupsband is, het blijven voor de rest 100% de tentakels zoals hier, twee andere tentakels spreiden iets meer uit om het toch nog op een humboldt squid te laten lijken en het silhouet niet te rond te maken"
- Over de schets: "qua idee wel, qua positie nog niet helemaal" ; "het hoofd blijft helemaal hetzelfde, ontwerp, textuur, positie etc"

## Toegestane afwijkingen van r5 (alleen deze)
1. De twee kanonnen (vorm van r5) over de schouders, positie zoals r9.
2. Twee tentakels opgerold als rupsband (verder 100% de tentakels van r5).
3. Twee tentakels iets meer gespreid (silhouet minder rond, meer Humboldt).
De oude krullen verdwijnen. Kop, mantel, ogen, mond: 100% r5 (ontwerp, textuur, positie).

## Stappen
1. Aangepast model op Gemini-resolutie, gebouwd uit r5-onderdelen (kop pixel-identiek) → Jordi keurt de posities.
2. Daarna pas de sprite (SPRITE_WERKWIJZE "Gemini-model namaken").

## Model
- **v1 (10 nov):** `model/model_v1.png`. Jordi: "die linker tentakel gaat wel, maar voor de rest ziet het er allemaal echt verschrikkelijk uit".
- Jordi over v1 (10 nov): "de kanon [linksboven gaat wel]. De rupsband tentakels zijn gewoon nagetekend en heel slecht, veel te dun, lijken totaal niet op het origineel. het rechterkanon is geknipt en geplakt en sluit niet goed aan, en de twee rechte tentakels lijken aanhangsels die totaal niet passen. Verder sluit het niet aan op het lichaam. Het kanon wat je weggehaald hebt vooraan heeb je ook slordig afgeknipt waardoor er nog een schouder zit. Ik neig ernaar dat je dit niet kan, dus wederom, wees eerljik"
- **Gemini r10 (11 nov):** `gemini/r10_rupsband.png` (Jordi, eigen Gemini-sessie). Jordi: "dit komt qua rupsbanden wat beter in de buurt, maar gemini krijgt de canontentakel niet meer terug. Deze kan jij wel nog toevoegen. Klopt het aantal tentakels dan? Want dan ben ik tevreden." en "dan moeten we nog wel wat met het formaat doen om te vertalen naar een sprite denk ik".
- Telling Claude: 1 kanon (linksboven), 1 krul achter de kop (verre kant, linksboven bij het oog), 2 rupsband-tentakels (voor), 2 tentakels naar rechts = 6. Formaat: 850×553 (1,54 : 1) → op 64 breed maar ±41 hoog.
- **Samenvoeging v1 (11 nov):** `samenvoeg/v1.png`: hele kanontentakel uit r5 incl. aansluiting (Jordi: "het enige wat je moet doen is 2 sprites samenvoegen. omcirkeld"; "de hele tentakel kopieren he, incl aansluiting"; "anders sluit die niet aan"), uitgeknipt via floodfill binnen de omlijning (`seg.py 110`), geschaald 1,24× en geplakt op r10 (`plak.py`). Formaat daarna via Gemini (Jordi: "ik ben bang dat jij het gaat verknallen").
