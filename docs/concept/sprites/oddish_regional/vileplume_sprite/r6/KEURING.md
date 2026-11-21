# Keuring r6 (onafhankelijke keurder, 20 nov)

Getoetst: (1) trouw aan `referenties/gemini_gekozen_vileplume.png`, (2) Gen 3-eisen. Toegestane afwijkingen (a) geklonterde tentakels, (b) gelaat afwerken, (c) linkerpoot schuiner tellen niet als fout.
Bekeken: 1× naast het model (model-bbox verkleind tot de sprite-bbox 57×62), 8× naast elkaar, 12× per onderdeel (krater, toppen T/L/R, gelaat A/B/C, poten). Gemeten: kleine kleurclusters (<3 px) en de modelomtrek op 64 px.

## Oordeel: FAIL

Op 1× leest hij als het model (vijf anemonen, krater, wit lijf, lange benen), maar Jordi's twee hoofdpunten zijn niet opgelost: de anemonen zijn niet netjes en de definitie is laag. Op 8× leest het als ruis/streepjescode, niet als tentakels.

## Reparaties (belangrijkste eerst)

1. **Tentakeltoppen van de achterste anemonen = streepjescode.** T (x27–40, y1–4), R (x40–59, y3–9) en L (x4–22, y4–10) bestaan uit kolommen van 1 px licht | 1 px zwart/R0 om en om (rij 2: `033K3K3K3K033K`; rij 4–6 bij R: `0..0.03K.03K`), allemaal recht omhoog, met losse doppen (31,1) (33,1) (35,1) en gaatjes als (43,6). In het model zijn het ±2 px brede, afgeronde vingers die **waaiervormig** uit elkaar staan (L leunt naar links, R naar rechts), licht in het midden, donkerder aan de randen, zonder zwart tussen elke pixel. **Neem vorm, breedte (2 px) en richting van elke vinger over uit het model** (binnen de toegestane klontering, ±8–10 per anemoon), met de omlijning alleen om de vinger heen.
2. **Voorste anemonen VL (x14–36, y15–28) en VR (x36–53, y13–27): het stralenpatroon valt uiteen in korte horizontale streepjes.** 26 losse 1–2 px-clusters in rood (idx 3) en 20 in licht (idx 5), o.a. (35,20) (40,20) (45,20) (22,22) (26,22) (14,21) (39,24) (40,25) (33,25). In het model loopt elke tentakel als één doorlopende straal van het mondje naar de rand (ster rond het mondje). **Neem per tentakel de doorlopende straal over uit het model** (vanaf de mondring tot de rand, geen onderbrekingen), zodat er geen vlakjes < 3 px overblijven.
3. **Krater (x25–39, y10–17) is een pil/rechthoek, niet rond.** Bovenrand recht over x27–35 (y10), onderrand recht over x28–35 (y17), het oranje bad is een rechthoek (x27–35, y13–14) met horizontale tintbanden (rij 11 grijs, 12 oranje, 13–14 geel, 15 bruin). In het model is de rand een ovaal met gebogen boven- en onderlip en is het bad lensvormig (spitse uiteinden links/rechts, geel alleen in het midden). **Neem de ovale rand en de lensvorm van het bad over uit het model**; de donkere keel eronder (y17–20) is goed.
4. **Gelaat: kies A (= model).** In B (standaard) en C hangen de ogen (25,32–33) en (29,32–33) direct aan de zwarte onderrand van de kroon (x22–29, y31); ze lezen als tandjes/inkepingen van de lijn, niet als ogen. In A staan ogen en U-mond los van de rand met een lichte rij ertussen, zoals in het model, en zijn ze goed te zien. Wil men B houden: **neem de lichte rij tussen rand en ogen over uit het model** (ogen 1 px lager, los van y31).
5. **Kleur/volume van de kroon (secundair, kleur mag afwijken):** licht oranje (idx 5, 422 px) is de grootste kroontint en ligt gelijkmatig over alle vijf, ook rechtsonder (VR, R). Het model is roder met licht vooral op de tentakelkoppen linksboven. Na punt 1–2 nagaan dat elke kroon licht linksboven en een schaduwsikkel rechtsonder heeft, niet alleen een donkere voet.
6. **Voeten:** linkervoet (21–23, y59) eindigt in `aKK`, rechtervoet (38–40, y59–62) in een zwart blokje `KK` op y62; in het model lopen beide benen licht uit met een donkere punt van 1 px. **Neem het einde van beide benen over uit het model.** Klein punt.

## Wat goed is
- Silhouet en verhoudingen kloppen op 1× met het model: vijf anemonen op de modelplekken, krater bovenmidden, wit lijf met twee armpjes, lange dunne benen.
- Donkere rand tussen de anemonen (toegestaan a) is consequent en scheidt de vijf kronen duidelijk.
- Linkerpoot staat schuiner (x25→21 over y44–59) met een gelijkmatige trap, zoals gevraagd (c); rechterpoot ongewijzigd.
- Lijf en armen: nette selout, licht linksboven, schaduw rechts, 3 tinten; arm-oksels netjes.
- Mondjes van de vijf anemonen staan op de modelplekken.
- Techniek: 16 paletkleuren incl. transparant, geen lichte kleur op de buitenrand, zwarte lijn aan de schaduwkant.
