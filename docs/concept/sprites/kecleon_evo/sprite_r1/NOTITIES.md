# Kecleon-evolutie, sprite r1 (maker-agent, 22 nov)

## Werkwijze
1. **Verkleinen zonder hertekenen** (`klassen.py`, `schrap.py`): figuur uit `combi_kop.png` (bbox 78×78) → 63×63 door 15 rijen en 15 kolommen te schrappen (Gengas/Mightyena-methode, lijnpixels wegen 10×, oog/kaakrijen 14–24 en oogkolommen 12–25 nooit geschrapt). Geschrapte rijen: 4, 8, 12, 25, 28, 31, 34, 40, 43, 47, 55, 58, 66, 69, 74; kolommen: 1, 7, 11, 26, 29, 32, 35, 40, 45, 48, 56, 61, 66, 69, 73 (in figuurcoördinaten). Resultaat: `model_verkleind63.png`. In de 64×64 staat de figuur op x 0–62, y 1–63 (voeten op de onderrand).
2. **Silhouet bevroren**: `bouw.py` controleert bij elke bouw dat de opake pixels exact gelijk zijn aan het verkleinde model (0 afwijkingen). Kleurfamilies per pixel uit `model_v1.png` alleen als kaart (`klassen63.npy`: o/g/p/#).
3. **Inkleuren met de hand**: `rijen.txt` is het handgeschreven raster (rij, startkolom, tekens); latere reparaties als `patch1–4.txt` via `zet.py`. Geen kleur op lichtheid berekend.
4. Controles: `controle.py` (kleuren, losse pixels, vlakjes < 3 px), `vel.py`, `raster.py`/`dump.py` alleen om te kijken.

## Palet (15 gebruikt incl. transparant; slot 15 ongebruikt)
- Lijn: k (41,24,41) buitenlijn schaduwzijde, pupil · r (140,49,57) selout op oranje, binnenlijnen oranje, mondlijn · E (156,90,41) selout/binnenlijnen op geel.
- Geel: A (255,247,189) · B (255,222,106) · C (238,180,65) · D (205,128,57). Tint 53° → 29° (schaduw naar oranje/bruin).
- Oranje: F (255,164,82) · G (238,112,57) · H (197,71,49) (+ r). Tint 28° → 9° → 355° (schaduw naar rood/bordeaux); hooglicht op oranje = B (geel).
- Roze (kaak): p (255,189,197) · q (238,130,150) · s (180,72,100).
- w wit (glans in de pupil).
- Helderheidsstappen ±35–45 per tint.

## Wat niet (letterlijk) uit het model komt, en waarom
- **Alle kleur** (mag afwijken; Jordi): indeling volgens v1-kaart, schaduw/licht van linksboven met de hand.
- **Kegeloog**: groene schijf → licht crème (A/B) zodat de pupil leest op een geheel geel hoofd; rand B/A met schaduwzijde C, schijfrand E/D. Pupil + glans 1-op-1 uit het model (glans midden in de pupil, omringd door pupilpixels; niet verplaatst).
- **Kam**: groen → C/D, de gele richels van het model → B/A, de diagonale modellijn (14,3)→(10,8) als E gehouden. Twee oranje spikkels in de kam (model r2) → geel, anders losse pixels.
- **Lijn rond de oogkegel links** (x8, rij 10–14, D): toegevoegd omdat kam/voorhoofd en kegel in het model alleen door groen/geel verschilden.
- **Roze vlekje bij de kaakhoek** (x20–22, rij 20–23, v1 'p') → oranje/H (schaduw onder de kop); roze alleen aan de onderkaak (x6–15, rij 24–25).
- **Spiraal van de krulstaart**: het verkleinde model had alleen brokken lijn; opnieuw als één doorlopende 1 px-lijn (E) gelegd over de modellijnstukken: (50,43)→(51–54,44)→(55,43)→(58,40–37)→(55–53,34)→(51,36–38)→(52,39)→(53–54,40)→(55,39–37)→(54,36). Per winding licht bovenaan (B) en donker onder de lijn (C/D).
- **Klauwen geel** (indeling): de klauwen van beide handen waren in v1 oranje; nu geel met E-lijnen ertussen.
- **Armlijnen**: voorkant onderarm r (lichtzijde) op rij 32–38; achterkant/elleboog k (schaduwzijde) waar het model zwart had.
- **Lijn dij/scheen** (rij 53, x32–36, r): vorm over vorm, niet in het model.
- Modellijnen: 260 van de 264 lijnpixels uit het verkleinde model zijn donker gebleven (k/r/E); 4 zijn vlak geworden: (57,35) en (51,43) door de schone spiraallijn, (22,39) en (18,41) in de hand.

## Zelfgenoemde zwakke punten (na eigen reparaties)
- Gerepareerd: rommelige nek/achterhoofd (veel 1 px-tinten) → opgeschoond (patch2); dijlicht was een verticale streep → ronde vlek met H-sikkel rechts en onder (patch1); buik onderaan vlak → licht linksboven, D rechtsonder (patch1); losse vulpixels (patch3–4); romp rechts was vlak G → lichtvlek bovenaan, via G naar H rechts/onder (patch5).
- Resterende "losse pixels" uit `controle.py` zijn bewust: puntjes van kam- en rugstekels (1 px kern), klauwtips, de glans in de pupil, lijnpixels.
- Twijfel: de kam is grotendeels C met B-richels; misschien te weinig verschil tussen kam en oogkegel op 1×. De rugstekels zijn op deze maat 2–3 px en lezen als kartels, zoals in het model.
- Twijfel: romp en dij zijn nu licht linksboven → H rechts, maar het oranje blijft een groot vlak; een keurder moet zeggen of het nog "effen" leest (vraag eerst naar volume).
