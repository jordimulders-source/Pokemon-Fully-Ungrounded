# Awki – keuring ronde 3 (onafhankelijke keurder)

**Gekeurd:** `kleur_r3/awki.png` (64×64, 16 kleuren, `normal.pal`), raster `kleur_r3/raster.txt`.
**Tegen:** `referenties/model_gekozen.png` (bevroren), silhouet `silhouet/silhouet.png`.
**Close-ups:** `vergelijk.png` (geheel 8×, kop+kuif 14×, opgeheven vleugel 12×, buik–vleugel 12×, gevouwen vleugel+staart 10×, poten 14×, telkens sprite | model op exact dezelfde schaal (model via EXTENT-transform met schaal 6.232, top 2, left 4); onderaan 1× en 2× op licht en donker naast Pidgeotto, Swellow, Fearow en het verkleinde model).
**Methode:** eerst zelf op het oog (1×, 2×, 8×), daarna gemeten met `kw.py` (model per kwartvak), mediaan-RGB per spritepixel, kleurgroep-telling per zone, `controle.py`, `rand.py`, `los1.py` en een eigen randscan per kant.

Alleen de twee eisen getoetst: (1) accuraat op het model, (2) Gen 3-techniek.

## Eis 1 – accuraat op het model

| Onderdeel | Oordeel | Bevinding (gemeten) |
|---|---|---|
| Kuif: vorm | PASS | Silhouet = model (diff 8, alleen het toegestane gat). Waaier schuin naar achteren-boven, zelfde lengte en breedte. |
| Kuif: strepen | PASS | Oranje- en karmijnstrepen in de lengterichting liggen op de modelkwartvakken (bijv. (36–37,9) 7 = model 6777/7777; (40,9) D = model DD66). Gemiddelde kleur kuif sprite (196,96,61) tegen model (206,95,65). |
| Kuif: lavendel punt | PASS | Punt (39–44, 3–9), diagonale grens lavendel/rood onder 45° = model. Donkere F-band linksonder, lichte E rechtsboven zoals het model ((41–43,5) E = model EEFF/EEFE/EEEE). F als selout aan de rechterrand vervangt de Gemini-gloed (toegestaan volgens SPEC). Rechterrand op (44,7) is 1 px smaller dan het model: onder de drempel. |
| Kuif: onderrand / uiteinde onderkant | PASS | Onderrand zwart aan de schaduwkant op de silhouetrand; het model heeft daar donkerrood (5/D) met een donkere rand (39,12) 6D5B, (40,12) 55... Uiteinde: (42–43,10) zwart, model (42,10) 6666 / (43,10) 3.C.; dit zijn silhouetrandpixels, dus omlijning hoort daar. De trap 2-1-2-3 (rij 10–13) komt uit het bevroren silhouet. Ter info: wil Jordi het uiteinde zachter, dan kan (42,10) donkerrood 5 worden (model daar rood 6) zodat de zwarte voet onder de punt maar 1 px breed is; geen eis. |
| Kuif: belijning en schaduw | PASS | Lichtkant karmijn-selout (37–38,6),(36,7),(35,8),(34,9) = model D66D/C6D6/D666; schaduw (D/6) langs de onderzijde = model. |
| Geel voorhoofd | PASS | Toef (24–31, 14–18) in A/9 met okerrand = model (bijv. (25–28,17) AAAA = model AAA8/9AAA/A998/AAAA). Scheidingslijn kuif|toef (27,15),(28,16) bruin 3 = model 4585/9855 (gemeten bruinig, geen rood). |
| Rood vlakje | PASS | 2×2 op (28–29, 19–20): 6 links, D rechts = model 8466/66DD en 316D/D1D2. Klein, geen bol. |
| Masker | PASS | Zwart masker (30–33, 18–21) = model 8111/1222/2222. |
| Oog | PASS | 2×2: glans B (30,19), iris oker (31,19–20), pupil bruin (30,20) = model C141 / 4849 / 3424 / 884C. Leest op 1× als oog met glans (zie 1×-rij). |
| Snavel | PASS | Lengte en plek = model (punt x21, rij 20–21). Boven licht C, onder 4 = model 4CCC/C4C4 resp. C444/4444. Ter info: op (22–23,20) staat de bovenomlijning in de snavel (model daar grijs 4422 tegen achtergrond), waardoor de punt 1 px dunner is; volgt uit het silhouet + 1 px buitenlijn, geen eis. |
| Witte keel | PASS | (28–33, 22–25) wit B = model BBBB; grijze C-schaduw links/onder = model (26,23) 11CC, (27,23) 2CCC. |
| Gouden oorvlek | PASS | (34–37, 19–22) = model 48AA/94A8/AAAA/9888/A988/8888. (36,20) is A waar het model 9888 heeft: 1 px, onder de drempel. |
| Opgeheven vleugel: kleurbanden | PASS | Volgorde geel → oranje → karmijn → bruine voorrand = model. Gemiddelden per band: oranje (226,146,69) tegen (236,163,66), karmijn (149,52,46) tegen (153,53,47). Bruine voorrand 2 px breed = model (17–18,16) 3454/4444. |
| Opgeheven vleugel: veerlijnen (Jordi's hoofdpunt) | PASS | Alle zeven donkere lijnen onder de gele veren liggen op de modelplekken: F1\|F2 (7,9–10) = model 2/1 op x7,5; F2\|F3 (7,16)-(8,17)-(9,18) = model 38B1/1894/4995; F3\|F4 (5,20),(6,21) 1 + (7,21) 2 = model B4.3/8AB2; F4 (7–9,26),(10–11,27) = model B1.4/184B/18B3/AA11; F5\|F6 (8–11,30) = model C3.B/3AC2/AA22/AA22; F6 (10–11,33),(12–14,34) = model 2544/8A49/11../11../11B8; F7\|F8 (15–17,36),(18,37) = model AA11/AA11/AA22. De rode veerlijnen in de oranje band ((11,15)-(12,16)-(13,17)-(13,18), (10–11,19)-(12,20)) en de donkerrode lijnen in het karmijn (L1–L5, kolom x19 rij 20–25) liggen op modelkwartvakken met 5/6 (D5DD, D5D5, 52D5). Geen zebra: één lijn per veerrij. Op 2× lezen de veren als losse vingers zoals het model. |
| Opgeheven vleugel: gele veerpunten | PASS | Vorm en lengte per vinger volgen het silhouet; okerbovenranden F4/F6 op model 8888/B9888. Er is iets meer oker dan in het model (59 tegen 29 px in de vleugelzone), vooral als selout op de silhouetrand; binnenin is het verschil enkele pixels (bijv. (9,12), (12,10)) en niet zichtbaar op 1×/2×. |
| Gevouwen vleugel | PASS | Tonen per pixel vrijwel gelijk aan het model (4 boven, 3 midden, 2 onder; gemiddelde (96,71,57) tegen (97,72,57)). Lichte veerranden op de modelplekken. |
| Buik + aansluiting buik–linkervleugel (Jordi's punt) | PASS | Rij 31–40 x17–23 per pixel gelijk aan het model (bijv. rij 31: 7 7 6 6 D D 5 8 9 = model 7777/7777/6677/6D7D/DDDD/DDDD/D354/8889/9494). Bruine scheiding (21,35–37) = model 9394/8483/A4A4; onderste gele punt ligt over de buik zoals het model. Bruine punten van de borst in de buik (26–27, 30–33) = model 4444/4343. Buik (201,150,73) tegen (197,150,69). |
| Aansluiting buik–gevouwen vleugel | PASS | Zwarte diagonaal (36,41)…(43,47) = de dunne zwarte lijn van het model (8188/8388: één zwart kwartvak). |
| Staart | **FAIL (klein)** | Vorm, onderrand met twee segmenten (50–53,53) en (56–59,53) en de donkere lijnen kloppen. Maar er staan 4 oranje (7) lichtpixels die het model niet heeft: (52,48), (53,48), (56,50), (58,51). Gemeten modelhelderheid daar 93, 93, 96, 107; de rest van de staart 85–95; palet 6 = 104, 7 = 136. Het model is een gelijkmatige roestkleur zonder lichtvlekjes. |
| Poten | PASS | Linkerpoot diagonaal van (30–32,50) naar (29–30,54), voet met tenen naar links (24–30, 55–58) = model per pixel (rij 56: 1 4 C 4 3 4 3 3 3 1 tegen ...1/4233/3C44/4422/4224/3443/4431/3311/3311/3113). Rechterpoot verticaal x40, gespreide tenen (36–43, 56–60) = model. Verre en nabije poot in perspectief zoals het model. |
| Gat tussen vleugel en hals | PASS | Alleen de toegestane 8 px (23–24, 23–26). |

## Eis 2 – Gen 3-techniek

| Punt | Oordeel | Bevinding |
|---|---|---|
| Buitenlijn/selout | PASS | Zwart aan de schaduwkant; gekleurde selout aan de lichtkant: oker om de gele veren, karmijn op de kuifbovenrand, F om de lavendel punt, 5 op de staartbovenrand. |
| Geen lichte kleur op de buitenrand | PASS | `rand.py` 0; eigen scan: aan de rechter- en onderkant alleen 1/2/3/5/6/8/F. Oker op de veerpunten = selout van het model. |
| Losse pixels | PASS | `los1.py`: alleen lijnuiteinden en de maskerrand, geen omlijningspixel midden in een vlak. `controle.py`: kleine clusters zijn lijnstukjes, het rode vlakje, het oog, teenscheidingen en één glanspixel (26,56). |
| ≤ 3 tinten per vlak | PASS | Geel A/9/8, vuur 7/6/D (+5 voor lijnen), lavendel E/F, bruin 4/3/2, keel B/C, buik 9/8 (+4 streepje). Voet 4/3/2 + één glanspixel C. |
| Geen zebra/raster/dambord | PASS | Veerlijnen één per veerrij; de rood-in-oranjepixels vormen diagonale lijnen, geen dambord. De tenen hebben 3/4-afwisseling, zoals het model ze tekent (teenscheidingen). |
| Oog leest op 1× | PASS | Glanspixel in het masker; op 1× licht en donker zichtbaar. |
| Leest op 1× op licht en donker | PASS | Naast Pidgeotto/Fearow: zelfde dichtheid en omlijning; kuif, vleugel en kop lezen op beide achtergronden. |

## Reparatie (FAIL)
**Staart, 4 px:** (52,48) 7 → 6, (53,48) 7 → 6, (56,50) 7 → 6, (58,51) 7 → 6. Gemeten modelhelderheid 93/93/96/107, dichtst bij rood 6 (lum 104); model kw (52,48) DDDD, (53,48) DDD6, (56,50) 68DD, (58,51) 66D6. Rest van de sprite: pixeldiff 0.

## Ter info voor Jordi (geen eis)
- Uiteinde kuif onderkant: zwarte voet (42–43,10) onder de lavendel punt komt uit het silhouet; zachter kan door (42,10) → 5.
- Snavelpunt (22–23,20) is omlijning i.p.v. grijs, waardoor de punt 1 px dunner is dan in het model.

## Eindoordeel
**Bijna goed: één kleine FAIL (staart, 4 px), verder PASS op beide eisen.** De punten die Jordi noemde (vleuglijnen, aansluiting buik–linkervleugel, poten, uiteinde kuif, belijning/schaduw van kuif en oog) liggen gemeten op het model en zijn technisch in orde. Na de staartreparatie (pixeldiff 0 erbuiten) kan de sprite naar Jordi zonder nieuwe keuring.
