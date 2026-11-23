# Regionale Pincurchin (Galápagos; naam: regional form, blijft Pincurchin?)

Lijn: Pincurchin (repo: puur Electric) → regionale vorm. Pincurchin weer in de dex (Jordi, 9 nov).

## Jordi letterlijk
- (eerder) "Pincurchin-vorm: pencil-spined sea urchin" · "ziet er erg sinister uit en Pincurchin is een saaie pokemon"
- 23 nov: "de regionale pincurchin gaan we maken"
- 23 nov, type: "poison/rock"
- 23 nov, welke pencil urchin: "maakt niet uit, hij wordt hybride, lijkend op een soort onderwater mijn"
- 23 nov, gezicht: "Pincurchins gezicht" (ogen en tanden van Pincurchin overnemen)

## Besloten
- Type: Poison/Rock.
- Ontwerp: hybride pencil urchin + onderwatermijn (zeemijn).
- Gezicht: dat van Pincurchin.

## Open
- Kleuren, pose, grootte, naam, evolutiemethode (wordt een gewone Pincurchin er een via een plek?).

## Rondes
- Gemini-startprompt v1: `gemini/PROMPT.md` (bijlage `gemini/bijlage_pincurchin.png` = Pincurchins sprite uit de repo, 8×, voor het gezicht).

## Gemini v1 (`r1/gemini_v1.png`, 23 nov)
- Jordi: "de stekels moeten groter, ik dacht aan bruin voor de binnenkant en donkerrood voor de stekels, geen roest"
- → prompt v2 (`gemini/PROMPT.md`), nieuw gesprek, alleen de Pincurchin-bijlage.

## Gemini v2 (`r2/gemini_v2.png`, 23 nov)
- Jordi: "de ogen zijn anders maar dat is niet erg, ik vind hem verder te kaal"
- Jordi: "en het rood mag wat feller" · "wel donker"
- Wat "te kaal" inhoudt is niet gespecificeerd; in prompt v3 letterlijk doorgegeven ("too bare"), zonder eigen invulling.
- Uitleg "te kaal" (Jordi): "de stekels bedekken niet genoeg van het lijf, te kort, niet genoeg, misschien wel allebei" → prompt v4 (vervangt v3).

## Gemini v4 (`r4/gemini_v4.png`, 23 nov)
- Jordi: "beter, maar het steen heeft teveel detail" → bijstuurzin in hetzelfde Gemini-gesprek (één wijziging), zie PROMPT.md.
- Jordi (na v4): "hij lijkt ook steeds minder op pincurchin"
- Jordi kiest wat er van Pincurchin terug moet: "Gezicht exact" (ogen en tanden 1-op-1 zoals Pincurchin). → startprompt v5, nieuw gesprek (vervangt de bijstuurzin).

## Gemini v5 (`r5/gemini_v5.png`, 23 nov)
- Jordi stuurt v5 naast een foto van een pencil urchin (`referenties/foto_pencil_urchin_jordi.jpg`): "behoorlijk verschil nog wel"
- Jordi: "dunner, langer en dichtheid, maar het gezicht mag daarvan utigezonderd zijn" (stekels dunner, langer, dichter; het gezicht blijft vrij) → startprompt v6.

## Gemini v6 (`r6/gemini_v6.png`, 23 nov)
- Jordi: "hij lijkt nog steeds niet, veel te stekelig"
- Uitleg (keuze Jordi): "Vorm: gladde staafjes" (gladde potloodstaafjes met een stomp eind zoals op de foto, geen gekartelde punten) → startprompt v7.

## Gemini v7 (`r7/gemini_v7.png`, 23 nov)
- Jordi: "ok veel beter, en hoe maken we hier nu een semi onderwater mijn nog van (ogen en mond kloppen niet maar die fixen we zelf)"
- Ogen en mond: in de sprite zelf Pincurchins gezicht overnemen (niet meer via Gemini).
- Op de vraag welke mijnkenmerken: "lastig te zeggen, bedenk maar een prompt". Voorstel Claude in bijstuurprompt v7 → v8: korte contacthoorns met bol kapje tussen de staafjes + naad om het midden (ring bovenop als reserve).

## Gemini v8 (`r8/gemini_v8.png`, 23 nov) = kandidaat-model
- Jordi: "ok prima, alleen we behouden slechts 3 van die spikes"
- v8 heeft 4 mijnhoorns: links, midden en rechts op het lijf, plus een klein knobbeltje bovenop tussen twee staafjes. Voorstel Claude (wacht op Jordi): het knobbeltje bovenop gaat weg, de andere 3 blijven. Weghalen in de sprite, niet via Gemini.
- Jordi: "de mond hier gaat weg en de ogen vervangen we"
- Besloten (Jordi): hoorns links, midden en rechts blijven (knobbeltje bovenop weg); ogen = Pincurchins ogen.
- Mond, Jordi: "het enige wat ik nog niet zeker weet is of we de mond helemaal weglaten of dat we die erop zetten dat de lijn eroverheen loopt. misschien beide proberen" → twee varianten: A zonder mond, B Pincurchins mond met de naad eroverheen.

## Model (bevroren)
`r8/gemini_v8.png`, met bovengenoemde uitzonderingen (knobbeltje bovenop weg, gezicht van Pincurchin). Verder niets hertekenen.

## Sprite (23 nov)
- r1 (maker) → keuring BIJNA (lijnen staafjes, naadgat, vlekjes, onderrand) → r2 met reparaties 1–5 (`sprite/r2/`, A en B). Naar Jordi: `pincurchin_regional_r2_AB_8x.png`. Open: loopt alleen de bovenste naadlijn over de mond in B of de hele naad (keurder: tweede lijn wist de onderlip).
- Jordi (r2, met 3D-render Pincurchin `referenties/pincurchin_3d_jordi.png`): "ah klopt ja, het zijn driehoekjes, dus datd is niet anders te vertalen denk ik. Misschien de mond iets groter en dat de mond de lijn overlapt ipv andersom" → ogen blijven; B: mond iets groter (Pincurchins mond geschaald, niet hertekend) en de mond ligt over de naad.
- Jordi (naast Pincurchin): "ja de mond mag wat groter, het rechteroog wat lager en het linkeroog moet iets meer vanuit een hoek, heeft het model dat ook?" · "en dan de mond overlapt d elijnen"
- Model v8: ja. Het linkeroog is daar smaller dan hoog (ovaal, in perspectief); het rechteroog is rond en staat iets lager dan het linker. → r3: linkeroog smaller door een kolom van Pincurchins oog te schrappen (niet tekenen), rechteroog 1–2 px lager.
- r3 (`sprite/r3/vel2.png`): 4 varianten, linkeroog c4/c3 (andere kolom geschrapt) × mond 115/130%; rechteroog 1 px lager (model: 0,73 px). Keuze bij Jordi.
- Jordi: "de derde is het beste" (= B115_c3). "Alleen het linker oog klopt volgens mij nog net niet helemaal, maar dat is echt 1 of 2 pixels verschil denk ik? kijk eens goed vanuit de hoek en de belijning"
- Gemeten (Claude): het linkeroog (x13–16) staat met zijn ring óp de linkerlijfrand (x13, rij 40–42 geel waar de lijflijn hoort), dus de ring raakt direct het rode staafje; geen lijf/lijn ertussen. Model zegt x13,7–16,6, dus x14–17 is even trouw. → r4: oog 1 px naar rechts, lijfrand terug.
- r4 (`sprite/r4/vel.png`): linkeroog R1 (x14–17, mond ervoor) / R2 (x14–17, oog voor de mond) / R3 (x13–16, 3 breed). Model: ring overal gelijk, geen lijn, ±1 px lijfrand tussen ring en staafje. Voorstel Claude: R2.
- Jordi bij r4: "kijk nu eens naar het model". Claude ziet in het model (r8, close-up): (1) het linkeroog is een smal, staand ovaal (±4×6 natief → ±3×4–5 in de sprite) met één smalle pupil in het midden; (2) tussen linkeroog en mond zit lijf: de mond raakt het oog niet en begint lager (bovenkant mond ±halverwege het oog). In r4 is het oog 4 breed met een pupil van 2 en ligt de mond er direct tegenaan. → r5.
- Jordi: "behoud de pupil wel volleidg" (bij het smaller maken van het linkeroog blijft de hele pupil staan).
- r5 (`sprite/r5/vel.png`): V1 oog 4×5 mond +1/+2, V2 oog 4×6, V3 mond +1/+3. 3 breed kan niet met de hele pupil (pupil zelf 2 breed). Mond 115% blijft groter dan in het model en bedekt de naad.
