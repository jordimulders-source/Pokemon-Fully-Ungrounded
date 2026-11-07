# Keuring viscacha kleur r5 (onafhankelijke keurder, 7 nov)
- Bron: `referenties/gemini_gekozen_ronde6.png` (origineel 1024×680, voor de vergelijking afgebeeld op de sprite met sx = (ox−220)/10, sy = (oy+15)/10; de sprite-omtrek valt daar vrijwel precies op), `kleur_r5/gemini64.png` (let op: deze verkleining snijdt Gemini's snorharen ook af), SPRITE_KERN.md, GEMINI.md.
- Bekeken op 8× (nearest) en 1× licht/donker, plus close-ups op 12–16× naast elkaar: kop, gezicht, staart, lijf, poten.

## Blind (vóór vergelijken)
Leest op 1× als bruingeel knaagdier met gele kraag en gele staartpluim. Op 8×: het gezicht is een platte verticale voorkant (x2, rij 26–31); neus en mond zijn een donker deukje binnen de omtrek, geen snuit. Linker snorharen zijn losse stompjes tegen de framerand, niet verbonden met de snuit. Over de crème borst ligt een raster van grijsbruine streepjes. Pootjes dun als stokjes, geen tenen. Pluim goudgeel en blokkig.

## Afvinktabel
| onderdeel | lijkt op Gemini | wijkt af in | ok? |
|---|---|---|---|
| kop | massa en plek kloppen (omtrek valt op Gemini) | voorkant is recht; Gemini is rond met de snuit als voorste punt | nee |
| oor ver | smal, rozige binnenkant onderin | – | ja |
| oor nabij | brede schelp, donkere binnenkant | – | ja |
| oog | lui, mag (Jordi) | – | ja |
| neus | donker, 3 px, ongeveer juiste hoogte (4–5,31),(4,32) | zit 2 px binnen de omtrek in een terugwijkend stuk (rij 32–33 begint pas op x3); bij Gemini is de neus het voorste punt van de snuit, op de rand. Op 1× niet te zien | nee |
| mond | korte lijn (4–6,33) | Gemini: Y-mondje (lijn omlaag uit de neus, dan kort naar achteren); nu één horizontaal streepje dat met de neus één donkere vlek vormt | nee |
| snuitvorm | – | Gemini: voorhoofd loopt schuin naar een ronde snuitbult op neushoogte (rij 31–33); sprite: voorhoofd steekt het verst uit (x2, rij 26–31), snuit wijkt terug (x3, rij 32–33) | nee |
| kin | crème onder de mond | Gemini: ronde kin met terracotta onderlip (±6–9, 35–36) en zwarte kinlijn, bef begint daaronder | deels |
| snorharen nabij | 3 lijnen van 1 px, uitwaaierend | ±3–4 px i.p.v. ±8 px (Gemini loopt tot ox≈165 → sx≈−5: valt buiten het frame), en los van de snuit: gaten op (2,32), (1–2,33); lezen als streepjes | nee |
| snorharen ver | 2 lijnen, richting rechtsonder | verkeerde plek, hoek en kleur: Gemini van de wang onder het oog (±8,33)/(9,34) vlak (helling ±0,35) naar onder de sikkelpunt (±20,37)/(21,38), in dezelfde donkerbruine lijnkleur; sprite (11–16,37–42) steil, op de bef, in E = de crème schaduwtint → met de E-pixels rond (11–17,37–42) een gestippeld raster | nee |
| gele pluk snuit/voorhoofd | twee punten op de kopvoorkant | 1–2 px te hoog (sprite rij 25–28, Gemini rij 26–30, op het voorhoofd net boven de neus) | deels |
| gele wangaanhangsel | grootte (±10×11), plek en sikkelvorm kloppen: punt (21–24,26), bolle kant x14, onderpunt (20–21,35–36), terracotta erachter zoals Gemini | – | ja |
| borst/bef | crème vlak, plek klopt | raster van E-pixels (zie verre snorharen); Gemini: schoon crème met één schaduwtint langs de rand | nee |
| voorpoten | plek en houding (ver opgeheven links, nabij lager) | Gemini: ronde wantpootjes met teenlijntjes; sprite: dunne stokjes met stompje (8–12,40–49) en (17–22,43–50) | nee |
| lijf/rug | massa, vachtpiek (34–38,26–27) | Gemini heeft een binnenlijn om de ronde dij en schouder; sprite niet; gekartelde vacht op de bil bij de staartaanzet ontbreekt | nee |
| buik | crème vlek, plek | Gemini: driehoekige vlek tussen voorpoot en dijlijn; sprite: losse ronde vlek zonder begrenzing | deels |
| achterpoten | terracotta, perspectief | Gemini: voeten met teenlijntjes (verre voet 22–29,55–58; nabije 41–48,59–62); sprite: platte klompen | deels |
| staart | tweekleurig, vorm volgt het masker | onderrand staartaanzet recht over 8 px (47–54,48); Gemini rond | deels |
| pluim | plek, gekarteld | Gemini: 4 slanke hoge vlammen in bleek citroengeel met lichte kern; sprite: 3 brede, lage punten, overwegend goudgeel (232,184,24) met donkere oker; bruine staart steekt bij Gemini in wiggen de pluim in | nee |
| kleuren | lijf, crème, terracotta, oor | pluim te donker/goud (zie boven); E (152,128,80) dubbel gebruikt als bef-schaduw én snorhaar → raster | deels |

## Coördinatorpunten getoetst
- Verre snorharen lezen als gestippelde strepen/raster: **bevestigd** (E-kleur, rij 37–42, mengt met de bef-schaduw).
- Linker snorharen kort: **bevestigd** (±4 px i.p.v. ±8, en niet aan de snuit vast).
- Neus moeilijk te zien: **bevestigd** (binnen de omtrek, versmelt met mond tot één vlek).

## Techniek
- Open randen 0, 16 kleuren, png = raster: ok.
- Losse pixels (3,36),(2,37),(1,38),(0,39): diagonale snorhaar, acceptabel als hij aan de snuit vastzit; nu zweeft hij.
- Kleurgroep crème: E als derde tint ligt als checker in het vlak (banding/ruis) → niet netjes.
- Rechte stukken: staartonderrand (47–54,48).

## Reparaties (via de maker)
1. **Framing (eerst, ontwerpvraag aan Jordi/coördinator):** Gemini inclusief snorharen is ±67 px breed op deze schaal; de snorharen passen alleen als de hele sprite ±7% kleiner (schaal ±0,093) of het masker opnieuw van het origineel. Anders blijven ze afgekapt = afwijking.
2. **Snuit:** voorhoofd rij 26–29 naar x3 (pluk erop), snuitbult rij 31–33 naar x2 als voorste punt; neus 2–3 px donker óp de voorrand (2–3,31–32); Y-mond: (3–4,33) omlaag, dan (5–6,34) naar achteren; ronde kin met terracotta onderlip (6–9,35–36) en kinlijn; bef pas vanaf rij 36–37.
3. **Snorharen nabij:** 3 lijnen in A die aan de snuit vastzitten (start (1–2,32–34), geen gaten), uitwaaierend (±10°, ±30°, ±50° omlaag), zo lang als het frame na reparatie 1 toelaat (doel ±8 px).
4. **Snorharen ver:** E-streepjes (11–16,37–42) weg; bef rij 37–42 schoon crème 6 met 5 langs de rand. Twee lijnen van 1 px in A van (8,33)→(20,37) en (9,34)→(21,38), vlak, eindigend onder de sikkelpunt.
5. **Pluk:** 1–2 px omlaag naar rij 26–30.
6. **Pluim:** 4 slanke vlammen, hoogste tot rij 9–10; hoofdkleur bleek citroen (9 en een lichtere), 8 als schaduw, 7 alleen als selout; bruine wiggen van de staart in de pluimbasis zoals Gemini.
7. **Voorpoten:** ronde wantjes met teenlijntje, ver (8–12,43–47), nabij (17–22,46–50).
8. **Lijf:** binnenlijn om de dij (boog ±(35,34) → (45,47)) en schouder, buikvlek driehoekig begrensd door die lijn; gekartelde vacht op de bil bij de staartaanzet (±44–46,33–40).
9. **Achterpoten:** teenlijntjes op beide voeten; staartonderrand (47–54,48) rond maken.

Oordeel: FAIL
