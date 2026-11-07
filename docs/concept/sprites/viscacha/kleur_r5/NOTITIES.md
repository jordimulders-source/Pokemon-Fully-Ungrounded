# Viscacha frontsprite, kleur ronde 5 (maker-agent)
Jordi (r4 afgekeurd): "kijk eens goed naar het gezicht, linkerkant, neus, whiskers, mond etc klopt niet"; aanvulling: "het elektrische wangaanhangsel heb je ook niet nagemaakt, je hebt het niet goed gecontroleerd, je mag alleen met ogen afwijken".
Dus: alles zoals Gemini (`referenties/gemini_gekozen_ronde6.png`), alleen het luie oog uit r4 blijft. Handwerk op het r4-raster in `reparaties_r5.py` (zones a–j).

## Diff r4→r5 (206 px)
| zone | px | wat |
|---|---|---|
| a gele snuitpluk | 9 | Plukje met twee punten (1,26) en (1,28) op de voorkant van de kop vóór het oog (rij 25–28), zoals Gemini; niet meer op de snuitpunt. |
| b snuit/neus/mond | 10 | Ronde snuitbult (voorste punt x2, rij 29–31, daaronder terug naar x3–4). Neus 3 px donker, driehoekig (4–5,31) en (4,32), net binnen de snuitpunt zoals Gemini. Mond: tapse lijn 1→2 van de neus naar achteren (4–6,33). |
| c kin/keel | 14 | Crème kin onder de mond (5–7,34–36), kinlijn in 6 van (7,35) naar (10,36), daarachter de crème keel. |
| d snorharen nabije kant | 15 | 3 lijnen van 1 px in B, uitwaaierend naar linksonder vanaf de snuit (vlak, schuin, steil), zoals Dedenne ze tekent. Ze lopen tegen de framerand x0, Gemini's lijnen gaan verder. |
| e wangaanhangsel | 58 | Gemini-sikkel op ware grootte en plek: punt (21–24,26) ver buiten de kop, bolle kant links tot x14 (rij 31–32), inkeping rechts (18,32–33), onderpunt (20–21,35–36). Bolle kant licht (A) met gele selout (8), binnenkant 9 en zwart, en de terracotta schaduwkant (3) erachter op de nek (19–25, rij 28–34), zoals Gemini. |
| f snorharen verre kant | 6 | 2 lijnen in F schuin over de crème borst (11–16,37–39) en (13–16,40–42), zoals Gemini. |
| g rug | 19 | Vachtpiek terug zoals het Gemini-masker: (35–38,26) en (34–37,27); de boog uit r2/r3 vervalt, de rugcontour is weer het Gemini-masker. |
| h staart en voet | 21 | Terug naar het Gemini-masker: rechterrand staart (60,28) en (61,29), onderrand staartaanzet (50–56,47–48) en verre voet (22,58) en (29,58). |
| i nazorg | 1 | Lege rand (4,25) → 8; overige nazorgpixels (42,31), (22,33), (20–21,34) en (18–19,36) staan ook in deze zone, maar zijn eerder aan zone e/g toegeteld. |
| j lijf/buik | 53 | Buikvlek smaller zoals Gemini (crème vanaf x26, punt (28–30,41)); bil meer oker 4 en minder terracotta, 3 alleen 2–4 px langs de achter- en onderrand. |

**Silhouet t.o.v. r4** (41 px, zie `controle_uitvoer.txt`; nieuw bestand `silhouet/silhouet_r5.txt`):
- Erbij: pluk (3–4,25) en (1,26); vachtpiek (35–38,26) en (34–37,27); staart (60,28) en (61,29); snuit (2,31); snorharen (0–3, rij 32–39); staartaanzet (50–56,47–48); verre voet (22,58) en (29,58).
- Weg: (1,29) (snuitvorm); de r2/r3-boog (40,29), (42,30), (43–44,32) en (44,33).
- **T.o.v. het Gemini-masker** (`silhouet_auto`): ontbreekt alleen (1,29). Extra zijn de dunne delen uit het plaatje die het masker door de drempel kwijt was (pluimpunten, oorschelpen, pluk, snorharen), de dichte kinspleet (8–9,37) en de dichte spleet tussen de achterpoten (34,51) en (35,52).

## Afvinklijst tegen Gemini (onderdelenvel onderaan `vel.png`, sprite | Gemini64, 12×)
- [x] kop: vorm en tonen (licht zand, schaduw achter onder het oor).
- [x] oor ver: smal, binnentint rechts.
- [x] oor nabij: brede ronde schelp, donkere binnenkant.
- [~] oog: **bewust anders** (lui, zwaar lid, Drowzee-basis), toegestaan door Jordi.
- [x] neus: donker, 3 px, net binnen de snuitpunt.
- [x] mond: korte lijn onder de neus naar achteren.
- [~] snorharen: 3 links en 2 over de borst, zoals Gemini; de linker zijn korter, omdat het frame bij x0 ophoudt.
- [x] gele snuitpluk: vóór het oog op de voorhoofdrand, met twee punten.
- [x] wangaanhangsel: grootte, plek, vorm, inkeping en schaduwkant zoals Gemini.
- [x] borst: crème, kin en keel.
- [x] voorpoten: ver opgeheven, nabij met pols en poot.
- [x] lijf: licht, vachtpiek op de rug, oker schaduw op de bil.
- [x] buik: smalle crème vlek met donkere crème onderaan.
- [x] achterpoten: terracotta, perspectief als Gemini.
- [x] staart: tweekleurig bruin/oker, vorm als het Gemini-masker.
- [~] pluim: gekarteld geel met drie punten; Gemini's vlammen zijn iets slanker en hoger.

## Controle (`controle_uitvoer.txt`)
- Open randen 0.
- Losse pixels: alleen de steile snorhaar (diagonale 1-px-lijn, zoals bij Dedenne).
- Clusters < 3 px: alleen het oog en de gele kern (57,12).
- 16 kleuren incl. transparant; png = raster.
- Vel: `vel.png` (keurvel: werk naast gemini64, foto1-kop, Dedenne (snorharen) en Drowzee (oog), close-up van de kop) + onderdelenvel (`onderdelen.png`, `onderdelen.py`).

## Zwakke punten
1. De linker snorharen zijn kort (frame); op 1× zijn het drie streepjes aan de snuit.
2. Op 8× ogen de verre snorharen (F) over de borst als strepen in de crème.
3. De pluimvlammen zijn minder slank dan bij Gemini (zie onderdelenvel).
4. De terracotta schaduw achter het wangaanhangsel is zoals Gemini, maar dat was in r1/r2 de "riem"-kritiek van de keurders; nu bewust gevolgd.
Niets gecommit.
