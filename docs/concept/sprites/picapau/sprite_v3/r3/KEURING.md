# Keuring picapau sprite_v3 r3

Keurder: onafhankelijk, 19 nov. Getoetst op twee eisen: (1) trouw aan `gemini/r5_verbeter.png`, (2) Gen 3-techniek (SPRITE_KERN). Kleur (Picapau-palet, Pikachu-bruine vleugels, roodbruine staart) telt bewust niet.

Methode: model verkleind naar spriteschaal (15,4 modelpx per spritepx; bbox sprite x14–48 / y13–62 tegen model x307–839 / y56–829, verhouding klopt in beide richtingen), 8×-vel naast elkaar, kop op 12×, silhouet-overlay, per-pixel klassenkaart (model vs sprite), eilandjes- en open-randscript, sprite 1× naast Taillow, Pikipek, Starly en Pikachu.

## Oordeel: PASS (met 4 kleine pixelreparaties)

### Eis 1: trouw aan het model
Silhouetverschil met het model: 36 px alleen in de sprite en 27 px alleen in het model, bijna allemaal de buitenlijn van 1 px. Geen onderdeel toegevoegd, weggelaten of geherinterpreteerd. Gecontroleerd per onderdeel:
- **Kuif:** twee punten met zwarte toppen op de plek van het model (links x27–28 / y13–17, rechts x31–34 / y14–18). Klopt.
- **Rafelige achterkuif:** de punten rechts op y21 (tot x34) en y27 (tot x35/36) zitten op de plek van het model. Klopt.
- **Oog:** 4–5 px breed en 4 hoog, midden ±(26, 29,5). In het model is het midden (26,0, 30,0) met een straal van 2 px. Glans linksboven. Klopt.
- **Verre oog:** 2 px zwart op (16,28) en (17,28) boven de snavel. Binnen de grens.
- **Snavel:** een grijze kegel naar linksboven met de punt op (14,28). Bovenkant licht, onderkant donker, basis y28–34. Klopt.
- **Wang:** rond, x24–29 / y33–37. In het model x23,6–29 / y32,8–38,2. Klopt.
- **Verre wang:** rood op de linkerrand, (16,34–35). In het model x15–16 / y33–35. Klopt (zie ook punt 4).
- **Buik:** ronde vorm met de lichte vlek linksboven (x18–22 / y41–46) en een lichtere plek onderaan (x29–31 / y52–53), net als in het model.
- **Vleugel:** vorm, bovenboog en punt (x43–44 / y51–52) zoals in het model. De 4 stippen zitten op de modelplekken (33,37), (37,37), (34,42) en (38,41).
- **Verre vleugel:** een smalle donkere strook links achter het lijf, x16–18 / y38–47. Klopt.
- **Staart:** komt onder de vleugel uit (y53), loopt diagonaal en heeft de punt op (47,62). Ook de donkere veerlijn in de lengte komt uit het model. Klopt.
- **Poten:** de nabije poot (x24–25, tenen x21–27 op y58) klopt. De verre poot zit 1 rij te laag (zie punt 3).

### Eis 2: Gen 3-techniek
- Tinten: geel 3 (+ stippenwit), staart 3, bruin 2, rood 2, grijs 2. Binnen de norm. Stappen in het geel ±30–40 helderheid, zoals bij Taillow.
- Licht komt van linksboven en de schaduw volgt de vorm als een sikkel. Geen banding, geen pillow shading.
- Selout: donkerbruin aan de lichte kant (kop linksboven), zwart aan de schaduwkant. Ze wisselen elkaar niet af op één rand.
- De losse pixels zijn allemaal selout, kuif- of snavelovergangen of de veerlijn in de staart, dus geen ruis. Alleen de staartpunt heeft een losse lichte pixel (punt 4).
- Op 1× leest de sprite naast Taillow, Pikipek, Starly en Pikachu als een nette Gen 3-vogel.
- Fouten: 3 open randen (punten 1, 2 en 4). Lichte kleur op de buitenrand mag niet.

## Reparaties (op volgorde van belang)
1. **Verre poot, open linkerrand:** maak (28,56) en (28,57) buitenlijn (1 of 11). Nu staat lichtgrijs (29,56–57) direct tegen de achtergrond. Het model toont op x28, y56–57 een donkere lijn links van de verre poot.
2. **Achterkuif, open rand op de onderste punt:** maak (35,27) buitenlijn (1). Nu is dat geel (idx 4) met lucht erboven. Het model toont daar de donkere rand van de punt ('b' op x35, y27).
3. **Verre poot 1 rij te laag:** in het model liggen de tenen van de verre poot op y58–59 (onderrand y59,8), even hoog als de nabije poot. In de sprite loopt de verre voet door tot y60: de rij x26–31 op y60 is buitenlijn en die op y59 grijs. Schuif de tenen van de verre voet (x26–31, y59–60) 1 rij omhoog, zodat de onderste buitenlijn op y59 ligt, zoals in het model.
4. **Staartpunt:** (46,61) is lichtoranje (idx 7) met lucht eronder, dus een open rand. Maak (46,61) de schaduwtint (9) of zet buitenlijn op (46,62). Het model toont daar een donkere punt ('kok' op x46–48, y62). Kijk daarbij of de losse lichte pixel (45,60) weg kan (idx 9 of 8), zodat de punt geen ruispixel meer heeft.

Na deze reparaties hoeft er geen nieuwe vormkeuring te komen. Een diff die laat zien dat alleen deze pixels veranderden, is genoeg.
