# Vaste opdracht voor elke sprite-agent (ook bij kleine reparaties)

Claude plakt de verwijzing naar dit bestand in **elke** sprite-opdracht, hoe klein ook. Jordi (23 okt): "ik moet elke keer dingen opnieuw vertellen waarvan ik dacht dat ik je erop getraind had." Dit bestand is daar het antwoord op.

## 1. Eerst lezen (altijd)
- **Kort: `docs/lessen/SPRITE_NORM.md` (één pagina) is de norm die elke agent leest**; de lijst hieronder is achtergrond voor wie twijfelt (tokens sparen, Jordi 24 okt).
- Dit bestand helemaal.
- **`docs/lessen/FAKEMON_CHECKLIST.md`** (vormen, poses, verhoudingen; uit de studie van alle 1024 sprites): elk punt afvinken. Achtergrond in `docs/lessen/vormstudie/STUDIE.md`.
- `docs/lessen/SPRITING.md` §0 (checklist) en §1–§8 (de regels uit de Dragonfly Cave-gids), plus de sectie(s) over deze Pokémon.
- `docs/lessen/FAKEMON_DESIGN.md` (vaste werkwijze bovenaan).
- Gericht in `docs/lessen/bronnen/dragonflycave_spriting_guide.txt` het onderdeel waar je aan werkt (omlijning, ogen, shading, perspectief).
- De NOTITIES.md van de vorige ronde van deze Pokémon en `docs/concept/sprites/FEEDBACK.md`.
- **`SPEC.md` in de map van deze Pokémon** (specificatie per onderdeel: referentie, bevroren/open, Jordi's woorden) en **`docs/lessen/RETRO_OLINGUITO.md`** (waarom 23 rondes; wat nu anders gaat).
- **De map `referenties/` van deze Pokémon** (foto's van het echte dier, skelet-sprites, kenmerk-sprites): gebruik ze als onderlaag en maatstaf; een referentie die Jordi aanwijst is de specificatie.
- **`AFGEKEURD.md` in de map van deze Pokémon** (als die bestaat): wijzigingen die Jordi al heeft afgekeurd. Nooit herhalen. Claude houdt dit bestand per Pokémon bij na elke afkeuring.

## 2. Jordi's vaste feedback (nooit opnieuw laten zeggen)
**Vorm en pose**
- Lijf én blik diagonaal 3/4 naar links-voor; nooit zuiver profiel of recht vooruit. Bijna frontaal mag alleen met perspectief (verre arm kleiner, niet recht op de billen).
- Snuitdieren: vaak maar **één oog** in beeld; het verre oog verdwijnt achter de neusbrug (Poochyena, Cyndaquil, Rhyhorn). De **snuit is één vorm** die in de 3/4-richting wijst, met de neus aan het eind.
- Alle ledematen, oren en ogen tellen; alles verbonden; geen geamputeerde verre kant; geen poten die aan elkaar vastzitten (minstens 1 kolom lucht of een omlijning).
- **Viervoeters lopen diagonaal, nooit in telgang** (kameel): de poten die tegelijk vóór staan zijn diagonale paren (nabije voor + verre achter). Check dit tegen de referentie (Jordi, olinguito 21b). **Uitzondering:** kameelachtigen (alpaca, lama, kameel) lopen echt in telgang; bij de alpaca bewust zo gehouden (Jordi, 24 okt).
- Pose niet stijf: poten niet kaarsrecht naast elkaar en niet identiek; één consistente houding (staan óf lopen); geen Escher-constructies.
- Lijf natuurlijk: teken het over een **echte Gen 3-sprite als skelet**, nooit uit ovalen/bonen; overgangen geleidelijk (Mightyena), geen rechthoekige romp of doos-kop.
- Formaat vergelijken met echte sprites van dezelfde fase (fase 1 ±800–950 px). Kop niet te groot.
- Kenmerken moeten op 1× lezen (een haakje van 3 px leest niet).

**Lijnen, ogen, kleur**
- Geen rechte lijnen waar het dier rond is; curven zonder hoeken; geen overdreven rechte staart.
- Ogen geïntegreerd (bovenlid donkerst, iris donker boven/licht onder, glans), niet opgeplakt, geen brilogen; geen volledig zwarte ogen zonder glans.
- Omlijning per kleurgroep, zwart alleen aan de schaduwkant; licht van linksboven; geen open randen (ook schaduwkleur naast transparant).
- Kleuren vergelijken met Pokémon van **hetzelfde type** (Dark mag donker).
- Verzonnen kleurvlakken mogen alleen als ze werken; bij twijfel één vachtkleur.
- Referentiefoto = inspiratie, geen blauwdruk (Pokémon-filosofie), maar de soort moet herkenbaar blijven.

**Werkwijze**
- **Wat Jordi goedkeurde blijft letterlijk staan** (pixel voor pixel). "Meer Pokémon" of "beter" nooit uitvoeren door goedgekeurde verhoudingen te veranderen.
- **Een kleine correctie is klein:** werk binnen het pixelbudget dat Claude opgeeft; tel en meld het aantal gewijzigde pixels. Verplaats je een onderdeel, laat dan de vorm eromheen meekloppen (neus verschuiven = snuit mee).
- Grote of ongevraagde wijzigingen alleen als variant naast het origineel.
- Met de hand tekenen (pixel-over/tekst-raster), geen automatische vormen of shading in het eindresultaat.

## 3. Vóór opleveren
- **Harde regel – geen nepfixes (Jordi):** een reparatie die het gezicht of het geheel in een gedrocht verandert, is geen klein foutje maar onacceptabel. Zet het resultaat op 1× en 3× **naast de laatst goedgekeurde versie**: oogt het gezicht vreemder, minder schattig of minder als dezelfde Pokémon, dan lever je het **niet** op. Ga terug naar de goedgekeurde versie en los het kleiner op, of meld eerlijk dat het niet lukt.
- Loop §0 en de lijst hierboven punt voor punt na in NOTITIES.md (ok / wat je deed).
- **Bekijk je resultaat zelf op 1× en 3× naast 2–3 echte sprites** en schrijf eerlijk op wat nog niet klopt.
- Lessen onder "Lessen" in je NOTITIES.md (Claude zet ze over); niet in SPRITING.md schrijven, niet committen tenzij gevraagd.

## 4. Claude (coördinator)
- **Tokens sparen:** agents krijgen SPRITE_NORM.md + SPEC/AFGEKEURD (niet alle lessenbestanden); één maker per sprite die met SendMessage doorwerkt; geen parallelle experimenten tenzij Jordi vraagt; kleine vellen.
- Plak de verwijzing naar dit bestand in elke sprite-opdracht en geef bij reparaties een pixelbudget en de lijst bevroren delen mee.
- **Bekijk elk resultaat zelf** (1× en 3×, naast de laatst goedgekeurde versie) vóór het naar Jordi gaat. Een gezicht of geheel dat slechter oogt dan de vorige goedgekeurde versie gaat **nooit** naar Jordi: terugsturen of de vorige versie houden.
- **Bevroren delen hard controleren met een pixeldiff** (niet op het oog): geef de agent de bevroren zones als rechthoeken/maskers en laat hem bewijzen dat die 0 pixels verschillen met de goedgekeurde versie. Een herschaling van de kop is géén reparatie: dan blijven oren, masker, oog en snuit niet behouden (olinguito ronde 19: oren veranderd, snuit misvormd, door Claude ten onrechte doorgelaten).
- **Elk zelfgenoemd zwak punt = automatisch fail** (Jordi, 24 okt: "waarom gebeurt dit elke keer weer opnieuw"): wat een maker of keurder zelf "zwak", "twijfel", "leest eerder als…" of "Jordi kan zeggen dat…" noemt, gaat terug naar de maker en nooit naar Jordi. Toets of iets op 1× **leest**, niet of het technisch in de pixels staat (olinguito finale: verre achterpoot "staat er" maar leest als schaduw).
- **Een formaat- of pixelgrens mag nooit winnen van de vorm:** meldt een agent "dunner/rechter gemaakt om onder X px te blijven", dan is dat een afkeuring, niet een kanttekening (olinguito 22: Claude liet een 5 px rechte poot door).
- Twijfel Claude bij de eigen check, dan de vorige goedgekeurde versie houden en eerst de oorzaak vinden; geen nieuwe ronde op gevoel.
- **Jordi's woorden letterlijk doorgeven** (citaat), niet parafraseren of inkorten tot een eigen lijstje. Een nieuwe instructie of referentie is een **aanvulling** op de vorige, geen vervanging: alle eerdere, nog openstaande punten gaan mee. Geeft Jordi een referentie-sprite die "volledig voldoet", dan is die referentie de specificatie: de agent neemt alles over wat hij laat zien (ook dingen die Claude niet heeft opgesomd, zoals de positie van het oog) en meet het na (olinguito stap 1: de oogpositie viel weg omdat Claude Linoone samenvatte tot drie punten).
- Nieuwe terugkerende feedback van Jordi meteen in §2 hierboven zetten.
