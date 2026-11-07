# Keuring poedelmot kleur_r19 (verse keurder, eerst blind geoordeeld)
Bron: `referenties/samengesteld.png`, mapping x 139–854 → 62 px, offset (1,17). Meting per spritepixel: gem/p15 van de modelhelderheid (`stappen/px.py`-methode).
8×: `scratchpad/keur_r19/naast.png` (model | sprite). 16× per zone: `kop.png`, `links.png`, `rechts.png`, `poten.png`, `klauw.png`, `sprietL.png`, `sprietR.png`. 1×/7× tegen het BOX-verkleinde model: `box7.png`, `1x_3.png`. Gen 3: `gen3.png` (Venomoth | Dustox | poedelmot). Alles in `/tmp/claude-0/-home-user/00176e0d-eaf6-508f-a6c5-463bdec7182b/scratchpad/keur_r19/`.

1×: houding, massa, ogen, kin, kraag, poten en klauwtjes lezen zoals het verkleinde model. Twee dingen lezen anders. De sprieten zijn zebra (zwart/tan) en hun nerf valt weg, waar het verkleinde model een donker, fijn getextureerd blad met een duidelijke lichte nerf geeft. De bovenste krul van de rechtervoorvleugel ligt ook verschoven.

## EIS 1: accuraatheid per onderdeel
| Onderdeel | Oordeel |
|---|---|
| Ogen | **Lijkt op het model.** Donkerkaart per pixel (model p15<70 tegen sprite 1/2/B): links en rechts klopt hij binnen 1 px. De glans links ligt op (18,34–35) en rechts op (27–28,35)+(27,36), op de modelplekken. Klein punt: in het model is (18,35) half donker (gem 110), dus de glans links is daar 1 px lang. |
| Kop/kin | **Lijkt op het model.** De kinlijn ligt waar het model hem heeft: (19,39), (20,41), (21–24,42) met model 79–116, p15 2–5, en (25–28,40–41). De kopkruin tussen de sprieten is licht, met een selout van 4 aan de lichtkant. |
| Sprieten: omtrek, punten, nerfligging | **Lijkt op het model.** De omtrek en de punten kloppen: links (1,18), rechts (52–53,19–20). De nerfboog ligt op de gemeten modelboog; de r18-klacht is opgelost. |
| Sprieten: vlak en baardjes | **Wijkt af.** Over het hele sprietvlak (1+6) is het model gem 53 met std 25–29 per spritepixel, de sprite gem 48 met std 67. De baardjes in 6 (lum 168) zijn bijna zo licht als de nerf C (lum 189). In het model meten de nerfpixels 107–115, ruim boven het vlak (53). De fase is willekeurig: op de 6-pixels meet het model gem 50, op de 1-pixels 54. Op 1× leest de sprite daardoor als zwart-tan zebra en verdwijnt de nerf links tussen de baardjes. Het verkleinde model is donker en fijn gestreept, met de nerf als lichtste lijn. |
| Bontkraag | **Lijkt op het model.** Wit, met haarstreken in 7 op de modelplekken. De onderrand naar de poten ligt goed: (26–29,47) en (16–17,47). |
| Linkervleugel | **Lijkt op het model in vorm, omtrek en kleur. Wijkt af in de tan streken.** Rij 31: het model is tan op x 9–11 en 15–16, de sprite heeft D op x 13–14 en 17–18. Rij 33: model x 10–13, sprite x 14–15. De streken liggen dus 2–3 px te ver rechts. Ernst: middel. |
| Rechtervoorvleugel | **Wijkt af in de krullen (belijning).** De buitenste krulboog ligt in de sprite (5) op (54,21), (55,22), (56,23), (56,24), (55,25) en (54–56,26). In het model (p15 155–165) ligt hij op (55–56,21), (56–57,22), (57–58,23), (57–58,24), (56–57,25) en (55–56,26). Hij staat dus 1–2 px te ver links, en op zijn plek in de sprite is het model wit (p15 206–215). Er zijn ook twee lijnstukjes die het model niet heeft: 444 op (51–53,24) (model p15 238–246, puur wit) en 555 op (52–54,26) (p15 216–246). De modeltan ligt daar op (50–51,25), (50,26) en (53–54,27). Ook rij 30 ligt 1 px te links: de sprite heeft 5 op x 47–49, het model is tan op x 48–52. De bovenrand en de rand van de vleugelpunt kloppen. |
| Rechterachtervoorvleugel/achtervleugel | **Lijkt op het model.** De scheidingslijn ligt op y35 x 41–51 en zakt bij x 52–53 naar y36; het model is daar donker (p15 2–63). De onderrand ligt op (40–43,44), (40/44,45) en (39–46,46) en klopt per pixel. De binnenkrullen zijn benaderd. Klein punt: (43–44,36) en (48–51,36) zijn wit waar het model licht tan is. |
| Middenstuk | **Lijkt op het model.** Platen 8/9 op x 30–34 en 6 op x 38–43, met ringlijnen zoals in het model. |
| Poot 1 (links voor) + klauwtjes | **Lijkt op het model.** Het balletje ligt op x 16–23, y 47–55. De klauwen op (18–20,55–57) en (22–24,55–56) vallen samen met het donker in het model. Hij sluit aan op de kraag. |
| Poot 2 + voetbal + klauwtjes | **Lijkt op het model.** De dij ligt op x 24–30, y 48–54 en de voetbal op x 25–30, y 56–58. De klauwen liggen op (24–29,58–59); in het model is het donker op x 24–27, y 58–59. |
| Verre poot (tan, x 31–34) | **Lijkt op het model.** Donker/tan op y 54–58, zoals het model (dark x 28–35). |
| Middenpoot voor + klauwtjes | **Lijkt op het model.** De bal ligt op x 35–40, y 54–59. De klauwen liggen op (35–39,60) en (36–39,61); in het model is het donker op x 35–39, y 60–61. |
| Rechterpoot + klauwtjes | **Lijkt op het model.** De bal ligt op x 41–47, y 52–58. De klauwen liggen op (43–46,58–59); in het model is het donker op x 43–46. |
| Belijning buiten | **Lijkt op het model.** Er zijn 0 open randen, de buitenlijn is overal 1 px, met de selout van 4 alleen aan de lichtkant. De sprietomtrek is zwart, met zwartbruin aan de bovenrand. |

## EIS 2: Gen 3 (naast Venomoth en Dustox, `gen3.png`)
- Er zijn 0 tintclusters < 3 px en 0 losse pixels. De contraststappen tussen A, 7, D, 6, 5, 4 en 3 zijn ±20–45. Het licht valt linksboven. **Voldoet.**
- **Palet:** C (214,192,160) en D (214,190,168) zijn praktisch dezelfde kleur (Δ 0/2/8). Dat zijn twee indexen voor één tint, en de crème-tan groep komt daardoor boven 3 tinten + lijn per vlak. Voeg ze samen.
- **Sprietvlak:** het 1/6-zebrapatroon met std 67 is drukker dan wat een Gen 3-sprite op een donker vlak doet. Venomoth en Dustox zetten op een donker vlak één middentint als textuur. Dit valt samen met de afwijking in EIS 1.
- De vleugelkrullen zijn hoekiger dan de doorlopende aders van Venomoth. Als ze op de modelboog liggen (reparatie 2), voldoet dat.

## Top-5 reparaties (alleen echte afwijkingen)
1. **Sprietbaardjes donkerder, zodat de nerf de lichtste lijn is.**
   - Zet de baardjes in een middentint van lum ±90–125 (bijv. 4, of een nieuwe tint), niet in 6 (168).
   - Mik op een vlakgemiddelde van ±53 en een std van ±25–30, zoals het model per spritepixel.
   - De nerf C blijft zoals hij nu is. Controleer op 1× naast het BOX-verkleinde model dat de nerf links en rechts doorloopt als de lichtste lijn.
2. **Rechtervoorvleugel, buitenste krulboog 1–2 px naar rechts.**
   - Leg de boog op (55–56,21), (56–57,22), (57–58,23), (57–58,24), (56–57,25) en (55–56,26).
   - Zet de oude plekken terug naar wit of crème. Het model meet daar p15 206–215.
3. **Verzonnen lijnstukjes in de voorvleugel weg.**
   - Maak 444 op (51–53,24) en 555 op (52–54,26) licht (model 230–247).
   - Leg de tan op de modelplekken: (50–51,25), (50,26) en (53–54,27).
   - Rij 30: 5 op x 48–52 in plaats van x 47–49.
4. **Linkervleugel, tan streken 2–3 px naar links.** Rij 31: model x 9–11 en 15–16. Rij 33: model x 10–13. Meet ook rij 30 en 32 opnieuw.
5. **C en D samenvoegen** tot één index (één tint), en de vrijgekomen index gebruiken voor de middentint van de baardjes (reparatie 1). Klein punt, alleen als de ronde het toelaat: de glans links op (18,35) inkorten (model gem 110).

Oordeel: FAIL
