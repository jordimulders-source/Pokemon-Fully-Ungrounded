# Keuring blobfish fase 1, sprite r4 (onafhankelijke keurder, 16 nov)

Getoetst: alleen (1) trouw aan `model/model.png`, (2) Gen 3-techniek volgens SPRITE_KERN. Bekeken op 1×, 2×, 4×, 8× en 10× naast de modelmediaan per 4×4-blok (zelfde raster als `natief.png`), en naast Magikarp/Feebas/Corphish (Gen 3). Vel: `keuring.png`.

## Oordeel: FAIL, alleen op eis 2 (contrast van het lijf). Eis 1 (trouw) is PASS.

### Eis 1, trouw aan het model: PASS
- **Kleur en toon:** gemiddeld helderheidsverschil sprite − modelmediaan over alle lijfpixels (tint 4/6/7) = **+0,2**. De tinten volgen het model per blok (tint 4: model 72–78, tint 6: 77–92, tint 7: 82–101, tint 9: 92–118).
- **Glans:** witte vlek (16,34) (14–16,35) (14–15,36) (13,37) valt precies op de modelblokken met witte pixels (model 15/16 wit in (15,35), 11/16 in (14,36)). Zelfde plek, vorm en maat.
- **Lippen:** lichte bovenlip met glans linksboven, zwarte mondlijn (8,46)→(12–18,49)→ opkrul (19,48), onderlip, lipeind rond (lijnrood x21 y48–50, (19–20,47)). Komt overeen met het model; de opkrul maakt hem "derpy blij" zoals het model. Neus hangt niet: de kop loopt rond over in de bovenlip.
- **Ogen:** op de modelcellen (nabij 19–20/45–46, ver 9–10/41–42), opgebouwd zoals het model; zwarte pupil is een bekende keuze.
- **Vinnen en staart:** kopvin (13–17, 31–33), rugvin, borstvin (30–38, 40–54, lob onder de buik) en staart (46–56, 26–35) op de modelplekken met lichte stralen; minder stralen op de rugvin is wat 64 px kan tonen.
- **Kin/buikrand:** lichte rand onderaan (tint 7/9, bv. (24–25,52) model lum 106–115) staat in het model (doorschijnende winegum). Niet als fout tellen.
- Onderliplijn (13–19,51) is lijnrood waar het model zwart heeft (donkere mediaan (47–70, 0–24)); als binnenlijn in een donkere tint is dat volgens SPRITE_KERN juist goed. Geen reparatie.

### Eis 2, Gen 3-techniek
Goed: buitenlijn overal 1 px en gesloten; geen lichte kleur op de rand; zwart onder/rechts, selout linksboven; geen geïsoleerde zwart/selout-wissel op de rand gevonden (script); rand 53 % zwart (Corphish 49 %, model onder/rechts dik zwart: ok); licht linksboven; glans wit, klein; lip-/vintinten 112/133/168 met goede stappen.

Fout: **het lijf is één toon in drie tinten.** Tint 4/6/7 = helderheid **75 / 82 / 87** (stappen 7 en 5); SPRITE_KERN vraagt ±30–40 per tint (Magikarp-rood: 53 / 80 / 142 / 190). Daardoor zijn er feitelijk >3 tinten in de lijfkleur zonder dat ze iets tonen, en is er geen schaduwsikkel: op 1× naast Magikarp/Feebas is de vis een donkere, vlakke rode vorm (zie `keuring.png`). Het model zelf is zo vlak (onder tint 4 meet het model overal 72–78), dus de sprite is trouw; de oplossing gaat boven het model uit.

## Reparaties

### Nodig
1. **Lichtronde lijf (alleen met akkoord van Jordi, GEMINI.md: "Gen 3 boven het model voor licht en contrast ... vraag het Jordi").** Geen pixel verplaatsen, alleen tinten (recept muriqui r8): de facetten van het model houden (kop licht linksboven: tint 9 → 7 → 6 → 4 naar rechtsonder) maar de lijftinten op stappen van ±20–30 helderheid zetten, bv. 4 ≈ 70, 6+7 samen ≈ 95–100, 9 ≈ 120–125 (9 is ook de liptint: lippen meeschuiven zodat het verschil lip/lijf blijft), en een schaduwtint ±50–55 voor de onder-/achterkant (lijf onder de borstvin, staartsteel) als Jordi dat wil. Daarbij de losse tint-6-pixels in het tint-4-vlak samenvoegen, anders worden ze ruis zodra het contrast stijgt: (14,42) (16,44) (15,45) (32,43) (33,44) (26,48) (25,49) (39,29) (40,30) (39,31) (blauw op het vel; model daar 81–90, nu onzichtbaar, na de lichtronde een vlekje). De diagonale reeks (26,36) (25,37) (24,38) is de lichte ribbel van het model: laten staan. Toon Jordi A (huidig) / B (lichtronde) op 4× en 1×. Weigert Jordi: dan is r4 PASS (de rest klopt).

### Polijsten
2. **(17,32) zwart → lijnrood (index 2).** Eén zwarte pixel tussen selout op de lichte bovenrand (kopvin-achterrand). Model: donkere mediaan (76,24,23), dichter bij lijnrood (90,34,36) dan bij zwart (48,12,14); buren (16,31) meten ook lijnrood (94,35,39). Rood omkaderd op het vel.

Verder niets: lippen, mondlijn met opkrul, ogen, glans, vinnen en silhouet niet aanraken.
