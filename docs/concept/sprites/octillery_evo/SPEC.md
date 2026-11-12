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
- Jordi over samenvoeging v1: "juist, dat is m" → bevroren ontwerp: `referenties/ontwerp_gekozen.png`. Volgende stap: formaat via Gemini (prompt in `gemini/PROMPT.md`, "Formaat").
- **Gemini r11 (11 nov):** `gemini/r11_afgewerkt.png` (prompt "Bijsnijden + netjes afwerken"). Jordi: "hier komt ie mee". Claude: 880×619 (1,42 : 1, was 1,54), aansluiting kanon netter; rupsband-tentakels onderaan grotendeels weg (alleen linkerkrul zichtbaar, rest een donkere massa).
- **Gemini r12 (11 nov):** `gemini/r12_compacter.png` (prompt "Compacter"). Jordi: "en dit formaat?". Claude: 818×619 (1,32 : 1) → 64×48; onderste kanon is een opgerolde tentakel geworden (geen monding meer), dus weer maar 1 kanon.
- Jordi over r12 (11 nov): "alleen het gat moeten we invullen, wat me wel zorgen baart is dat de rupsbanden nu totaal niet meer goed zitten. Ook dit werkt dus niet".

## Analyse anatomie (Claude, 11 nov; Jordi: "analyseer even of het fysiologisch/biologisch/geometrisch klopt")
- Klopt: ogen aan de zijkant, pijlvormige mantel met vinnen aan de punt (Humboldt), nabij kanon groter dan het verre (perspectief), monding van beide kanonnen naar links, licht linksboven.
- Klopt niet: (1) bij een inktvis komen alle armen uit één krans rond de mond; hier begint de krul linksboven áchter/boven het verre oog (uit de kruin) en lijkt het onderste kanon uit de wang onder het nabije oog te komen (de lus loopt over het gezicht). (2) Aantal: 2 kanonnen + krul linksboven + 2 rupsbanden (de nabije grotendeels onder het kanon) + 2 rechts = 7 ledematen i.p.v. 6; de krul linksboven is over. (3) Rechte snijnaad boven de loop van het onderste kanon (links, bij de wratten van de rupsband). (4) Echte inktvissen hebben de sifon onder de kop, niet de mond als buis; dat is Octillery-erfgoed en mag (Pokémon-vrijheid).
- Beweging (voorstel, nog niet besloten): echte octopussen (Abdopus aculeatus, Amphioctopus marginatus; Huffard 2005) "lopen" op twee armen door ze over de grond af te rollen als een loopband; de arm draait niet, er loopt een golf van samentrekking doorheen (peristaltiek, zoals bij een rups of slakkenvoet). Zuignappen hechten achteraan, voorkant komt los, schuift naar voren, hecht weer. Zuignappen als anker tegen de terugslag van de kanonnen (zoals de spaden van een veldkanon).
- Jordi (11 nov): "ja die kanontentakel moet idd lager zitten, is dat te fixen? Die erachter is niet aantoonbaar hoog. Ik tel 8 tentakels, drie erachter. Zitten de zuignappen bij alle tentakels aan de goede kant?"
- Telling klopt: 8 (2 kanonnen, krul achter de kop, 2 rupsbanden, 3 rechts). Het geplakte r5-stuk bevat ook de r5-kin; daardoor lijkt het kanon uit de wang te komen. Poging lager (`samenvoeg/plak2.py`, `v2.png`): zonder de lus eindigt de steel met een rechte snede vóór de kin; aansluiten vergt hertekenen → niet gelukt.
- Zuignappen: echte inktvisarmen hebben ze aan de binnenkant (mondkant, holle kant bij een krul). Goed: de 2 rechts (onder/binnenkant van de boog). Verkeerd: de krul achter de kop (wratten aan de bolle buitenkant). Rupsbanden: voor lopen moeten ze naar de grond (buitenkant van de lus onderaan); de linker heeft ze aan de bovenkant. Kanonnen: geen zuignappen zichtbaar (gestileerd).
- Jordi (11 nov) over v2: "dit moet nog iets beter aansluiten, klein beetje hoger, dan kunnen we het daarna met een sprite wel fixen denk ik" → v3: stuk 30 px hoger (`plak2.py 560 376 575 -30`), `samenvoeg/v3.png`.
- Jordi (11 nov): "alle zuignappen lijken aan de buitenkant te zitten, dus dat is prima, de kleinste tentakel lijkt alleen geen zuignappen te hebben, daar moet wel nog iets komen" → toegestane toevoeging in de sprite: zuignappen (gele wratten, zelfde stijl) op de kleinste tentakel (Claude vermoedt: de donkere boog rechts achter, tussen oog en de rechter tentakels; navragen).
- Jordi (11 nov), met `samenvoeg/jordi_zuignappen_weg.png`: "deze zitten wel verkeerd en mogen weg, maar dat kan tijdens het spriten wel. En ja ik bedoel die donkere boog rechts. Ik denk dat dit wel moet lukken" → model = v3 (`referenties/ontwerp_gekozen.png`).

## Toegestane afwijkingen in de sprite (definitief)
1. Zuignappen (gele wratten, zelfde stijl) op de donkere boog rechts.
2. De omcirkelde wratten onder de kin (op de tentakel onder het onderste kanon) weg.
3. Naden van het plakken wegwerken: rechte lijn boven de loop van het onderste kanon, harde overgang waar de steel achter de kin verdwijnt.
- Jordi (12 nov) over `af/` (r5): "hoe komt deze door de keuring heen?" · "er gaat echt zoveel fout dat het niet eens zin heeft om het allemaal te benoemen" → afgekeurd; `af/` is géén eindresultaat.
- Jordi (12 nov): "ik vind echt letterlijk geen enkel onderdeel goed gelukt".
- Jordi over `samenvoeg/r16_kort.png` (12 nov): "ook niet mooi he".
